"""
Week 8 - Health API Project
 
This program collects COVID-19 data from different
countries and saves the information into a CSV file.
"""

from pathlib import Path
 
import pandas as pd
import requests
 
# Settings for the COVID-19 Health API
 
URL = "https://disease.sh/v3/covid-19/countries"
PARAMS = {}
RECORDS_KEY = None
 
# Choose the health information we want to study
 
RENAME = {}
 
KEEP = [
    "country",
    "continent",
    "cases",
    "deaths",
    "recovered",
    "tests",
    "population",
    "active"
]
 
# Remove rows with missing important information
 
MUST_HAVE = ["cases", "continent"]
 
# Location where the CSV file will be saved
 
RAW_FILE = Path(__file__).parent / "DATA" / "raw.csv"
 
 
def get_data(url, params):
    """Collect COVID-19 information from the API."""
    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        return response.json()
 
    except requests.RequestException as error:
        print("Could not get the health data:", error)
        return None
 
 
def make_table(data, records_key):
    """Convert the API information into a table."""
    records = data[records_key] if records_key else data
    return pd.json_normalize(records, sep="_")
 
 
def tidy_data(df):
    """Keep the health columns and remove missing values."""
    df = df.rename(columns=RENAME)
    df = df[KEEP]
    df = df.dropna(subset=MUST_HAVE)
    return df
 
 
def save_data(df, path):
    """Save the COVID-19 data into a CSV file."""
    path.parent.mkdir(exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Saved {len(df)} rows to {path}")
 
 
if __name__ == "__main__":
    data = get_data(URL, PARAMS)
 
    if data is not None:
        table = make_table(data, RECORDS_KEY)
        table = tidy_data(table)
 
        print("COVID-19 Health Data")
        print(table.head())
 
        save_data(table, RAW_FILE)