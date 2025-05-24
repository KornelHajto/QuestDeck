from .config import Config
import os
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import requests
from bs4 import BeautifulSoup

config = Config()

def extract_torrent_page_link(game_url):
    try:
        response = requests.get(game_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            torrent_links = soup.find_all('a', string=lambda text: text and ".torrent file only" in text)
            
            if torrent_links:
                return torrent_links[0]['href']
            
            torrent_links = soup.find_all('a', href=lambda href: href and "paste.fitgirl-repacks.site" in href)
            if torrent_links:
                return torrent_links[0]['href']
                
        return None
    except Exception as e:
        print(f"Error extracting torrent link: {e}")
        return None

def download_torrent_with_selenium(paste_url):
    download_dir = config.get('torrent_save_dir', os.path.join(os.path.expanduser('~'), 'Downloads'))
    os.makedirs(download_dir, exist_ok=True)

    options = Options()
    options.add_argument("-headless")
    
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.dir", os.path.abspath(download_dir))
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.download.manager.closeWhenDone", True)
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-bittorrent,application/octet-stream")
    options.set_preference("browser.download.viewableInternally.enabledTypes", "")
    options.set_preference("browser.helperApps.alwaysAsk.force", False)
    
    print("Starting Firefox in headless mode...")
    
    driver = webdriver.Firefox(options=options)
    driver.set_window_size(1920, 1080)
    
    try:
        print(f"Navigating to paste URL: {paste_url}")
        driver.get(paste_url)
        
        time.sleep(5)
        print(f"Page title: {driver.title}")
        
        print("Looking for download button...")
        
        try:
            wait = WebDriverWait(driver, 20)
            download_btn = wait.until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(@class, 'alert-link') and contains(text(), 'Download attachment')]"))
            )
            
            filename = download_btn.get_attribute('download')
            if filename:
                print(f"Found torrent: {filename}")
            
            print("Clicking download button...")
            driver.execute_script("arguments[0].click();", download_btn)
            
            print(f"Download triggered, saving to: {download_dir}")
            
            time.sleep(20)
            
        except TimeoutException:
            print("Could not find the expected download button. Trying alternatives...")
            
            try:
                download_links = driver.find_elements(By.XPATH, "//a[contains(text(), 'Download')]")
                if download_links:
                    print(f"Found alternative download link, clicking...")
                    driver.execute_script("arguments[0].click();", download_links[0])
                    time.sleep(20)
                else:
                    print("No download links found")
            except Exception as alt_e:
                print(f"Error with alternative approach: {alt_e}")
            
    except Exception as e:
        print(f"Error using Selenium: {e}")
    finally:
        driver.quit()
        print("Browser closed")
        
        try:
            torrent_files = [f for f in os.listdir(download_dir) if f.endswith('.torrent')]
            if torrent_files:
                print(f"Success! Downloaded torrent file(s): {', '.join(torrent_files)}")
            else:
                print("No .torrent files found in the download directory. Download may have failed.")
        except Exception as verify_e:
            print(f"Error verifying downloads: {verify_e}")