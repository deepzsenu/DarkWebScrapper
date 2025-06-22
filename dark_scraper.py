import os
import requests
import sys
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import re

# === CONFIGURATION ===
TOR_PROXY = 'socks5h://127.0.0.1:9050'
ROOT_DOWNLOAD_DIR = 'downloads'
VIDEO_DIR = os.path.join(ROOT_DOWNLOAD_DIR, 'videos')
IMAGE_DIR = os.path.join(ROOT_DOWNLOAD_DIR, 'images')
MAX_THREADS = 10
TIMEOUT = 30
RETRY_LIMIT = 3

proxies = {
    'http': TOR_PROXY,
    'https': TOR_PROXY
}

# === SETUP FOLDERS ===
def setup_folders():
    for path in [VIDEO_DIR, IMAGE_DIR]:
        os.makedirs(path, exist_ok=True)

# === URL VALIDATION ===
def is_valid_onion_url(url):
    pattern = r'^http://[a-z2-7]{56}\.onion(?:/.*)?$'
    return re.match(pattern, url) is not None

def ensure_http_scheme(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        return "http://" + url
    return url

def is_direct_media_link(url):
    return url.lower().endswith(('.mp4', '.jpg', '.png'))

# === NETWORK + PARSING HELPERS ===
def fetch_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, proxies=proxies, timeout=TIMEOUT)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"[!] Error fetching {url}: {e}")
        return None

def find_media_links(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    media_links = {'mp4': [], 'jpg': [], 'png': []}

    # <a href=...>
    for tag in soup.find_all('a', href=True):
        href = tag['href']
        full_url = urljoin(base_url, href)
        href_lower = href.lower()
        if href_lower.endswith('.mp4'):
            media_links['mp4'].append(full_url)
        elif href_lower.endswith('.jpg'):
            media_links['jpg'].append(full_url)
        elif href_lower.endswith('.png'):
            media_links['png'].append(full_url)

    # <img src=...>
    for img in soup.find_all('img', src=True):
        src = img['src']
        full_url = urljoin(base_url, src)
        if src.lower().endswith('.jpg'):
            media_links['jpg'].append(full_url)
        elif src.lower().endswith('.png'):
            media_links['png'].append(full_url)

    # <source src=...>
    for src_tag in soup.find_all('source', src=True):
        src = src_tag['src']
        full_url = urljoin(base_url, src)
        if src.lower().endswith('.mp4'):
            media_links['mp4'].append(full_url)

    return media_links

def sanitize_filename(url):
    parsed = urlparse(url)
    return os.path.basename(parsed.path).split('?')[0] or f"file_{hash(url)}"

def download_file(url, media_type, session, retry_count=0):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }

    filename = sanitize_filename(url)
    folder = VIDEO_DIR if media_type == 'mp4' else IMAGE_DIR
    filepath = os.path.join(folder, filename)

    if os.path.exists(filepath):
        return f"[✓] Skipped ({media_type} exists): {filename}"

    try:
        with session.get(url, proxies=proxies, stream=True, timeout=TIMEOUT, headers=headers) as r:
            r.raise_for_status()
            with open(filepath, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return f"[✔] Downloaded {media_type}: {filename}"
    except Exception as e:
        if retry_count < RETRY_LIMIT:
            return download_file(url, media_type, session, retry_count + 1)
        return f"[✘] Failed ({media_type}): {url} - {e}"

# === MAIN SCRAPE FUNCTION ===
def scrape_and_download(url):
    url = ensure_http_scheme(url)
    if not is_valid_onion_url(url):
        print("[!] Invalid .onion URL. Must be a valid v3 .onion (56 characters).")
        return

    with requests.Session() as session:
        if is_direct_media_link(url):
            ext = url.lower().split('.')[-1]
            print(f"[i] Direct file detected: {url}")
            result = download_file(url, ext, session)
            print(result)
        else:
            html = fetch_html(url)
            if not html:
                return

            media_links = find_media_links(html, url)
            total_files = sum(len(lst) for lst in media_links.values())
            print(f"[i] Found {len(media_links['mp4'])} videos, {len(media_links['jpg'])} JPGs, {len(media_links['png'])} PNGs.")

            with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
                futures = []

                for link in media_links['mp4']:
                    futures.append(executor.submit(download_file, link, 'mp4', session))
                for link in media_links['jpg']:
                    futures.append(executor.submit(download_file, link, 'jpg', session))
                for link in media_links['png']:
                    futures.append(executor.submit(download_file, link, 'png', session))

                for f in tqdm(as_completed(futures), total=total_files, desc="Downloading Media"):
                    print(f.result())

# === ENTRY POINT ===
if __name__ == "__main__":
    setup_folders()

    if len(sys.argv) > 1:
        onion_url = sys.argv[1]
    else:
        onion_url = input("Enter a .onion URL: ").strip()

    scrape_and_download(onion_url)
