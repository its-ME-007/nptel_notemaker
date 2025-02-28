import os
import subprocess
import sys
import time
#just add a file upload procedure for any hacks. 
def run_script(script_name, description):
    """Run a Python script and check its exit status."""
    print(f"\n{'='*60}")
    print(f"RUNNING: {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run([sys.executable, script_name], check=True)
        if result.returncode == 0:
            print(f"\n✅ Successfully completed: {script_name}")
            return True
        else:
            print(f"\n Failed to execute {script_name} with return code {result.returncode}")
            return False
    except subprocess.CalledProcessError as e:
        print(f"\n Error executing {script_name}: {str(e)}")
        return False
    except Exception as e:
        print(f"\n Unexpected error running {script_name}: {str(e)}")
        return False

def ensure_directories():
    """Ensure necessary directories exist."""
    os.makedirs("response_files", exist_ok=True)

def check_api_key():
    """Check if the Gemini API key is set."""
    if "GEMINI_API_KEY" not in os.environ:
        api_key = input("Please enter your Gemini API key: ").strip()
        os.environ["GEMINI_API_KEY"] = api_key
        print("API key set for this session")

def main():
    """Main execution function to run all scripts in sequence."""
    print("\n🚀 Starting NPTEL transcript extraction and processing pipeline")
    
    # Setup
    ensure_directories()
    check_api_key()
    
    # Step 1: Run the NPTEL transcript extractor
    if not run_script("nptel.py", "Extracting transcript from HTML"):
        print("Pipeline halted due to failure in transcript extraction")
        return
    
    # Step 2: Run the Gemini model processing
    if not run_script("api.py", "Processing transcript with Gemini AI"):
        print("Pipeline halted due to failure in AI processing")
        return
    
    # Step 3: Convert XML response to PDF
    # First rename the response file to what response_to_pdf.py expects
    # try:
    #     os.rename("response_files/response.xml", "notes.xml")
    #     print("✅ Renamed response.xml to notes.xml")
    # except FileNotFoundError:
    #     print("❌ Could not find response.xml file")
    #     return
    # except Exception as e:
    #     print(f"❌ Error renaming file: {str(e)}")
    #     return
    
    if not run_script("response_to_pdf.py", "Converting XML to PDF"):
        print("Pipeline halted due to failure in PDF conversion")
        return
    
    print("\n✨ PIPELINE COMPLETED SUCCESSFULLY ✨")
    print("Output PDF available at: output.pdf")

if __name__ == "__main__":
    start_time = time.time()
    main()
    elapsed_time = time.time() - start_time
    print(f"\nTotal execution time: {elapsed_time:.2f} seconds")
