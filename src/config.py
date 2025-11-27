from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
MODEL_DIR = BASE_DIR / "models" / "saved_models"
ASSETS_DIR = BASE_DIR / "assets"

# Data paths
RAW_DATA = DATA_DIR / "raw"
PROCESSED_DATA = DATA_DIR / "processed"
RESULTS_DATA = DATA_DIR / "results"

# Model paths
REGRESSION_MODEL = MODEL_DIR / "model_regression_best.pkl"
TFIDF_VECTORIZER = MODEL_DIR / "tfidf_vectorizer.pkl"

# Constants
PRICE_COLUMN = "Giá TB"
CONDITION_COLUMN = "Tình Trạng"

# Results paths
NEW_POST_FILE = RESULTS_DATA / "results_post_new_pending.csv"