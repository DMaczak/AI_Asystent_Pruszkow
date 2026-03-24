from pobierz_warunki_techniczne import pobierz_warunki_techniczne
from adres_do_tetryt import adres_na_wspolrzedne, wspolrzedne_na_teryt
from mpzp_scraper import pobierz_ustalenia_mpzp

def main():
    print("="*60)
    print("========= ASYSTENT PRAWA BUDOWLANEGO DLA PRUSZKOWA =========")
    print("="*60)
    print("Sprawdzanie plikow źródłowych...")

    pobierz_warunki_techniczne()

    adres_input = input("\nPodaj ulice i numer dzialki w Pruszkowie np. Boleslawa Prusa 14 => ")
    adres = f"Pruszkow, {adres_input}"

    lat, lon = adres_na_wspolrzedne(adres)
    
    if lat and lon:

        teryt = wspolrzedne_na_teryt(lat, lon)

        if teryt:
            print(f"\n Numer TERYT dzialki to: {teryt}")

            print("\nPróbuję pobrać ustalenia MPZP z serwera...")
            wynik_mpzp = pobierz_ustalenia_mpzp(teryt)
            
            if "błąd" in wynik_mpzp.lower() or "nie znaleziono" in wynik_mpzp.lower():
                print(f"Coś poszło nie tak: {wynik_mpzp}")
            else:
                print("\n POBRANO WYNIK ANALIZY MPZP I ZAPISANO DO PLIKU ")
               

        else:
            print("\n Nie udalo sie ustalic numeru TERYT. Nie ma takiej dzialki")
    else:
        print("\n Nie udalo się znalezc wspolrzednych dla tego adresu")
"""
URUCHOMIENIE PROGRAMU
"""

if __name__ == "__main__":
    main()