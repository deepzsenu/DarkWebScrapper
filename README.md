Absolutely! Here's your focused `README.md` file — clean, clear, and without license or credit sections:

---


# 🕵️ Dark Web Media Scraper

A Python-based tool to scrape and download `.mp4`, `.jpg`, and `.png` files from `.onion` websites over the Tor network. This script supports both full-page scraping and direct media links. Ideal for legal research, archival, and testing purposes.

---

## 🔧 Features

- ✅ Download `.mp4`, `.jpg`, and `.png` files
- ✅ Automatically creates folders:
  - `downloads/images`
  - `downloads/videos`
- ✅ Supports both:
  - full `.onion` page scraping
  - direct media URLs
- ✅ Uses Tor (`SOCKS5` on port `9050`) for anonymous access
- ✅ Multi-threaded downloads with retry logic and progress bar

---

## 📦 Requirements

- Python 3.7+
- Tor Browser (must be installed and running)

### 🔌 Python Packages

Install dependencies:

```bash
pip install requests[socks] beautifulsoup4 tqdm
````


---

## 🧪 Preparing Your Environment

### Step 1: Install Tor Browser

Download and install from:
👉 [https://www.torproject.org/download/](https://www.torproject.org/download/)

### Step 2: Launch Tor

Open **Tor Browser** and keep it running. This allows the scraper to connect to `.onion` sites via the built-in SOCKS proxy (`127.0.0.1:9050`).

> No need to manually browse anything — just keep the browser open in the background.

---

## 🚀 How to Use

### Option 1: Run and Enter URL When Prompted

```bash
python dark_scraper.py
```

You'll see:

```
Enter a .onion URL:
```

Paste your `.onion` link here and press Enter.

---

### Option 2: Pass URL Directly via Command Line

```bash
python dark_scraper.py http://examplev3onionaddress.onion/
```

---

## 📁 Output

Downloads are saved into the following auto-created folders:

```
downloads/
├── images/   ← .jpg and .png files
└── videos/   ← .mp4 files
```

---

## ✅ Supported URLs

| Type              | Example                                        | Behavior               |
| ----------------- | ---------------------------------------------- | ---------------------- |
| Full pages        | `http://somesite.onion/gallery/`               | Scrapes all media tags |
| Direct media file | `http://somesite.onion/files/video.mp4`        | Downloads directly     |
| v3 .onion only    | Must be 56 characters and start with `http://` | Required               |

---

## 🧯 Troubleshooting

| Problem                                      | Solution                                                 |
| -------------------------------------------- | -------------------------------------------------------- |
| `RemoteDisconnected` or `Connection Aborted` | Server is blocking non-browser clients or is down        |
| No files found                               | Media might be dynamically loaded via JS (not supported) |
| "Invalid .onion URL"                         | Ensure it's a 56-character v3 `.onion` address           |
| Files fail to download                       | Check your Tor connection and try again                  |

---

## 🛠 Example

```bash
python dark_scraper.py http://examplev3onionaddress.onion/
```

Console output:

```
[i] Found 3 videos, 4 JPGs, 2 PNGs.
✔ Downloaded mp4: sample1.mp4
✔ Downloaded jpg: cover.jpg
✔ Downloaded png: icon.png
```

---


