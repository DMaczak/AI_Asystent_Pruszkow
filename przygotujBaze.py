import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()
if not os.getenv("OPENAI_API_KEY"):
    print("Brak klucza AI")
    exit()

def stworz_baze_wektorowa():
    print("="*60)
    print("Rozpoczynam budowanie bazy")
    print("="*60)

    base_dir = Path(__file__).resolve().parent
    sciezka_pdf = base_dir / "data" / "raw" / "wt.pdf"
    folder_bazy = base_dir / "data" / "baza_chroma"

    if not sciezka_pdf.exists():
        print("Nie ma pliku z warunkami technicznymi")
        return

    print("Wczytywanie dokumentu PDF...")
    loader = PyPDFLoader(str(sciezka_pdf))
    strony = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,    
        chunk_overlap=200,  
        separators=["\n\n", "\n", " ", ""]
    )
    kawaliki_tekstu = text_splitter.split_documents(strony)
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small") 
    
    baza_chroma = Chroma.from_documents(
        documents=kawaliki_tekstu,
        embedding=embeddings,
        persist_directory=str(folder_bazy)
    )   
    print("\nBaza została utworzona")