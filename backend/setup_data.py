import os
import requests

BASE_URL = (
    "https://raw.githubusercontent.com/chapagain/php-swiss-ephemeris/master/sweph/"
)

FILES_TO_DOWNLOAD = [
    "sepl_18.se1",  # Planets (Sun - Pluto)
    "semo_18.se1",  # Moon
]

TARGET_DIR = "./data/ephemeris"


def download_ephemeris():
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)
        print(f"📂 Created directory: {TARGET_DIR}")

    for filename in FILES_TO_DOWNLOAD:
        file_path = os.path.join(TARGET_DIR, filename)

        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            print(f"  {filename} already exists (skipping).")
            continue

        print(f"⬇️ Downloading {filename} from mirror...")
        url = BASE_URL + filename
        try:
            r = requests.get(url, stream=True)
            if r.status_code == 200:
                with open(file_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=1024):
                        f.write(chunk)
                print(f"Successfully downloaded {filename}")
            else:
                print(f"Failed to download {filename} (Status: {r.status_code})")
        except Exception as e:
            print(f"Error downloading {filename}: {e}")


if __name__ == "__main__":
    download_ephemeris()
