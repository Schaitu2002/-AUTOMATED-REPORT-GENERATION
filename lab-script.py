# pypdf2 is used to modify and read existing pdfs but its major disadvantage is that it 
# cannot create new pdf files So we are used another python module named report lab
#  that helps us to create new pdf files and edit our heart's content on them

install the pandads lab
pip install pandas reportlab

import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
import os

def parse_reference_range(ref_range, value):
    """Determine if result is normal or abnormal."""
    try:
        if '-' in ref_range:
            low, high = map(float, ref_range.split('-'))
            return 'Normal' if low <= float(value) <= high else 'Abnormal'
        elif '<' in ref_range:
            high = float(ref_range.replace('<', ''))
            return 'Normal' if float(value) < high else 'Abnormal'
        elif '>' in ref_range:
            low = float(ref_range.replace('>', ''))
            return 'Normal' if float(value) > low else 'Abnormal'
    except:
        return 'Unknown'
    return 'Unknown'

def generate_pdf_report(patient_id, patient_data, output_dir='reports'):
    filename = f"{output_dir}/{patient_id}_{patient_data['Name'].iloc[0].replace(' ', '_')}.pdf"
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, f"Medical Lab Report")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"Patient ID: {patient_id}")
    c.drawString(50, height - 100, f"Name: {patient_data['Name'].iloc[0]}")
    c.drawString(50, height - 120, f"Age: {patient_data['Age'].iloc[0]}")

    # Table Data
    table_data = [['Test', 'Result', 'Unit', 'Reference', 'Status']]
    for _, row in patient_data.iterrows():
        status = parse_reference_range(row['ReferenceRange'], row['Result'])
        table_data.append([row['Test'], row['Result'], row['Unit'], row['ReferenceRange'], status])

    # Create Table
    t = Table(table_data, colWidths=[100, 60, 50, 100, 70])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
    ]))

    # Draw table
    t.wrapOn(c, width, height)
    t.drawOn(c, 50, height - 350)

    c.save()
    print(f"Generated report for {patient_data['Name'].iloc[0]} at {filename}")

def main():
    df = pd.read_csv('lab_results.csv')
    if not os.path.exists('reports'):
        os.makedirs('reports')

    for patient_id, group in df.groupby('PatientID'):
        generate_pdf_report(patient_id, group)

if __name__ == "__main__":
    main()
