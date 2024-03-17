from sklearn import linear_model
from sklearn import naive_bayes
from sklearn import decomposition
from sklearn.svm import SVC
import xgboost as xgb


models = {
    "regression_model": linear_model.LogisticRegression(),
    "naive_bayes"     : naive_bayes.MultinomialNB(),
    "SVM"             : SVC(C=0.1, probability=True),
    "XGB"             : xgb.XGBClassifier(max_depth=7, 
                                          n_estimators=200, 
                                          colsample_bytree=0.8, 
                                          subsample=0.8, 
                                          nthread=10, 
                                          learning_rate=0.1)
} 