import requests

def adres_na_wspolrzedne(adres):
    
    print(f"Szukam wspolrzednych dla adresu: {adres}...")
    url_nom = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': adres,
        'format': 'json',
        'limit': 1
    }
    headers = {
        'User-Agent': 'AsystentPrawaBudowlanego_PoC_Pruszkow'
    }
    
    try:
        response = requests.get(url=url_nom, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        dane = response.json()
        
        if not dane:
            print("Nie znaleziono adresu w bazie OpenStreetMap.")
            return None, None
            
        lat = dane[0]['lat']
        lon = dane[0]['lon']
        print(f"Znaleziono punkt GPS: Szer:{lat}, Dług:{lon}")
        return lat, lon
    
    except Exception as e:
        print(f"Blad podczas wyszukiwania adresu: {e}")
        return None, None

def wspolrzedne_na_teryt(lat, lon):
    
    print("Sprawdzam jaka to dzialka w GUGiK...")
    url_uldk = f"https://uldk.gugik.gov.pl/?request=GetParcelByXY&xy={lon},{lat},4326&result=id"
    
    try:
        response = requests.get(url=url_uldk, timeout=10)
        response.raise_for_status()
        linie = response.text.strip().split('\n')
        
        if len(linie) >= 2 and linie[0] == '0':
            teryt = linie[1].strip()
            print(f"Znaleziono działke. Numer TERYT: {teryt}")
            return teryt
        else:
            print("GUGiK nie znalazl dzialki w tym miejscu")
            return None
            
    except Exception as e:
        print(f"Blad podczas odpytywania GUGiK: {e}")
        return None
    