from PyPDF2 import PdfReader, PdfWriter
 
 
def extract_pdf_pages(input_pdf_path, output_pdf_path, pages_to_keep):
    """
    Extrait certaines pages d'un fichier PDF (1-based indexing).
    """
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()
 
    for page_num in pages_to_keep:
        if 1 <= page_num <= len(reader.pages):
            writer.add_page(reader.pages[page_num - 1])
 
    with open(output_pdf_path, "wb") as output_pdf:
        writer.write(output_pdf)
 
    return output_pdf_path
 
 
if __name__ == "__main__":
    pdf_file = "tests/pdf/Europ_Assistance.pdf"
    for i in range(19, 23):
        output_pdf = f"pager{i-18}.pdf"
 
        pages = [i] # numéro de la page à extraire
        extract_pdf_pages(pdf_file, output_pdf, pages)