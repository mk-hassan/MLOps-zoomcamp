# 🗂 NYC Green Taxi Data Uploader

This script automates the process of downloading **NYC Green Taxi trip data (Parquet format)** from a public CDN and uploading it to a specified **AWS S3 bucket**.

---

## 📁 Project Overview

### Functionality
- Downloads **monthly Parquet files** for a specified year.
- Uploads each file to **Amazon S3** under a specific prefix.

---

## 🔧 Requirements

- Python 3.7+
- [boto3](https://pypi.org/project/boto3/)
- [requests](https://pypi.org/project/requests/)
- AWS credentials configured (see below)

Install dependencies:

```bash
pip install boto3 requests
```

---

## 🔐 AWS Credentials

Make sure your AWS credentials are configured (for example, using the `~/.aws/credentials` file):

```ini
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
```

Alternatively, credentials can be configured via environment variables or IAM roles if running in AWS environments.

---

## 🧠 Code Structure

### Configuration

```python
s3_bucket_name = 'tyc-taxi'
s3_prefix = 'nyc-taxi/green/'
year = 2022
months = range(1, 13)
```

- `s3_bucket_name`: Destination S3 bucket name.
- `s3_prefix`: Folder/prefix in S3 where files will be uploaded.
- `year`: The target year of the taxi data.
- `months`: Months to download (e.g. January to December).

---

### Functions

#### `download_parquet_file(year: int, month: int, save_dir: Path) -> Path`

Downloads a Parquet file for the given `year` and `month` from NYC's open data CDN and saves it locally.

#### `upload_to_s3(local_path: Path, bucket: str, s3_key: str)`

Uploads a local file to the given S3 bucket using `boto3`.

#### `main()`

- Creates a temporary directory.
- Iterates through months.
- Downloads each month’s file.
- Uploads it to S3 with the key format: `green/{month}-{year}.parquet`.

---

## 🏁 How to Run

```bash
python script.py
```

Make sure your AWS credentials are correctly set up beforehand.

---

## 📂 S3 Upload Format

Example structure in the S3 bucket:

```
s3://tyc-taxi/
└── nyc-taxi/
    └── green/
        ├── 1-2022.parquet
        ├── 2-2022.parquet
        ├── ...
        └── 12-2022.parquet
```

---

## ✅ Example Output

```
Downloading https://.../green_tripdata_2022-01.parquet...
Saved to /tmp/tmpxxxx/green_tripdata_2022-01.parquet
Uploading /tmp/tmpxxxx/green_tripdata_2022-01.parquet to s3://tyc-taxi
...
```

---