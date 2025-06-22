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

