import os

HOMEDIR = "."

# fetch home directory
# from docker container

LABEL = "target"
TEXT  = "text"

# define path to BERT model files
# now we assume that all the data is stored in data
DATA_PATH = os.path.join("data")

# this is where you want to save the modeled
MODEL_PATH = os.path.join("models")

# original tranining/testing files
TRAINING_FILE = os.path.join(DATA_PATH, "train.csv")
TESTING_FILE  = os.path.join(DATA_PATH, "test.csv")

# post-processing training/testing files
CLEANED_TRAINING_FILE = os.path.join(DATA_PATH, "cleaned_train_folds.csv")
CLEANED_TESTING_FILE  = os.path.join(DATA_PATH, "cleaned_test.csv")

# mlflow tracking uri
MLFLOW_TRACKING_URI = "http://mlflow.tracking.com:5001"