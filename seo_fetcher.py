import random

def fetch_seo_data(keyword):
    """
    Given a keyword, return fake SEO metrics.
    """
    # Mock search volume between 1,000 to 50,000
    search_volume = random.randint(1000, 50000)

    # Mock difficulty score (0 to 100)
    keyword_difficulty = random.randint(10, 80)

    # Mock cost-per-click value
    avg_cpc = round(random.uniform(0.5, 5.0), 2)
    avg_cpc_str = f"${avg_cpc}"

    return {
        "search_volume": search_volume,
        "keyword_difficulty": keyword_difficulty,
        "avg_cpc": avg_cpc_str
    }