import os
import requests
from pathlib import Path

def pobierz_warunki_techniczne():
    
    url_pdf = "https://isap.sejm.gov.pl/isap.nsf/download.xsp/WDU20220001225/O/D20221225.pdf"
    
    base_dir = Path(__file__).resolve().parent
    folder_docelowy = base_dir / "data" / "raw"
    sciezka_zapisu = folder_docelowy / "wt.pdf"
    folder_docelowy.mkdir(parents=True, exist_ok=True)

    if  sciezka_zapisu.exists():
        print(f"Plik {sciezka_zapisu} już istnieje")
        return
        
    print("Pobieranie Warunków Technicznych...")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url=url_pdf, headers=headers, stream=True, timeout=15)
        response.raise_for_status() 

        with open(sciezka_zapisu, 'wb') as plik:
            for chunk in response.iter_content(chunk_size=8192):
                plik.write(chunk)
                
        print(f"OK. Pomyslnie pobrano prawo budowlane")
        
    except requests.exceptions.RequestException as e:
        print(f"Wystapil blad {e}")