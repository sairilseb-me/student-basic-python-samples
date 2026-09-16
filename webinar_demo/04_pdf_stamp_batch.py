"""
04 - Batch Signing: Putting It All Together
--------------------------------------
Goal: Combine everything from scripts 01-03 into one automation:
find every clearance PDF in a folder, stamp a signature on each
one, and save the results in a new folder. No manual clicking,
no doing it one by one.

This is the "toy version" of the real clearance app you'll demo
right after this.
"""

from pathlib import Path
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

SOURCE_FOLDER = Path("sample_documents")
SIGNATURE_IMAGE = "assets/signature.png"
OUTPUT_FOLDER = Path("signed_output")

OUTPUT_FOLDER.mkdir(exist_ok=True)


def build_signature_overlay():
    """Creates a one-page PDF containing just the signature image,
    positioned where we want it to land on every document."""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawImage(
        SIGNATURE_IMAGE,
        x=160, y=280,
        width=180, height=60,
        mask="auto",
    )
    c.save()
    buffer.seek(0)
    return PdfReader(buffer)


def sign_pdf(source_path: Path, overlay_reader, output_folder: Path):
    """Stamps the signature onto one PDF and saves it to the output folder."""
    reader = PdfReader(source_path)
    writer = PdfWriter()

    page = reader.pages[0]
    page.merge_page(overlay_reader.pages[0])
    writer.add_page(page)

    output_path = output_folder / f"SIGNED_{source_path.name}"
    with open(output_path, "wb") as f:
        writer.write(f)

    return output_path


def run_batch_signing():
    overlay_reader = build_signature_overlay()
    pdf_files = list(SOURCE_FOLDER.glob("*.pdf"))

    print(f"Found {len(pdf_files)} document(s) to sign.\n")

    for pdf_file in pdf_files:
        output_path = sign_pdf(pdf_file, overlay_reader, OUTPUT_FOLDER)
        print(f"Signed: {pdf_file.name} -> {output_path.name}")

    print(f"\nDone. {len(pdf_files)} document(s) signed and saved in '{OUTPUT_FOLDER}/'.")


if __name__ == "__main__":
    run_batch_signing()
