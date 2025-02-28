import os
from bs4 import BeautifulSoup

# Directory containing HTML files
outer_files_dir = "outer_files"

# Directory to save extracted text
response_files_dir = "response_files"
os.makedirs(response_files_dir, exist_ok=True)  # Ensure the output directory exists

# List all HTML files in outer_files directory
for file in os.listdir(outer_files_dir):
    if file.endswith(".html") or file.endswith(".htm"):  # Process only HTML files
        file_path = os.path.join(outer_files_dir, file)

        with open(file_path, 'r', encoding='utf-8') as f:
            html_doc = f.read()

        soup = BeautifulSoup(html_doc, 'html.parser')

        transcript_divs = soup.select("#video-transcript-div div")

        transcript_text = "\n".join(div.get_text(" ", strip=True) for div in transcript_divs)

        # Extract filename without extension
        file_name = os.path.splitext(file)[0] + '.txt'
        output_path = os.path.join(response_files_dir, file_name)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(transcript_text)

        print(f"Processed: {file} -> {file_name}")
