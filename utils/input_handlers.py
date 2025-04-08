from typing import Optional, List

def get_user_input() -> Optional[str]:
    print("\nEnter/Paste your job description (press Enter twice to finish):")
    try:
        lines = []
        while True:
            line = input()
            if line == '':
                if len(lines) >= 1:
                    break
                else:
                    print("Please paste the job description first")
                    continue
            lines.append(line)
        return "\n".join(lines) if lines else None
    except KeyboardInterrupt:
        return None
    except EOFError:
        return "\n".join(lines) if lines else None

def process_multiple_inputs() -> List[str]:
    print("Enter multiple JDs separated by '==' (press Enter twice when done):")
    print("Type your JDs, then press Enter twice to finish:")
    content = []
    empty_line_count = 0
    while True:
        try:
            line = input()
            if line.strip() == '':
                empty_line_count += 1
                if empty_line_count >= 2:
                    break
            else:
                empty_line_count = 0
                content.append(line)
        except EOFError:
            break
    full_text = "\n".join(content)
    return [jd.strip() for jd in full_text.split("==") if jd.strip()]