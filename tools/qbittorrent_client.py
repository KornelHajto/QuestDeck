import os
import requests
import logging
from urllib.parse import urljoin

logger = logging.getLogger(__name__)

class QBittorrentClient:
    def __init__(self, config):
        self.host = config.get('qbittorrent_host')
        self.port = config.get('qbittorrent_port')
        self.username = config.get('qbittorrent_username')
        self.password = config.get('qbittorrent_password')
        
        if self.host.endswith('/'):
            self.host = self.host[:-1]
            
        self.base_url = f"{self.host}:{self.port}"
        self.session = requests.Session()
        self.is_authenticated = False
    
    def authenticate(self):
        try:
            login_url = urljoin(self.base_url, "/api/v2/auth/login")
            response = self.session.post(
                login_url,
                data={"username": self.username, "password": self.password}
            )
            
            if response.status_code == 200 and response.text == "Ok.":
                self.is_authenticated = True
                logger.info("Successfully authenticated with qBittorrent")
                print("Successfully authenticated with qBittorrent")
                return True
            else:
                logger.error(f"Failed to authenticate with qBittorrent: {response.text}")
                print(f"Failed to authenticate with qBittorrent: {response.text}")
                return False
                
        except requests.RequestException as e:
            logger.error(f"Connection error when authenticating to qBittorrent: {str(e)}")
            print(f"Connection error when authenticating to qBittorrent: {str(e)}")
            return False
    
    def add_torrent(self, torrent_file_path):
        if not self.is_authenticated and not self.authenticate():
            return False
            
        try:
            add_url = urljoin(self.base_url, "/api/v2/torrents/add")
            
            if not os.path.exists(torrent_file_path):
                logger.error(f"Torrent file not found: {torrent_file_path}")
                print(f"Torrent file not found: {torrent_file_path}")
                return False
                
            with open(torrent_file_path, 'rb') as f:
                files = {'torrents': f}
                response = self.session.post(add_url, files=files)
                
            if response.status_code == 200 and response.text == "Ok.":
                logger.info(f"Successfully added torrent to qBittorrent: {os.path.basename(torrent_file_path)}")
                print(f"Successfully added torrent to qBittorrent: {os.path.basename(torrent_file_path)}")
                return True
            else:
                logger.error(f"Failed to add torrent to qBittorrent: {response.text}")
                print(f"Failed to add torrent to qBittorrent: {response.text}")
                return False
                
        except requests.RequestException as e:
            logger.error(f"Connection error when adding torrent to qBittorrent: {str(e)}")
            print(f"Connection error when adding torrent to qBittorrent: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Error adding torrent to qBittorrent: {str(e)}")
            print(f"Error adding torrent to qBittorrent: {str(e)}")
            return False
    
    def check_connection(self):
        try:
            print(f"Attempting to connect to qBittorrent at {self.base_url}")
            version_url = urljoin(self.base_url, "/api/v2/app/version")
            
            print(f"Sending request to: {version_url}")
            response = self.session.get(version_url, timeout=5)
            
            print(f"Response status code: {response.status_code}")
            print(f"Response text: {response.text}")
            
            if response.status_code == 200:
                logger.info(f"Successfully connected to qBittorrent version: {response.text}")
                print(f"Successfully connected to qBittorrent version: {response.text}")
                return True
            elif response.status_code == 403:
                logger.error(f"Connection forbidden. You need to authenticate first.")
                print(f"Connection forbidden. You need to authenticate first.")
                
                if self.authenticate():
                    return self.check_connection()
                return False
            else:
                logger.error(f"Failed to connect to qBittorrent: {response.text}")
                print(f"Failed to connect to qBittorrent: {response.text}")
                return False
                
        except requests.RequestException as e:
            logger.error(f"Connection error when checking qBittorrent: {str(e)}")
            print(f"Connection error when checking qBittorrent: {str(e)}")
            return False