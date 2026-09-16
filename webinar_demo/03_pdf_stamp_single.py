"""
03 - Stamping a Signature onto ONE PDF
--------------------------------------
Goal: Show the actual mechanic behind "drag to sign": placing an
image at a specific (x, y) position on a PDF page, then saving a
new merged PDF. This is a simplified version of what the clearance
app does under the hood.
"""

from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

SOURCE_PDF = "sample_documents/Juan_Dela_Cruz_clearance.pdf"
SIGNATURE_IMAGE = "assets/signature.png"
OUTPUT_PDF = "output_single_signed.pdf"

# Step 1: build a small "overlay" PDF that contains ONLY the signature,
# positioned exactly where we want it on the page.
overlay_buffer = io.BytesIO()
overlay_canvas = canvas.Canvas(overlay_buffer, pagesize=letter)
overlay_canvas.drawImage(
    SIGNATURE_IMAGE,
    x=160, y=280,      # position on the page, in points
    width=180, height=60,
    mask="auto",        # keeps the transparent background transparent
)
overlay_canvas.save()
overlay_buffer.seek(0)

# Step 2: merge the overlay on top of the original PDF's page
original_pdf = PdfReader(SOURCE_PDF)
overlay_pdf = PdfReader(overlay_buffer)

writer = PdfWriter()
page = original_pdf.pages[0]
page.merge_page(overlay_pdf.pages[0])
writer.add_page(page)

# Step 3: save the result
with open(OUTPUT_PDF, "wb") as f:
    writer.write(f)

print(f"Signed PDF saved as: {OUTPUT_PDF}")
