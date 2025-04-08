import os
import sys
from typing import List, Dict
from experience_parser import ExperienceParser
from utils.file_handlers import read_job_descriptions, save_results
from utils.input_handlers import get_user_input, process_multiple_inputs
from tqdm import tqdm

def process_jds(jds: Dict[str, str]) -> List[Dict]:
    parser = ExperienceParser()
    results = []    
    for jd_name, jd_text in tqdm(jds.items(), desc="Processing JDs"):
        try:
            experience = parser.extract_experience(jd_text)
            results.append({
                "Job Description": jd_name,
                "Extracted Experience": experience if experience else "Not Found",
            })
        except Exception as e:
            print(f"\nError processing {jd_name}: {e}")
            results.append({
                "Job Description": jd_name,
                "Extracted Experience": "Error",
            })    
    return results

def process_single_jd(jd_text: str, source_name: str = "pasted_jd") -> Dict:
    try:
        parser = ExperienceParser()
        experience = parser.extract_experience(jd_text)        
        return {
            "Job Description": source_name,
            "Extracted Experience": experience if experience else "Not Found",
        }
    except Exception as e:
        print(f"Error processing JD: {str(e)}")
        return {
            "Job Description": source_name,
            "Extracted Experience": "Error",
        }

def display_menu() -> int:
    print("\n" + "="*50)
    print("Job Experience Extractor".center(50))
    print("="*50)
    print("1. Process all JDs in sample_jds folder")
    print("2. Paste a single JD")
    print("3. Paste multiple JDs (separate with '==')")
    print("4. Exit")    
    while True:
        try:
            choice = int(input("\nEnter your choice (1-4): "))
            if 1 <= choice <= 4:
                return choice
            print("Please enter a number between 1 and 4")
        except ValueError:
            print("Invalid input. Please enter a number")

def main():
    output_file = os.path.abspath("results/output.csv")    
    while True:
        choice = display_menu()
        if choice == 1:
            jds = read_job_descriptions("sample_jds")
            if not jds:
                print("\nNo JDs found in sample_jds folder")
                continue
            results = process_jds(jds)
            save_results(results, output_file)
            print("\nProcessing Results:")
            for result in results:
                print(f"\n{result['Job Description']}:")
                print(f"Extracted: {result['Extracted Experience']}")
        elif choice == 2:
            print("\nPaste the job description (press Enter twice to finish):")
            jd_text = get_user_input()
            if not jd_text:
                print("\nNo input received or input was empty")
                continue
            result = process_single_jd(jd_text)
            print("\nResult:")
            print(f"Extracted Experience: {result['Extracted Experience']}")            
            save_choice = input("\nSave to results? (y/n): ").lower()
            if save_choice == 'y':
                save_results([result], output_file)
                print("Result saved successfully")
        elif choice == 3:
            jd_texts = process_multiple_inputs()
            if not jd_texts:
                print("\nNo valid inputs received")
                continue
            results = []
            for i, jd_text in enumerate(jd_texts, 1):
                if jd_text.strip():
                    results.append(process_single_jd(jd_text, f"pasted_jd_{i}"))
            if results:
                save_results(results, output_file)
                print("\nResults:")
                for result in results:
                    print(f"\n{result['Job Description']}:")
                    print(f"Extracted: {result['Extracted Experience']}")
        elif choice == 4:
            print("\nExiting...")
            break

if __name__ == "__main__":
    main()