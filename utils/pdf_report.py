# Manav — Secure PDF Generator
# FPDF2 wrapper. Streamlit expects bytearrays for the download button.

from fpdf import FPDF

def generate_pdf_report(session_summary: str) -> bytes:
    """
    Generates a minimalist PDF report of the session.
    Strips away unsupported unicodes (like emojis/Punjabi) automatically.
    """
    pdf = FPDF()
    pdf.add_page()
    
    # Header styling
    pdf.set_font("Helvetica", size=18, style='B')
    pdf.set_text_color(19, 136, 8)  # Indian tricolor green touch
    
    # FPDF2 syntax for new lines:
    pdf.cell(w=0, h=12, text="MindMitra Wellbeing Report", new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.ln(8)
    
    # Body text
    pdf.set_font("Helvetica", size=11)
    pdf.set_text_color(40, 40, 40)
    
    # ── CRITICAL FIX ──
    # FPDF's default font doesn't have glyphs for Hindi/Punjabi or Emojis.
    # We encode to latin-1 and replace unknown chars with '?' to prevent UnicodeEncodeError crash.
    safe_text = session_summary.encode('latin-1', 'replace').decode('latin-1')
    
    pdf.multi_cell(w=0, h=8, text=safe_text)
    
    # Output byte array for Streamlit's st.download_button
    return bytes(pdf.output())
