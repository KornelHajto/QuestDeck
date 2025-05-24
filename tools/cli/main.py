import asyncio
from tools.search.fitgirl import search_fitgirl
from tools.torrent.handler import extract_torrent_page_link, download_torrent_with_selenium

async def run_cli():
    query = input("Enter the game you want to search for: ")
    games = await search_fitgirl(query)

    if not games:
        print("No results found.")
        return

    print("\nSearch results:")
    for i, game in enumerate(games, start=1):
        print(f"{i}. {game['title']}")

    choice = input("\nEnter the number of the game you want the .torrent file for (or 'q' to quit): ")

    if choice.lower() == 'q':
        print("Exiting.")
        return

    try:
        choice_num = int(choice)
        if 1 <= choice_num <= len(games):
            selected_game = games[choice_num - 1]
            print(f"\nYou selected:\n{selected_game['title']}")
            print(f"Page link: {selected_game['link']}")

            paste_url = extract_torrent_page_link(selected_game['link'])

            if paste_url:
                print(f"Found paste URL:\n{paste_url}")
                print("Downloading .torrent file via Selenium...")
                download_torrent_with_selenium(paste_url)
            else:
                print("Could not find .torrent file link on page.")

        else:
            print("Invalid number chosen.")
    except ValueError:
        print("Please enter a valid number.")

if __name__ == "__main__":
    asyncio.run(run_cli())