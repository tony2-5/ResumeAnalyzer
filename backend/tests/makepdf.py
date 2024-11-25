from fpdf import FPDF

def create_sample_pdf(file_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="This is a sample PDF file.", ln=True, align="C")
    pdf.output(file_path)

# 生成 sample.pdf
create_sample_pdf("sample.pdf")
