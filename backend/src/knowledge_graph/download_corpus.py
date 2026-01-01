import requests
import os

# URL from your project references (Source: Internet Archive)
BPHS_URL = "https://archive.org/stream/ParasharaHoraSastra/BrihatParasharaHoraSastra_VedicAstrologyEbook_djvu.txt"
OUTPUT_DIR = "./data/raw_texts"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "bphs_full.txt")


def download_full_corpus():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    print(f"⬇️ Starting download of full BPHS Corpus...")
    try:
        response = requests.get(BPHS_URL, stream=True)
        response.raise_for_status()

        total_size = 0
        with open(OUTPUT_FILE, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                total_size += len(chunk)

        print(f"  Download Complete: {OUTPUT_FILE}")
        print(f"📦 Total Size: {total_size / 1024 / 1024:.2f} MB")

    except Exception as e:
        print(f"  Download Failed: {e}")


if __name__ == "__main__":
    download_full_corpus()
