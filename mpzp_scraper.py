import requests
from bs4 import BeautifulSoup
from pathlib import Path

def pobierz_ustalenia_mpzp(teryt):
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    url_dzialki = f"https://uldk.gugik.gov.pl/dzinfo.php?dzialka={teryt}"
    
    try:
        print(f"Szukam informacji dla działki: {teryt}...")
        response = requests.get(url=url_dzialki, headers=headers, timeout=10)
        response.raise_for_status() 
        
        soup = BeautifulSoup(response.text, 'html.parser')

        link_ustalenia = None
        for a_tag in soup.find_all('a', href=True):
            if 'getUstaleniaSzczegolowe' in a_tag['href']:
                link_ustalenia = a_tag['href']
                break
        
        if not link_ustalenia:
            return "Nie znaleziono ustaleń MPZP dla tej działki"
            
        print(f"Znaleziono link do szczegółów MPZP => Pobieram treść...")

        mpzp_response = requests.get(url=link_ustalenia, headers=headers, timeout=10)
        mpzp_response.raise_for_status()

        mpzp_response.encoding = 'utf-8' 
        mpzp_soup = BeautifulSoup(mpzp_response.text, 'html.parser')

        czysty_tekst = mpzp_soup.get_text(separator='\n', strip=True)

        base_dir = Path(__file__).resolve().parent
        folder_data = base_dir / "data"
        folder_data.mkdir(exist_ok=True)
        
        nazwa_pliku = f"mpzp_{teryt.replace('.', '_').replace('/', '_')}.txt"
        sciezka_zapisu = folder_data / nazwa_pliku
        
        sciezka_zapisu.write_text(czysty_tekst, encoding="utf-8")
        
        return czysty_tekst
        
    except requests.exceptions.RequestException as e:
        return f"Błąd sieci podczas pobierania danych: {e}"
    except Exception as e:
        return f"Wystąpił nieoczekiwany błąd: {e}"
    
    