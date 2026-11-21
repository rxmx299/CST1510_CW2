"""
Week 8 - Health API Project
 
This program collects COVID-19 data from different
countries and saves the information into a CSV file.
"""

from pathlib import Path
 
import pandas as pd
import requests
 
# ---- Settings for the COVID-19 Health API ----
 
URL = "https://disease.sh/v3/covid-19/countries" # the URL of the API
PARAMS = {}                                      # additional parameters (none needed here)
RECORDS_KEY = None                               # None because the API response is already a flat list
 
# ---- Data filtering settings ----
 
RENAME = {}                                      # dictionary to rename columns if needed
KEEP = [                                         # the columns we want to keep in our dataset
    "country",
    "continent",
    "cases",
    "deaths",
    "recovered",
    "tests",
    "population",
    "active"
] 
MUST_HAVE = ["cases", "continent"]               # removes rows missing data in these required columns

# ---- File path configuration ----

# creates the file path for raw.csv inside the DATA folder
RAW_FILE = Path(__file__).parent / "DATA" / "raw.csv"
 
# ---- The functions ---- 

def get_data(url, params):
    """Collect COVID-19 information from the API."""
    try:
        # sends a GET request to the API with a 15-second timeout limit
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status() # raises an error if the response has an unsuccessful status code like 404 or 500
        return response.json()      # converts the JSON (raw text) response into a Python list/dictionary
 
    except requests.RequestException as error:
        # handles request errors and displays an error message instead of crashing
        print("Could not get the health data:", error)
        return None
 
 
def make_table(data, records_key):
    """Convert the API information into a table."""
    # if a records_key is provided, extract that key. Otherwise, use the data list directly
    records = data[records_key] if records_key else data
    # flattens JSON structures into a pandas DataFrame (table)
    return pd.json_normalize(records, sep="_")
 
 
def tidy_data(df):
    """Keep the health columns and remove missing values."""
    df = df.rename(columns=RENAME)     # applies any column renaming rules
    df = df[KEEP]                      # keeps only the columns specified in the KEEP list
    df = df.dropna(subset=MUST_HAVE)   # drops rows with empty values in required columns
    return df
 
 
def save_data(df, path):
    """Save the COVID-19 data into a CSV file."""
    path.parent.mkdir(exist_ok=True)   # ensures the DATA folder exists before saving
    df.to_csv(path, index=False)       # saves the DataFrame to CSV without row indices
    print(f"Saved {len(df)} rows to {path}")
 
 
if __name__ == "__main__":
    # fetch raw data from the API
    data = get_data(URL, PARAMS)
 
    if data is not None:
        # converts to table and cleans it up
        table = make_table(data, RECORDS_KEY)
        table = tidy_data(table)

        # prints a quick preview of the top rows
        print("COVID-19 Health Data")
        print(table.head())

        # saves the cleaned data to disk
        save_data(table, RAW_FILE)