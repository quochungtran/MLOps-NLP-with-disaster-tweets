import os

HOMEDIR = "."

# fetch home directory
# from docker container

LABEL = "target"
TEXT  = "text"

DATA_PATH = os.path.join("data")
MODEL_PATH = os.path.join("models")

# original tranining/testing files
TRAINING_FILE = os.path.join(DATA_PATH, "train.csv")
TESTING_FILE  = os.path.join(DATA_PATH, "test.csv")

# post-processing training/testing files
CLEANED_TRAINING_FILE = os.path.join(DATA_PATH, "cleaned_train_folds.csv")
CLEANED_TESTING_FILE  = os.path.join(DATA_PATH, "cleaned_test.csv")

# mlflow tracking uri
MLFLOW_TRACKING_URI = "http://mlflow.tracking.com:5001"

# config files path for text processing 
TEXT_PROCESSING_MAP_PATH = "./src/text_processing_map_config"