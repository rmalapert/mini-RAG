from langchain_community.document_loaders import PyPDFLoader
from langchain.schema import Document
import fitz  # PyMuPDF
import io
from PIL import Image
import numpy as np
import easyocr

reader = easyocr.Reader(['fr'], gpu=False)  # Initialise une seule fois

def load_pdf_with_fallback_ocr(pdf_path: str, text_threshold: int = 30) -> list[Document]:
    print(f"Chargement de : {pdf_path}")

    # 1. Essai PyPDFLoader
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    total_text = "".join([doc.page_content for doc in docs]).strip()
    if len(total_text) >= text_threshold:
        print("✅ Texte extrait avec PyPDFLoader.")
        return docs

    # 2. OCR avec EasyOCR via PyMuPDF
    print("⚠️ Texte insuffisant. Passage à l’OCR avec EasyOCR...")
    ocr_docs = []
    pdf = fitz.open(pdf_path)

    for i in range(len(pdf)):
        page = pdf.load_page(i)
        pix = page.get_pixmap(dpi=300)
        img_bytes = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_bytes))

        # EasyOCR prend des fichiers ou des tableaux numpy
        img_np = np.array(img)  # Convertit l’image PIL en array numpy
        result = reader.readtext(img_np, detail=0, paragraph=True)
        text = "\n".join(result).strip()

        if text:
            ocr_docs.append(Document(page_content=text, metadata={"page": i + 1}))

    print(f"✅ OCR effectué avec EasyOCR. {len(ocr_docs)} pages extraites.")
    return ocr_docs

# def load_pdf_with_fallback_ocr(pdf_path, text_threshold):
#     print(f"Chargement de : {pdf_path}")
#     filename = os.path.basename(pdf_path)  # Récupère juste le nom du fichier (ex: mondoc.pdf)

#     # 1. Essai PyPDFLoader
#     loader = PyPDFLoader(pdf_path)
#     docs = loader.load()

#     # Ajout du nom de fichier dans les métadonnées
#     for doc in docs:
#         doc.metadata["source"] = filename

#     total_text = "".join([doc.page_content for doc in docs]).strip()
#     if len(total_text) >= text_threshold:
#         print("✅ Texte extrait avec PyPDFLoader.")
#         return docs

#     # 2. OCR avec EasyOCR via PyMuPDF
#     print("⚠️ Texte insuffisant. Passage à l’OCR avec EasyOCR...")
#     ocr_docs = []
#     pdf = fitz.open(pdf_path)

#     for i in range(len(pdf)):
#         page = pdf.load_page(i)
#         pix = page.get_pixmap(dpi=300)
#         img_bytes = pix.tobytes("png")
#         img = Image.open(io.BytesIO(img_bytes))

#         # EasyOCR prend des fichiers ou des tableaux numpy
#         img_np = np.array(img)
#         result = reader.readtext(img_np, detail=0, paragraph=True)
#         text = "\n".join(result).strip()

#         if text:
#             ocr_docs.append(Document(
#                 page_content=text,
#                 metadata={"page": i + 1, "source": filename}  # ➕ Ajout du nom du fichier ici aussi
#             ))

#     print(f"✅ OCR effectué avec EasyOCR. {len(ocr_docs)} pages extraites.")
#     return ocr_docs
