import requests
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

def search_coaching_centers(city, exam, limit=10):
    query = f"{exam} coaching center in {city}"

    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": query,
        "key": GOOGLE_API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    print("GOOGLE MAPS STATUS:", data.get("status"))
    print("GOOGLE MAPS MESSAGE:", data.get("error_message"))
    print("TOTAL RESULTS:", len(data.get("results", [])))

    results = []

    for place in data.get("results", [])[:limit]:
        place_id = place["place_id"]

        results.append({
            "name": place.get("name"),
            "owner": "Not Available",
            "phone": "Not Available",
            "address": place.get("formatted_address"),
            "maps_link": f"https://www.google.com/maps/place/?q=place_id:{place_id}",
            "source_url": "Google Maps"
        })

    return results