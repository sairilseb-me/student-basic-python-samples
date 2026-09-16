"""
02 - Batch Processing Pattern
--------------------------------------
Goal: Turn a "do this once" task into a function, then run it over
every file automatically. This is the core pattern behind almost
every automation script you'll ever write.
"""

from pathlib import Path

folder = Path("sample_documents")


def describe_file(file_path: Path) -> dict:
    """
    This function represents 'the one task' you want to automate.
    Today it just reads basic info, but this is the same slot
    where real processing (stamping, resizing, converting) goes.
    """
    student_name = file_path.stem.replace("_clearance", "").replace("_", " ")
    size_kb = file_path.stat().st_size / 1024
    return {
        "student": student_name,
        "file": file_path.name,
        "size_kb": round(size_kb, 2),
    }


def process_all_files(folder_path: Path):
    """This is the 'batch' part: loop + apply the task to everything."""
    results = []
    pdf_files = list(folder_path.glob("*.pdf"))

    for pdf_file in pdf_files:
        print(f"Processing {pdf_file.name} ...")
        result = describe_file(pdf_file)
        results.append(result)

    return results


if __name__ == "__main__":
    summary = process_all_files(folder)

    print()
    print("Batch summary:")
    for item in summary:
        print(f" - {item['student']}: {item['file']} ({item['size_kb']} KB)")
