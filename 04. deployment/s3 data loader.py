import boto3
from pathlib import Path
import requests
import tempfile

# Config
s3_bucket_name = 'tyc-taxi'
s3_prefix = 'nyc-taxi/green/'
year = 2022  # Change as needed
months = range(1,13)  # Example: Jan–Mar

# Initialize S3 client
client = boto3.client("s3")

def download_parquet_file(year: int, month: int, save_dir: Path) -> Path:
    url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_{year:04d}-{month:02d}.parquet"
    local_path = save_dir / url.split("/")[-1]

    print(f"Downloading {url}...")
    response = requests.get(url)
    response.raise_for_status()

    with open(local_path, "wb") as f:
        f.write(response.content)

    print(f"Saved to {local_path}")
    return local_path

def upload_to_s3(local_path: Path, bucket: str, s3_key: str):
    print(f"Uploading {local_path} to s3://{bucket}")
    client.upload_file(str(local_path), bucket, s3_key)

def main():
    with tempfile.TemporaryDirectory() as tmp_dir_name:
        tmp_dir = Path(tmp_dir_name)

        for month in months:
            local_file = download_parquet_file(year, month, tmp_dir)
            upload_to_s3(local_file, s3_bucket_name, f"green/{month:0d}-{year:04d}.parquet")

if __name__ == "__main__":
    main()
