import os
import pandas as pd
from typing import Dict, List
from tqdm import tqdm

def read_job_descriptions(directory: str) -> Dict[str, str]:
    jds = {}
    if not os.path.exists(directory):
        return jds
        
    files = [f for f in os.listdir(directory) if f.endswith(".txt")]
    for filename in tqdm(files, desc="Reading JDs"):
        try:
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as f:
                jds[filename] = f.read()
        except Exception as e:
            print(f"Error reading {filename}: {e}")
    return jds

def save_results(results: List[Dict], output_file: str) -> None:
    if not results:
        print("No results to save")
        return  
    try:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)        
        simplified_results = []
        for result in results:
            role_name = os.path.splitext(result["Job Description"])[0]
            simplified_results.append({
                "Role": role_name,
                "Experience": result["Extracted Experience"]
            })
        df = pd.DataFrame(simplified_results)
        required_columns = ["Role", "Experience"]
        df = df[required_columns]
        if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
            try:
                existing_df = pd.read_csv(output_file)
                combined_df = pd.concat([existing_df, df], ignore_index=True)
                combined_df.to_csv(output_file, index=False)
            except pd.errors.EmptyDataError:
                df.to_csv(output_file, index=False)
        else:
            df.to_csv(output_file, index=False)            
        print(f"Results successfully saved to {output_file}")
    except Exception as e:
        print(f"Error saving results: {str(e)}")