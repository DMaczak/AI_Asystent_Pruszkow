import os
from pathlib import Path
from dotenv import load_dotenv
from smolagents import CodeAgent, OpenAIServerModel, tool

@tool
def czytajMPZP(tetryt:str) -> str:

    base_dir = Path(__file__).resolve().parent
    nazwa_pliku = f"mpzp_{tetryt.replace('.', '_').replace('/', '_')}.txt"
    sciezka_pliku = base_dir / "data" / nazwa_pliku

    if not sciezka_pliku.exists():
        return f"Błąd: Nie znaleziono pliku {nazwa_pliku}."
        
    return sciezka_pliku.read_text(encoding="utf-8")

model = OpenAIServerModel(model_id="gpt-4o-mini")
agent = CodeAgent(tools=[czytajMPZP], model=model, add_base_tools=False)

def uruchomChat(teryt):

    print("\n"+"="*60)
    print("========= WYSZUKIWANIE INFORMACJI PROSZE CZEKAC... =========")
    print("\n"+"="*60)

    prompt_startowy = f"""
    Użyj narzędzia czytaj_plik_mpzp dla teryt: {teryt}. 
    Następnie wypisz w bardzo krótkich, zwięzłych słowach (w punktach) 
    najważniejsze parametry dla tej działki:
    1. Główne przeznaczenie terenu.
    2. Maksymalna wysokość zabudowy.
    3. Minimalny wskaźnik powierzchni biologicznie czynnej.
    Jeśli jakiejś informacji nie ma, napisz 'Brak danych'
    """
    

