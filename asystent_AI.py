import os
from pathlib import Path
from dotenv import load_dotenv
from smolagents import CodeAgent, OpenAIServerModel, tool
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from baza_zapytan import inicjalizuj_baze, zapisz_rozmowe

load_dotenv()
if not os.getenv("OPENAI_API_KEY"):
    print("\nNie ma klucza, wprowadz klucz i uruchom ponownie")
    exit()

@tool
def czytajWT(zapytanie: str) -> str:
    """
    To narzędzie przeszukuje ogólnopolskie Prawo Budowlane.
    
    ZASADY UŻYCIA:
    1. Używaj tego ZAWSZE do spraw technicznych, których zazwyczaj NIE MA w MPZP, takich jak:
       - odległość budynku od granicy działki (z oknami i bez),
       - minimalne wymiary schodów, drzwi, okien,
       - zasady dotyczące instalacji, miejsc parkingowych, czy ppoż.
    2. Pamiętaj: Jeśli informacje stąd przeczą ustaleniom z narzędzia 'czytajMPZP' 
       zawsze wybieraj te z czytajMPZP
    
    Args:
        zapytanie: Konkretne hasło do wyszukania, np. "odległość budynku od granicy", "szerokość schodów"
    """
    print("Agent przeszukuje baze")
    
    base_dir = Path(__file__).resolve().parent
    folder_bazy = base_dir / "data" / "baza_chroma"
    
    if not folder_bazy.exists():
        return "Baza nie istnieje."
        
    try:
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        baza = Chroma(persist_directory=str(folder_bazy), embedding_function=embeddings)
        wyniki = baza.similarity_search(zapytanie, k=3)
        
        if not wyniki:
            return "Nie znaleziono w Prawie Budowlanym informacji na ten temat."
            
        odpowiedz = "Oto najważniejsze fragmenty z Prawa Budowlanego (Warunków Technicznych):\n\n"
        for i, doc in enumerate(wyniki):
            odpowiedz += f"--- Fragment {i+1} ---\n{doc.page_content}\n\n"
            
        return odpowiedz
        
    except Exception as e:
        return f"Wystąpił błąd podczas przeszukiwania bazy: {e}"
    
@tool
def czytajMPZP(teryt:str) -> str:

    """
    To narzędzie czyta ustalenia Miejscowego Planu Zagospodarowania (MPZP) dla podanej działki.
    Zwraca cały tekst planu miejscowego.
    
    Args:
        teryt: Numer TERYT działki, np. '142102_1.0019.482/51'
    """

    base_dir = Path(__file__).resolve().parent
    nazwa_pliku = f"mpzp_{teryt.replace('.', '_').replace('/', '_')}.txt"
    sciezka_pliku = base_dir / "data" / nazwa_pliku

    if not sciezka_pliku.exists():
        return f"Błąd: Nie znaleziono pliku {nazwa_pliku}."
        
    return sciezka_pliku.read_text(encoding="utf-8")

model = OpenAIServerModel(model_id="?????")
agent = CodeAgent(tools=[czytajMPZP, czytajWT], model=model, add_base_tools=False)

def uruchomChat(teryt):

    inicjalizuj_baze()

    print("\n"+"="*60)
    print("========= WYSZUKIWANIE INFORMACJI PROSZE CZEKAC... =========")
    print("\n"+"="*60)

    prompt_startowy = f"""
    Użyj narzędzia czytajMPZP dla teryt: {teryt}. 
    Następnie wypisz w bardzo krótkich, zwięzłych słowach (w punktach) 
    najważniejsze parametry dla tej działki:
    1. Główne przeznaczenie terenu.
    2. Maksymalna wysokość zabudowy.
    3. Minimalny wskaźnik powierzchni biologicznie czynnej.
    Jeśli jakiejś informacji nie ma, napisz 'Brak danych'
    """

    print("Agent myśli...")
    podsumowanie = agent.run(prompt_startowy)
    print("===== Znalezione podstawowe informacje o dzialce ===== ")
    print(podsumowanie)
    
    zapisz_rozmowe(teryt, "Autogeneracja: Podsumowanie działki", podsumowanie)

    while True:
        pytanie = input("\n👤 Wpisz swoje pytanie lub wpisz 'exit' aby wyjść: ")
        if pytanie.lower() in ['exit', 'wyjscie', 'quit']:
            break
            
        if not pytanie.strip():
            continue

        print("\n🤖 Agent myśli...")
        odpowiedz = agent.run(pytanie)
        
        print("\n" + "="*60)
        print("ODPOWIEDŹ: ")
        print(odpowiedz)
        print("="*60)
        zapisz_rozmowe(teryt, pytanie, odpowiedz)