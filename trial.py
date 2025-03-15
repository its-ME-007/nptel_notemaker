import os
import time
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def upload_to_gemini(path, mime_type=None):
    file = genai.upload_file(path, mime_type=mime_type)
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file

def wait_for_files_active(files):
    print("Waiting for file processing...")
    for name in (file.name for file in files):
        file = genai.get_file(name)
        while file.state.name == "PROCESSING":
            print(".", end="", flush=True)
            time.sleep(10)
            file = genai.get_file(name)
        if file.state.name != "ACTIVE":
            raise Exception(f"File {file.name} failed to process")
    print("...all files ready")
    print()

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain", #set output to markdown
}

model = genai.GenerativeModel(
    model_name="tunedModels/datasetscraper-pgkowqrd1on0",
    generation_config=generation_config,
)

# TODO Make these files available on the local file system
files = [
    upload_to_gemini("response_files/lecture_4.txt", mime_type="text/plain"),
    upload_to_gemini("response_files/lecture_5.txt", mime_type="text/plain"),
    upload_to_gemini("response_files/lecture_6.txt", mime_type="text/plain"),
    upload_to_gemini("response_files/lecture_7.txt", mime_type="text/plain"),
    upload_to_gemini("response_files/lecture_8.txt", mime_type="text/plain"),
    upload_to_gemini("response_files/lecture_9.txt", mime_type="text/plain"),
]

# Some files have a processing delay. Wait for them to be ready.
wait_for_files_active(files)

dest_folder = "notes_folder"
#os.makedirs(dest_folder, exist_ok=True) # Create folder if it doesn't exist.
i = 3
for file in files:
    response = model.generate_content([
        "make pdf notes of this file.\n",
        file,
    ])

    response_file = os.path.join(dest_folder, f"notes_{i + 1}.md") #create the file name
    i += 1
    with open(response_file, "w") as f:
        f.write(response.text)

    # print(response.text)