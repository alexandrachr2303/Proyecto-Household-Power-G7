from pathlib import Path
import ssl
import urllib.request
import zipfile


ROOT_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT_DIR / "data" / "raw"
URL = "https://archive.ics.uci.edu/static/public/235/individual+household+electric+power+consumption.zip"
ZIP_PATH = RAW_DIR / "electric_power.zip"


def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    context = ssl._create_unverified_context()
    with urllib.request.urlopen(URL, context=context) as response:
        ZIP_PATH.write_bytes(response.read())

    with zipfile.ZipFile(ZIP_PATH, "r") as z:
        z.extractall(RAW_DIR)

    print("Ingesta completada")
    print(f"Archivos guardados en: {RAW_DIR}")


if __name__ == "__main__":
    main()
