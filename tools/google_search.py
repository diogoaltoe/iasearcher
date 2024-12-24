from langchain_google_community import GoogleSearchAPIWrapper


def search_country_wikipedia(name: str):
    """Searches for country page on Wikipedia"""
    search = GoogleSearchAPIWrapper()

    query = name + " Wikipedia page"
    return search.results(query=query, num_results=5)
