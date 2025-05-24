from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, IntPrompt
from rich.markdown import Markdown

import asyncio
from tools.search.fitgirl import search_fitgirl
from tools.torrent.handler import extract_torrent_page_link, download_torrent_with_selenium

console = Console()

async def run_cli():
    console.print("[bold cyan]Welcome to the QuestDeck! 🎮[/bold cyan]\n")

    query = Prompt.ask("Enter the game you want to search for")
    games = await search_fitgirl(query)

    if not games:
        console.print("[bold red]No results found.[/bold red]")
        return

    table = Table(title="Search results", show_lines=True)
    table.add_column("#", justify="right", style="bold magenta")
    table.add_column("Game Title", style="bold green")

    for i, game in enumerate(games, start=1):
        table.add_row(str(i), game['title'])

    console.print(table)

    choice = Prompt.ask("\nEnter the number of the game you want the .torrent file for (or 'q' to quit)")

    if choice.lower() == 'q':
        console.print("[yellow]Exiting...[/yellow]")
        return

    try:
        choice_num = int(choice)
        if 1 <= choice_num <= len(games):
            selected_game = games[choice_num - 1]
            console.print(f"\n[bold]You selected:[/bold] {selected_game['title']}")
            console.print(f"[bold]Page link:[/bold] {selected_game['link']}")

            paste_url = extract_torrent_page_link(selected_game['link'])

            if paste_url:
                console.print(f"[bold green]Found paste URL:[/bold green] {paste_url}")
                console.print("[bold]Downloading .torrent file via Selenium...[/bold]")
                download_torrent_with_selenium(paste_url)
                console.print("[bold green]Download process completed![/bold green]")
            else:
                console.print("[bold red]Could not find .torrent file link on page.[/bold red]")

        else:
            console.print("[bold red]Invalid number chosen.[/bold red]")
    except ValueError:
        console.print("[bold red]Please enter a valid number.[/bold red]")


if __name__ == "__main__":
    asyncio.run(run_cli())