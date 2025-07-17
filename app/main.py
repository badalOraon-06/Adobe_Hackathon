from extractor import extract_outline
import sys
import os

def main():
    input_path = "input/sample_outline_ai.pdf"  # You can change this path
    output_path = "output/outline.json"

    if not os.path.exists("output"):
        os.makedirs("output")

    outline = extract_outline(input_path)

    # Save output
    with open(output_path, 'w', encoding='utf-8') as f:
        import json
        json.dump(outline, f, indent=2, ensure_ascii=False)

    print(f" Outline extracted and saved to {output_path}")

if __name__ == "__main__":
    main()
