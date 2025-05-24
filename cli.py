import requests
from bs4 import BeautifulSoup

def search_fitgirl(query):
    base_url = "https://fitgirl-repacks.site/?s="
    search_url = base_url + query.replace(" ", "+")

    response = requests.get(search_url)
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

def main():
    query = input("Enter the game you want to search for: ")
    games = search_fitgirl(query)

    if not games:
        print("No results found.")
        return

    print("\nSearch results:")
    for i, game in enumerate(games, start=1):
        print(f"{i}. {game['title']}")

    choice = input("\nEnter the number of the game you want the link for (or 'q' to quit): ")

    if choice.lower() == 'q':
        print("Exiting.")
        return

    try:
        choice_num = int(choice)
        if 1 <= choice_num <= len(games):
            selected_game = games[choice_num - 1]
            print(f"\nYou selected:\nTitle: {selected_game['title']}\nLink: {selected_game['link']}")
        else:
            print("Invalid number chosen.")
    except ValueError:
        print("Please enter a valid number.")

if __name__ == "__main__":
    main()
