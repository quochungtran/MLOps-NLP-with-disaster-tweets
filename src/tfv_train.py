import argparse
import os
import joblib
import pandas as pd
from sklearn import metrics
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize
from sklearn import preprocessing, decomposition, model_selection, metrics, pipeline
import mlflow
from mlflow.models.signature import infer_signature


# local import 
import config as cfg
import model_dispatcher

def tfidf_process(df_train):
    # init TfidfVectorizer with NLTK's work_tokenize
    tfidf = TfidfVectorizer(
        min_df=3,
        max_features=None,
        strip_accents='unicode',
        analyzer='word',
        token_pattern=r'\w{1,}',
        ngram_range=(1,3), 
        use_idf=True,
        smooth_idf=True, 
        sublinear_tf=True,
        stop_words = 'english'
    )

    # fit ciunt_vec on the training data reviews 
    tfidf.fit(df_train[cfg.TEXT])
    # save the tfidf model
    joblib.dump(tfidf, os.path.join(cfg.MODEL_PATH, "tfidf.pkl"))

    return tfidf


def run(fold, model, pre=False):
    
    # read training data with folds
    df = pd.read_csv(cfg.CLEANED_TRAINING_FILE)
    
    # training data where kfold is not equal to provided fold
    # also, note that we reset the index
    df_train = df[df.kfold != fold].reset_index(drop=True)
    # validation
    df_valid = df[df.kfold == fold].reset_index(drop=True)

    count_vec = tfidf_process(df_train)
          
    # trainsform training and validation data reviews
    x_train = count_vec.transform(df_train[cfg.TEXT])
    x_valid = count_vec.transform(df_valid[cfg.TEXT])

    # target is label col in the dataframe
    y_train = df_train[cfg.LABEL].values
    y_valid = df_valid[cfg.LABEL].values

    # do Scale the data obtained from SVD. Renaming variable to resuse without scaling
    if (pre):
        print("Data precocessing ...")
        svd = decomposition.TruncatedSVD(n_components=120)
        svd.fit(x_train)    
        x_train = svd.transform(x_train)
        x_valid = svd.transform(x_valid)

        scl = preprocessing.StandardScaler()
        scl.fit(x_train)
        x_train = scl.transform(x_train)
        x_valid = scl.transform(x_valid)
    
    # fetch the model from model_dispatch
    clf = model_dispatcher.models[model]

    # mlflow setting up
    mlflow.set_tracking_uri(cfg.MLFLOW_TRACKING_URI)
    mlflow.set_experiment(
        f"tfv_{model}_fold_{fold}_exp"
    )

    print("Model training    ...")
    # fit the model on training data
    clf.fit(x_train, y_train)

    # create prediction for validation samples
    preds = clf.predict(x_valid)

    # print(df_valid)
    # print(len(preds))
    # calculate and show accuracy
    accuracy = metrics.accuracy_score(y_valid, preds)
    print(f"Fold: {fold}  Accuracy = {accuracy} ")
    
    # # mlflow log
    mlflow.log_params(clf.get_params())
    
    metrics_models  = {"Accuracy": accuracy}
    mlflow.log_metrics(metrics_models)

    signature = infer_signature(x_valid, accuracy)
    mlflow.sklearn.log_model(
            sk_model=clf,
            artifact_path="model",
            signature=signature,
        )
    mlflow.end_run()
    
    # save the model
    joblib.dump(
        clf, 
        os.path.join(cfg.MODEL_PATH, f"tfv_{model}_fold_{fold}.pkl")
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--pre",
        type=bool
    )

    parser.add_argument(
        "--fold",
        type=int
    )

    parser.add_argument(
        "--model",
        type=str
    )

    args = parser.parse_args()

    run(
        fold=args.fold,
        model=args.model,
        pre=args.pre
    )