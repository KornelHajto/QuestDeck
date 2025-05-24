import httpx
from bs4 import BeautifulSoup

async def search_fitgirl(query):
    base_url = "https://fitgirl-repacks.site/?s="
    search_url = base_url + query.replace(" ", "+")

    print(f"Searching FitGirl for: {query}")
    async with httpx.AsyncClient() as client:
        response = await client.get(search_url)

    if response.status_code != 200:
        print("Failed to retrieve search results")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('article', class_='post')

    results = []
    for article in articles:
        title_tag = article.find('h1', class_='entry-title')
        if not title_tag:
            continue

        link_tag = title_tag.find('a')
        if not link_tag:
            continue

        title = link_tag.text.strip()
        link = link_tag['href']

        results.append({'title': title, 'link': link})

    return results
