import streamlit as st
import io
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from app import pdf_to_json,extract,pdf_to_template
st.title("PDF TO TEMPALATE")
file = st.file_uploader("Upload your PDF", type="pdf")
resume = None  
if file:
    st.success("PDF uploaded successfully!")
    pdf_bytes = file.read()
    text = extract(pdf_bytes)
    st.subheader("Preview of Extracted Text")
    st.write(text[:800] + ("..." if len(text) > 800 else ""))
    if st.button("Convert to JSON with Groq"):
        
            try:
                json = pdf_to_json(pdf_bytes)
                st.subheader("JSON Output")
                st.json(json)
            except Exception as e:
                st.error(f"Error: {e}")
    style = st.selectbox(
        "Choose Template",
        ["modern", "minimal", "classic"]
    )
    if st.button("Generate Resume Template"):
        
            try:
                resume = pdf_to_template(pdf_bytes, style)
                st.subheader(f"Resume ({style.capitalize()} Style)")
                st.markdown(resume)
            except Exception as e:
                st.error(f"Error: {e}")
    def save(resume_text: str) -> bytes:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer)
        styles = getSampleStyleSheet()
        story = [
            Paragraph(line, styles["Normal"])
            for line in resume_text.split("\n") if line.strip()
        ]
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
    if resume and st.button("Download Resume as PDF"):
        pdf_bytes_out = save(resume)
        st.download_button(
            label=" Download Resume (PDF)",
            data=pdf_bytes_out,
            file_name="resume.pdf",
            mime="application/pdf"
        )
