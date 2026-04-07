# Sinamor
from fpdf import FPDF

def generate_pdf_report(session_summary):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=16, style='B')
    pdf.cell(200, 10, text="MindMitra - Mental Health Report", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", size=12)
    # FPDF default font doesn't support unicode (Punjabi/Emojis), so we replace them
    safe_summary = session_summary.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 10, text=safe_summary)
    
    # We use bytearray which is compatible with streamlit download button
    return pdf.output()
