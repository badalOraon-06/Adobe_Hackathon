import os
import json
import time
from extractor import extract_outline

def main():
    start_time = time.time()

    input_dir = "/app/input"
    output_dir = "/app/output"
    os.makedirs(output_dir, exist_ok=True)

    if not os.path.exists(input_dir):
        print(f"Error: Input directory {input_dir} does not exist")
        return

    pdf_files = [filename for filename in os.listdir(input_dir) 
                 if filename.lower().endswith(".pdf")]
    
    if not pdf_files:
        print("No PDF files found in input directory")
        return

    print(f"Found {len(pdf_files)} PDF file(s) to process")

    for filename in pdf_files:
        print(f"Processing: {filename}")
        input_path = os.path.join(input_dir, filename)
        output_filename = os.path.splitext(filename)[0] + ".json"
        output_path = os.path.join(output_dir, output_filename)

        try:
            result = extract_outline(input_path)
            
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            print(f"✓ Successfully processed {filename} -> {output_filename}")
            
        except Exception as e:
            print(f"✗ Error processing {filename}: {e}")
            # Create empty result to avoid missing output files
            empty_result = {"title": "", "outline": []}
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(empty_result, f, indent=2, ensure_ascii=False)

    duration = time.time() - start_time
    print(f"Execution completed in {duration:.2f} seconds")

if __name__ == "__main__":
    main()