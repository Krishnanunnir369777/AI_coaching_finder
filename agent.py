from openstreetmap import search_coaching_centers


def parse_user_query(query: str):
    """
    Expected format:
    'JEE coaching in Patna'
    """
    query = query.strip().lower()

    if "coaching in" not in query:
        raise ValueError("Use format: <exam> coaching in <city>")

    exam, city = query.split("coaching in")
    return {
        "exam": exam.strip().upper(),
        "city": city.strip().title()
    }


def run_agent(user_query: str):
    parsed = parse_user_query(user_query)
    return search_coaching_centers(parsed["city"], parsed["exam"])
