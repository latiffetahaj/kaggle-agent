from langchain.tools import tool
from langsmith import traceable
from kaggle.api.kaggle_api_extended import KaggleApi
import os
import pandas as pd
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from urllib.parse import urlparse

# Configure logger for this module
logger = logging.getLogger(__name__)


@tool
@traceable(name="fetch_kaggle_dataset")
def fetch_kaggle_dataset(kaggle_link: str, download_path: str = "./datasets") -> dict:

    """
    Downloads a Kaggle dataset and returns structured info for the agent.
    
    This tool downloads a dataset from Kaggle, extracts it, and provides
    schema information for all CSV files found.
    
    Args:
        kaggle_link: Full URL to the Kaggle dataset (e.g., 
                    "https://www.kaggle.com/datasets/user/dataset-name")
        download_path: Local directory path where dataset will be saved.
                      Defaults to "./datasets"
    
    Returns:
        dict: A dictionary with the following structure:
            {
                "status": "ok" or "error",
                "folder_path": str,  # Absolute path to downloaded dataset
                "csv_files": List[str],  # List of CSV filenames found
                "schemas": Dict[str, Dict],  # Schema info per CSV file
                "dataset_slug": str,  # Extracted dataset identifier
                "error_message": str (optional),  # Present if status="error"
                "metadata": {  # Additional context
                    "total_files": int,
                    "timestamp": str
                }
            }
    
    Raises:
        No exceptions raised - all errors are caught and returned in response dict
    """

    logger.info(f"🚀 Starting Kaggle dataset download")
    logger.info(f"   Link: {kaggle_link}")
    logger.info(f"   Download path: {download_path}")
    
    start_time = datetime.now()
    
    try:
        logger.info("📝 Step 1/4: Authenticating with Kaggle API...")
        api = KaggleApi()
        api.authenticate()
        logger.info("✅ Authentication successful")
        
        logger.info("📝 Step 2/4: Parsing dataset identifier from URL...")
        try:
            dataset_slug = _extract_dataset_slug(kaggle_link)
            logger.info(f"✅ Extracted dataset slug: {dataset_slug}")
        except Exception as e:
            error_msg = f"Failed to parse Kaggle link: {e}"
            logger.error(f"❌ {error_msg}")
            return _create_error_response(error_msg, "url_parsing")
        
        logger.info("📝 Step 3/4: Preparing download directory...")
        abs_download_path = os.path.abspath(download_path)
        os.makedirs(abs_download_path, exist_ok=True)
        logger.info(f"✅ Directory ready: {abs_download_path}")
        
        logger.info("📝 Step 4/4: Downloading dataset from Kaggle...")
        logger.info(f"   This may take a while depending on dataset size...")
        try:
            api.dataset_download_files(dataset_slug, path=abs_download_path, unzip=True)
            logger.info("✅ Dataset downloaded and extracted successfully")
        except Exception as e:
            error_msg = f"Download failed: {str(e)}"
            logger.error(f"❌ {error_msg}")
            logger.error(f"   Dataset slug: {dataset_slug}")
            logger.error(f"   Check: 1) Kaggle credentials, 2) Dataset exists, 3) Network connection")
            return _create_error_response(error_msg, "download", dataset_slug=dataset_slug, folder_path=abs_download_path)
        
        logger.info("📊 Analyzing downloaded files...")
        csv_files = [f for f in os.listdir(abs_download_path) 
                    if f.endswith(".csv")]
        
        if not csv_files:
            logger.warning("⚠️  No CSV files found in downloaded dataset")
        else:
            logger.info(f"✅ Found {len(csv_files)} CSV file(s)")
        
        schemas = {}
        for idx, csv_file in enumerate(csv_files, 1):
            logger.info(f"   Analyzing {idx}/{len(csv_files)}: {csv_file}")
            try:
                file_path = os.path.join(abs_download_path, csv_file)
                df = pd.read_csv(file_path, nrows=5)
                schema = df.dtypes.astype(str).to_dict()
                schemas[csv_file] = schema
                logger.info(f"      ✅ Schema extracted: {len(schema)} columns")
            except Exception as e:
                error_msg = f"Failed to read {csv_file}: {str(e)}"
                logger.warning(f"      ⚠️  {error_msg}")
                schemas[csv_file] = {"error": error_msg}
                return _create_error_response(error_msg, "read", dataset_slug=dataset_slug, folder_path=abs_download_path, csv_file=csv_file)
        
        elapsed_time = (datetime.now() - start_time).total_seconds()
        logger.info(f"🎉 Dataset processing complete in {elapsed_time:.2f}s")
        logger.info(f"   Total CSV files: {len(csv_files)}")
        logger.info(f"   Location: {abs_download_path}")
        
        result = {
            "status": "ok",
            "folder_path": abs_download_path,
            "csv_files": csv_files,
            "schemas": schemas,
            "dataset_slug": dataset_slug,
            "metadata": {
                "total_files": len(csv_files),
                "timestamp": datetime.now().isoformat(),
                "elapsed_seconds": round(elapsed_time, 2)
            }
        }
        
        return result
        
    except Exception as e:
        # Catch-all for unexpected errors
        error_msg = f"Unexpected error: {str(e)}"
        logger.exception(f"❌ {error_msg}")
        return _create_error_response(error_msg, "unexpected", dataset_slug=None, folder_path=download_path)


def _extract_dataset_slug(kaggle_link: str) -> str:
    """
    Extract dataset slug from Kaggle URL.
    """
    try:
        parsed = urlparse(kaggle_link)
        
        path = parsed.path.strip('/')
        
        parts = path.split('/')
        
        if 'datasets' in parts:
            idx = parts.index('datasets')
            if len(parts) > idx + 2:
                return f"{parts[idx + 1]}/{parts[idx + 2]}"
        
        if len(parts) >= 2:
            return f"{parts[-2]}/{parts[-1]}"
        
        raise ValueError(f"Invalid Kaggle URL format: {kaggle_link}")
        
    except Exception as e:
        raise ValueError(f"Failed to parse Kaggle URL '{kaggle_link}': {str(e)}")

def _create_error_response(error_msg: str, error_step: str, **kwargs) -> dict:
    """Helper to create consistent error responses."""
    logger.error(f"❌ {error_msg}")
    return {
        "status": "error",
        "error_message": error_msg,
        "dataset_slug": kwargs.get('dataset_slug'),
        "folder_path": kwargs.get('folder_path'),
        "csv_files": [],
        "schemas": {},
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "error_step": error_step
        }
    }