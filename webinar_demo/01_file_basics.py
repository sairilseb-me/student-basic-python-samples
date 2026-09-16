"""
01 - File System Basics with pathlib
--------------------------------------
Goal: Stop navigating folders manually. Let Python find and filter
files for you. This is step 1 toward automating anything that
touches a bunch of files.
"""

from pathlib import Path

# Point to the folder of sample clearance forms
folder = Path("sample_documents")

print("All files in the folder:")
for file in folder.iterdir():
    print(" -", file.name)

print()

# Filter to only PDFs (this is the pattern you'll use constantly)
print("Only PDF files:")
pdf_files = list(folder.glob("*.pdf"))
for pdf in pdf_files:
    print(" -", pdf.name)

print()
print(f"Total PDFs found: {len(pdf_files)}")

# Pull useful info out of each filename
print()
print("Extracting student names from filenames:")
for pdf in pdf_files:
    student_name = pdf.stem.replace("_clearance", "").replace("_", " ")
    print(f" - {student_name}")
