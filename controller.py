from collections import defaultdict
import requests
from bs4 import BeautifulSoup
import folium


def get_coordinates(city_name: str) -> list:
    url = f"https://pl.wikipedia.org/wiki/{city_name}"
    try:
        response = requests.get(url).text
        soup = BeautifulSoup(response, "html.parser")
        latitude = float(soup.select(".latitude")[1].text.replace(",", "."))
        longitude = float(soup.select(".longitude")[1].text.replace(",", "."))
        return [latitude, longitude]
    except Exception as e:
        print("Błąd pobierania współrzędnych:", e)
        return [52.2, 21.0] #domyślna lokalizacja

def get_grouped_map(data: list, filename="mapa.html") -> None:
    grouped = defaultdict(list)

    for item in data:
        grouped[item['location']].append(item['name'])

    mapa = folium.Map(location=[52.21, 21.0], zoom_start=6)

    for location, names in grouped.items():
        coord = get_coordinates(location)

        #  WAŻNA LOKALIZACJA – TU DODAJ IMIONA I LOKALIZACJE DO POPUPA
        popup_text = f"<b>{location}</b><br>" + "<br>".join(["• " + name for name in names]) #  lista klientów
        tooltip_text = ", ".join(names)  # na podgląd

        folium.Marker(
            location=coord,
            popup=popup_text,
            tooltip=tooltip_text
        ).add_to(mapa)

    mapa.save(filename)

