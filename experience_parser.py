import spacy
from typing import Optional, List, Dict
class ExperienceParser:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.experience_keywords = [
            "experience", "exp", "years", "yrs", "minimum", 
            "maximum", "at least", "required", "qualification",
            "work experience", "professional experience"
        ]
        self.number_words = {
            'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
            'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10
        }

    def extract_experience(self, text: str) -> Optional[str]:
        if not text or not isinstance(text, str):
            return None            
        doc = self.nlp(text.lower())
        experience_phrases = self._find_experience_phrases(doc)
        if not experience_phrases:
            return None
        normalized_ranges = []
        for phrase in experience_phrases:
            normalized = self._normalize_experience(phrase.text)
            if normalized:
                normalized_ranges.append(normalized)
        if not normalized_ranges:
            return None
        return self._merge_ranges(normalized_ranges)

    def _find_experience_phrases(self, doc) -> List:
        phrases = []
        for sent in doc.sents:
            if any(keyword in sent.text.lower() for keyword in self.experience_keywords):
                phrases.append(sent)
        return phrases

    def _normalize_experience(self, phrase: str) -> Optional[str]:
        phrase = self._replace_word_numbers(phrase.lower())
        tokens = phrase.split()
        if "to" in tokens:
            idx = tokens.index("to")
            if idx > 0 and idx < len(tokens)-1:
                first = self._extract_number(tokens[idx-1])
                second = self._extract_number(tokens[idx+1])
                if first is not None and second is not None:
                    return f"{min(first, second)} - {max(first, second)} Years"        
        for i, token in enumerate(tokens):
            if "-" in token and not token.startswith("-") and not token.endswith("-"):
                parts = token.split("-")
                if len(parts) == 2:
                    first = self._extract_number(parts[0])
                    second = self._extract_number(parts[1])
                    if first is not None and second is not None:
                        return f"{min(first, second)} - {max(first, second)} Years"
        if "minimum" in tokens:
            for i, token in enumerate(tokens):
                if token == "minimum" and i < len(tokens)-1:
                    num = self._extract_number(tokens[i+1])
                    if num is not None:
                        return f"{num} - {num + 2} Years"
        if "maximum" in tokens:
            for i, token in enumerate(tokens):
                if token == "maximum" and i < len(tokens)-1:
                    num = self._extract_number(tokens[i+1])
                    if num is not None:
                        return f"{num - 2} - {num} Years"
        if "at" in tokens and "least" in tokens:
            at_idx = tokens.index("at")
            if at_idx < len(tokens)-2 and tokens[at_idx+1] == "least":
                num = self._extract_number(tokens[at_idx+2])
                if num is not None:
                    return f"{num} - {num + 2} Years"
        for i, token in enumerate(tokens):
            if "+" in token and not token.startswith("+"):
                num_part = token.split("+")[0]
                num = self._extract_number(num_part)
                if num is not None:
                    return f"{num} - {num + 2} Years"
        for i, token in enumerate(tokens):
            num = self._extract_number(token)
            if num is not None and i < len(tokens)-1:
                next_token = tokens[i+1]
                if next_token.startswith(("year", "yr", "yrs")):
                    return f"{num} - {num + 2} Years"        
        return None

    def _extract_number(self, text: str) -> Optional[int]:
        cleaned = ''.join(c for c in text if c.isalnum())
        if cleaned in self.number_words:
            return self.number_words[cleaned]
        if cleaned.isdigit():
            return int(cleaned)            
        return None
        
    def _replace_word_numbers(self, text: str) -> str:
        words = text.split()
        for i, word in enumerate(words):
            cleaned_word = ''.join(c for c in word if c.isalnum())
            if cleaned_word in self.number_words:
                words[i] = word.replace(cleaned_word, str(self.number_words[cleaned_word]))
        return ' '.join(words)

    @staticmethod
    def _merge_ranges(ranges: List[str]) -> str:
        if len(ranges) == 1:
            return ranges[0]            
        narrowest = ranges[0]
        min_diff = float('inf')        
        for r in ranges:
            parts = r.split(' - ')
            diff = int(parts[1].split()[0]) - int(parts[0])
            if diff < min_diff:
                min_diff = diff
                narrowest = r                
        return narrowest