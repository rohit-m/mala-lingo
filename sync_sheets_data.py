import os
import pandas as pd
import requests
from supabase import create_client
from datetime import datetime
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('/var/log/sync.log')
    ]
)
logger = logging.getLogger(__name__)

# Supabase configuration
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    logger.error("Missing required environment variables: SUPABASE_URL and/or SUPABASE_KEY")
    raise ValueError("Missing required environment variables")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Google Sheets URLs (add your URLs here)
SHEET_URLS = os.getenv('SHEET_URLS', '').split(',')
if not SHEET_URLS or SHEET_URLS[0] == '':
    logger.error("No Google Sheets URLs provided in SHEET_URLS environment variable")
    raise ValueError("No Google Sheets URLs provided")

def get_sheet_data(url):
    """Fetch data from Google Sheets URL and return as DataFrame"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return pd.read_csv(pd.StringIO(response.text))
    except Exception as e:
        logger.error(f"Error fetching data from {url}: {str(e)}")
        return None

def get_existing_data(table_name):
    """Fetch existing data from Supabase table"""
    try:
        response = supabase.table(table_name).select("*").execute()
        return pd.DataFrame(response.data)
    except Exception as e:
        logger.error(f"Error fetching data from Supabase: {str(e)}")
        return pd.DataFrame()

def sync_data():
    """Main function to sync data from Google Sheets to Supabase"""
    logger.info("Starting data sync process")
    
    for url in SHEET_URLS:
        try:
            # Get sheet name from URL or use a default table name
            sheet_name = url.split('/')[-2]  # You might want to customize this
            table_name = f"sheet_{sheet_name}"
            
            # Get new data from Google Sheets
            new_data = get_sheet_data(url)
            if new_data is None:
                continue
                
            # Get existing data from Supabase
            existing_data = get_existing_data(table_name)
            
            # If no existing data, insert all new data
            if existing_data.empty:
                records = new_data.to_dict('records')
                supabase.table(table_name).insert(records).execute()
                logger.info(f"Inserted {len(records)} new records into {table_name}")
                continue
            
            # Find new records by comparing with existing data
            # Assuming there's a unique identifier column, modify this as needed
            id_column = 'id'  # Change this to your unique identifier column
            existing_ids = set(existing_data[id_column])
            new_records = new_data[~new_data[id_column].isin(existing_ids)]
            
            if not new_records.empty:
                records = new_records.to_dict('records')
                supabase.table(table_name).insert(records).execute()
                logger.info(f"Inserted {len(records)} new records into {table_name}")
            else:
                logger.info(f"No new records found for {table_name}")
                
        except Exception as e:
            logger.error(f"Error processing sheet {url}: {str(e)}")
            continue

if __name__ == "__main__":
    sync_data() 