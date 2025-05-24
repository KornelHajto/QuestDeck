from tools.search import search_fitgirl

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
