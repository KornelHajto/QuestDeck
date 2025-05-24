import yaml
import os

class Config:
    def __init__(self, config_path='config.yaml'):
        self.config_path = config_path
        self.data = {}
        self.load_config()

    def load_config(self):
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Config file not found: {self.config_path}")

        with open(self.config_path, 'r') as f:
            self.data = yaml.safe_load(f)

        required = ['torrent_save_dir', 'qbittorrent_host', 'qbittorrent_port',
                    'qbittorrent_username', 'qbittorrent_password', 'mode']

        for field in required:
            if field not in self.data:
                raise ValueError(f"Missing required config field: {field}")

        if self.data['mode'] not in ['local', 'qbittorrent', 'both']:
            raise ValueError("Invalid mode value. Must be 'local', 'qbittorrent', or 'both'.")

    def __getitem__(self, key):
        return self.data.get(key)

    def get(self, key, default=None):
        return self.data.get(key, default)