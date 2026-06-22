import json
import gzip
import shutil
import logging
from pathlib import Path

import requests


# Logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


# Configuration Loader

def load_config(config_path: str) -> dict:

    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


# Directory Creation

def create_city_directories(city_name: str):

    city_slug = city_name.lower().replace(" ", "_")

    city_dir = Path("data") / city_slug

    raw_dir = city_dir / "raw"
    extracted_dir = city_dir / "extracted"
    metadata_dir = city_dir / "metadata"
    profiling_dir = city_dir / "profiling"

    raw_dir.mkdir(parents=True, exist_ok=True)
    extracted_dir.mkdir(parents=True, exist_ok=True)
    metadata_dir.mkdir(parents=True, exist_ok=True)
    profiling_dir.mkdir(parents=True, exist_ok=True)

    return {
        "city_dir": city_dir,
        "raw_dir": raw_dir,
        "extracted_dir": extracted_dir,
        "metadata_dir": metadata_dir,
        "profiling_dir": profiling_dir
    }


# Download Functions

def download_file(url: str, destination: Path):

    logging.info(f"Downloading {destination.name}")

    response = requests.get(
        url,
        stream=True,
        timeout=120
    )

    response.raise_for_status()

    with open(destination, "wb") as file:

        for chunk in response.iter_content(chunk_size=8192):

            if chunk:
                file.write(chunk)

    logging.info(f"Downloaded {destination.name}")


def download_all_files(files: dict, raw_dir: Path):

    for file_key, url in files.items():

        filename = url.split("/")[-1]

        destination = raw_dir / filename

        if destination.exists():

            logging.info(
                f"Already exists: {filename}"
            )

            continue

        download_file(url, destination)


# Extraction Functions

def extract_gzip_file(
    gz_path: Path,
    extracted_dir: Path
):

    output_filename = gz_path.stem

    output_path = extracted_dir / output_filename

    if output_path.exists():

        logging.info(
            f"Already extracted: {output_filename}"
        )

        return

    logging.info(f"Extracting {gz_path.name}")

    with gzip.open(gz_path, "rb") as f_in:

        with open(output_path, "wb") as f_out:

            shutil.copyfileobj(f_in, f_out)

    logging.info(
        f"Extracted {output_filename}"
    )


def extract_all_files(
    raw_dir: Path,
    extracted_dir: Path
):

    for file_path in raw_dir.iterdir():

        if file_path.suffix == ".gz":

            extract_gzip_file(
                file_path,
                extracted_dir
            )

        else:

            destination = (
                extracted_dir /
                file_path.name
            )

            if destination.exists():

                continue

            shutil.copy(
                file_path,
                destination
            )


# Metadata

def generate_metadata(
    city: str,
    raw_dir: Path,
    metadata_dir: Path
):

    metadata = {
        "city": city,
        "files": []
    }

    for file in raw_dir.iterdir():

        metadata["files"].append({
            "file_name": file.name,
            "size_mb": round(
                file.stat().st_size / (1024 * 1024),
                2
            )
        })

    output_file = (
        metadata_dir /
        "ingestion_metadata.json"
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            metadata,
            f,
            indent=4
        )

    logging.info(
        "Metadata file generated"
    )


# Pipeline

def run_pipeline(config_path: str):

    logging.info(
        "Starting ingestion pipeline"
    )

    config = load_config(config_path)

    city = config["city"]

    files = config["files"]

    dirs = create_city_directories(city)

    logging.info(
        f"Selected City: {city}"
    )

    download_all_files(
        files,
        dirs["raw_dir"]
    )

    extract_all_files(
        dirs["raw_dir"],
        dirs["extracted_dir"]
    )

    generate_metadata(
        city,
        dirs["raw_dir"],
        dirs["metadata_dir"]
    )

    logging.info(
        "Pipeline completed successfully"
    )


# Entry Point

if __name__ == "__main__":

    run_pipeline(
        "config/london.json"
    )