from pathlib import Path
from reportlab.pdfgen import canvas
def generate_text_pdf(lines: list[str], output_path: str = "reports/generated/report.pdf") -> str:
    path = Path(output_path); path.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(path)); y = 800
    for line in lines:
        pdf.drawString(50, y, line[:110]); y -= 20
        if y < 50: pdf.showPage(); y = 800
    pdf.save()
    return str(path)
