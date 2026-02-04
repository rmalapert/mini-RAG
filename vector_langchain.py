from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import AzureOpenAIEmbeddings
import os
from dotenv import load_dotenv
from pdf_loader import load_pdf_with_fallback_ocr


load_dotenv()

MAJ_VS = False
PDF_FOLDER = "data/pdf"
DB_DIR = "vectorstore_db"
#PDF_FOLDER = "data/pdf test"
#DB_DIR = "vectorstore_db_test"

COLLECTION_NAME = "slide_knowledge"

embedding = AzureOpenAIEmbeddings(
    api_key=os.getenv("OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    azure_deployment=os.getenv("DEPLOYMENT_NAME_EMBEDDING"),
    api_version=os.getenv("OPENAI_API_VERSION"),
)

# Initialisation de la base vectorielle
vector_store = Chroma(
    collection_name=COLLECTION_NAME,
    persist_directory=DB_DIR,
    embedding_function=embedding
)

# Indexation si la base n'existe pas encore
if MAJ_VS or not os.path.exists(DB_DIR) or not os.listdir(DB_DIR):
    documents = []
    for pdf_name in os.listdir(PDF_FOLDER):
        if pdf_name.endswith(".pdf"):
            #loader = PyPDFLoader(os.path.join(PDF_FOLDER, pdf_name))
            #docs = loader.load()
            pdf_path = os.path.join(PDF_FOLDER, pdf_name)
            docs = load_pdf_with_fallback_ocr(pdf_path)

            # for doc in docs:
            #     print("\n=== Page ===")
            #     print(doc.page_content[:500])  # affiche les 500 premiers caractères de chaque page
                
            splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            documents += splitter.split_documents(docs)

    vector_store.add_documents(documents)
    vector_store.persist()

retriever = vector_store.as_retriever(search_type="mmr", search_kwargs = {"k": 5})




