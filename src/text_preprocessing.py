import re
import string
import pandas as pd
import csv
import os

# remove URLs
def remove_urls(tweet:string):
    tweet = re.sub(r'http\S+', '', tweet)
    return tweet


# Words with the punctation and special characters
def remove_punc(tweet:string):
    punctuations = '@#!?+&*[]-%.:/();$=><|{}^' + "'`"
    for p in punctuations:
        tweet = tweet.replace(p, f' {p} ')
        
    # ... and ..
    tweet = tweet.replace('...', ' ... ')
    if '...' not in tweet:
        tweet = tweet.replace('..', ' ... ')
    
    return tweet

def get_substitutions(map_file:string):
    # declare the substitues corresponding to the
    substitutions = {}

    with open(map_file, mode='r') as csvfile:
        reader = csv.reader(csvfile)

        next(reader, None)
        for row in reader:
            original_word, replacement = row
            substitutions[original_word] = replacement
    return substitutions

def cleaning_text(tweet:string, map_file:string):
    sub = get_substitutions(map_file)

    for original_word, replacement in sub.items():
        # Escape special characters in the original word for regex
        original_word_escaped = re.escape(original_word)
        # Perform the substitution using re.sub()
        tweet = re.sub(original_word_escaped, replacement, tweet)
    
    return tweet

def processing_text(df, text_processing_path):
    
    df["text"] = df["text"].apply(lambda x: remove_urls(x))
    df["text"] = df["text"].apply(lambda x: remove_punc(x))

    for map_file in os.listdir(text_processing_path):
        df["text"] = df["text"].apply(lambda x: cleaning_text(x, os.path.join(text_processing_path, map_file)))
    
    return df


if __name__=="__main__":
    TEXT_PROCESSING_PATH = "./src/text_processing_map_config"
    DATA_PATH = os.path.join("data")
    TRAINING_FILE = os.path.join(DATA_PATH, "train.csv")
    TESTING_FILE  = os.path.join(DATA_PATH, "test.csv")

    df_train = pd.read_csv(TRAINING_FILE)
    df_test  = pd.read_csv(TESTING_FILE)
    df_train = processing_text(df_train,TEXT_PROCESSING_PATH)
    df_test  = processing_text(df_test,TEXT_PROCESSING_PATH)
    
    df_train = df_train.to_csv(f"./data/cleaned_train.csv", index=False)
    df_test  = df_test.to_csv( f"./data/cleaned_test.csv" , index=False)