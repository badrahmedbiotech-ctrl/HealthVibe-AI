from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def create_pdf(patient):

    filename = f"report_{patient['name']}.pdf"

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b>HealthVibe AI</b>", styles["Title"]))

    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(Paragraph(f"Patient: {patient['name']}", styles["Normal"]))
    story.append(Paragraph(f"Age: {patient['age']}", styles["Normal"]))
    story.append(Paragraph(f"Gender: {patient['gender']}", styles["Normal"]))

    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(Paragraph(
        f"Prediction: {patient['prediction']}",
        styles["Heading2"]
    ))

    story.append(Paragraph(
        f"Confidence: {round(patient['probability']*100,1)} %",
        styles["Heading2"]
    ))

    doc.build(story)

    return filename