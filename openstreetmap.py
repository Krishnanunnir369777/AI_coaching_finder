import requests
import time

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
OVERPASS_URL = "https://overpass-api.de/api/interpreter"

HEADERS = {
    "User-Agent": "AI-Coaching-Institute-Finder/1.0 (Educational Project)"
}


def get_city_coordinates(city):
    params = {
        "q": city,
        "format": "json",
        "limit": 1
    }

    response = requests.get(NOMINATIM_URL, params=params, headers=HEADERS, timeout=20)
    response.raise_for_status()
    data = response.json()

    if not data:
        raise ValueError("City not found")

    return float(data[0]["lat"]), float(data[0]["lon"])


def search_coaching_centers(city, exam, limit=10):
    try:
        lat, lon = get_city_coordinates(city)
        time.sleep(1)

        query = f"""
        [out:json][timeout:25];
        (
          node["name"](around:12000,{lat},{lon});
          way["name"](around:12000,{lat},{lon});
        );
        out center;
        """

        response = requests.post(
            OVERPASS_URL,
            data=query,
            headers=HEADERS,
            timeout=30
        )

        if response.status_code != 200:
            return []

        data = response.json()
        results = []

        education_keywords = [
            "coaching", "classes", "academy", "institute",
            "tuition", "tutorial", "iit", "jee", "neet", "entrance"
        ]

        bad_keywords = [
            "hospital", "clinic", "blood", "doctor",
            "health", "medical", "diagnostic", "nursing"
        ]

        for el in data.get("elements", []):
            tags = el.get("tags", {})
            name = tags.get("name", "")

            name_lower = name.lower()

            if (
                exam.lower() in name_lower
                and any(k in name_lower for k in education_keywords)
                and not any(b in name_lower for b in bad_keywords)
            ):
                lat2 = el.get("lat") or el.get("center", {}).get("lat")
                lon2 = el.get("lon") or el.get("center", {}).get("lon")

                results.append({
                    "name": name,
                    "owner": "Not Available",
                    "phone": tags.get("phone", "Not Available"),
                    "address": tags.get("addr:full", "Not Available"),
                    "maps_link": f"https://www.openstreetmap.org/?mlat={lat2}&mlon={lon2}",
                    "source_url": "OpenStreetMap"
                })

                if len(results) >= limit:
                    break

        return results

    except Exception as e:
        print("OSM ERROR:", e)
        return []
