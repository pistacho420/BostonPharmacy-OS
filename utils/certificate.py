from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import os


def create_certificate(name, score):

    filename = f"certificates/PTCB_Certificate_{name}.pdf"

    os.makedirs(
        "certificates",
        exist_ok=True
    )


    pdf = canvas.Canvas(
        filename,
        pagesize=letter
    )


    pdf.setFont(
        "Helvetica-Bold",
        24
    )

    pdf.drawCentredString(
        300,
        700,
        "Boston Pharmacy Training Academy"
    )


    pdf.setFont(
        "Helvetica",
        18
    )

    pdf.drawCentredString(
        300,
        620,
        "Certificate of Completion"
    )


    pdf.setFont(
        "Helvetica",
        14
    )

    pdf.drawCentredString(
        300,
        540,
        f"Awarded to: {name}"
    )


    pdf.drawCentredString(
        300,
        500,
        "PTCB Preparation Program"
    )


    pdf.drawCentredString(
        300,
        460,
        f"Exam Score: {score}%"
    )


    pdf.drawCentredString(
        300,
        420,
        f"Date: {datetime.now().strftime('%Y-%m-%d')}"
    )


    pdf.save()


    return filename