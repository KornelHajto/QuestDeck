# QuestDeck

A CLI-based automation tool for managing game downloads via torrents. It scrapes selected sources for game entries, fetches the corresponding .torrent files, and — if configured — sends them directly to a running qBittorrent instance using its Web API. Otherwise, it stores the .torrent files locally for manual use. Designed to be fast, minimal, and highly scriptable, this tool simplifies the process of tracking and fetching new game repacks.

## Features

- Search for games directly from the command line
- Automatically extract torrent links from game pages
- Download .torrent files in headless mode (no browser window needed)
- Store torrents locally for manual management
- Integrate with qBittorrent Web API for automatic torrent addition
- Configurable to work in local-only, qBittorrent-only, or both modes

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/QuestDeck.git
   cd QuestDeck[config.yaml](config.yaml)
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Ensure Firefox is installed (required for Selenium)

5. Download the appropriate geckodriver for your system:
   - Visit: https://github.com/mozilla/geckodriver/releases
   - Place the geckodriver executable in your PATH or in the project directory

## Configuration

1. Copy the example configuration file:
   ```
   cp config.yaml.example config.yaml
   ```

2. Edit `config.yaml` with your settings:
   ```yaml
   torrent_save_dir: ./torrents  # Directory to save torrent files
   qbittorrent_host: http://localhost  # qBittorrent Web UI host
   qbittorrent_port: 8080  # qBittorrent Web UI port
   qbittorrent_username: admin  # qBittorrent Web UI username
   qbittorrent_password: adminadmin  # qBittorrent Web UI password
   mode: both  # 'local', 'qbittorrent', or 'both'
   ```

## Usage

Run the CLI tool:
```
python3 main.py
```

## Wiki and Documentation
For comprehensive documentation including:


Advanced configuration options
Contribution guidelines
Visit the wiki: https://git.kornelhajto.xyz/kornelhajto/QuestDeck/wiki