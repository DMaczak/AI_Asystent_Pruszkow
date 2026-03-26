import os
from pathlib import Path
from dotenv import load_dotenv
from smolagents import CodeAgent, OpenAIServerModel, tool

load_dotenv()
if not os.getenv("OPENAI_API_KEY"):
    print("\nNie ma klucza, wprowadz klucz i uruchom ponownie")
    exit()
@tool
def czytajWT()


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

    print("Agent mysli...")
    podsumowanie = agent.run(prompt_startowy)
    print("===== Znalezione podstawowe informacje o dzialce ===== ")
    print(podsumowanie)

    while True:
        pytanie = input("\n Wpisz swoje pytanie lub wpisz 'exit' aby wyjsc")
        if pytanie.lower() in ['exit']:
            break

        odpowiedz = agent.run(pytanie)
        print("\n"+"="*60)
        print("Agent mysli...")

        print("\nODPOWIEDZ:")
        print(odpowiedz)