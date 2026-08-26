from pathlib import Path
import urllib.request
import zipfile


ROOT_DIR = Path(__file__).resolve().parents[2]

RAW_DIR = ROOT_DIR / "data" / "raw"

URL = (
    "https://archive.ics.uci.edu/static/public/235/"
    "individual+household+electric+power+consumption.zip"
)

ZIP_PATH = RAW_DIR / "electric_power.zip"

DATA_FILE = RAW_DIR / "household_power_consumption.txt"


def main():

    RAW_DIR.mkdir(parents=True, exist_ok=True)

    if not ZIP_PATH.exists():
        print("Descargando dataset...")
        urllib.request.urlretrieve(URL, ZIP_PATH)
    else:
        print("El archivo ZIP ya existe.")

    if not DATA_FILE.exists():
        print("Extrayendo dataset...")

        with zipfile.ZipFile(ZIP_PATH, "r") as zip_file:
            zip_file.extractall(RAW_DIR)
    else:
        print("El dataset ya fue extraído.")

    if not DATA_FILE.exists():
        raise FileNotFoundError(
            "La ingesta terminó, pero no se encontró el archivo esperado."
        )

    print("Ingesta completada")
    print(f"Dataset disponible en: {DATA_FILE}")


if __name__ == "__main__":
    main()