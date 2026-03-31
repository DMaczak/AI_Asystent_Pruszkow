import sqlite3
from datetime import datetime
from pathlib import Path

def pobierz_sciezke_bazy():
    """Zwraca ścieżkę do pliku bazy w folderze data"""
    base_dir = Path(__file__).resolve().parent
    folder_data = base_dir / "data"
    folder_data.mkdir(exist_ok=True)
    return folder_data / "historia_zapytan.db"

def inicjalizuj_baze():
    """Tworzy plik bazy i tabelę, jeśli jeszcze nie istnieją"""
    sciezka = pobierz_sciezke_bazy()
    conn = sqlite3.connect(sciezka)
    kursor = conn.cursor()
    
    kursor.execute('''
        CREATE TABLE IF NOT EXISTS historia (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_czas TEXT,
            teryt TEXT,
            pytanie TEXT,
            odpowiedz TEXT
        )
    ''')
    conn.commit()
    conn.close()

def zapisz_rozmowe(teryt, pytanie, odpowiedz):
    """Zapisuje pojedyncze pytanie i odpowiedź do bazy"""
    sciezka = pobierz_sciezke_bazy()
    conn = sqlite3.connect(sciezka)
    kursor = conn.cursor()
    
    data_czas = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    kursor.execute('''
        INSERT INTO historia (data_czas, teryt, pytanie, odpowiedz)
        VALUES (?, ?, ?, ?)
    ''', (data_czas, teryt, pytanie, str(odpowiedz)))
    
    conn.commit()
    conn.close()