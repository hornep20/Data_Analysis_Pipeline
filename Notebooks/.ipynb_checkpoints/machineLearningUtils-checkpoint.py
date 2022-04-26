from sklearn.metrics import classification_report
def printClassificationReport(y_true, y_pred):
    print('\nClassification Report\n------------------------------------------------------')
    print(classification_report(y_true, y_pred))

from sklearn import metrics
def printConfusionMatrix(model, X_test, y_test):
    fig, ax = plt.subplots(figsize=(7, 5))
    plt.rcParams.update({'font.size': 14})
    metrics.plot_confusion_matrix(model, X_test, y_test, cmap='Blues', ax=ax)
    cmlabels = ['True Negatives', 'False Positives', 'False Negatives', 'True Positives']
    for i,t in enumerate(ax.texts):
        t.set_text(t.get_text() + "\n" + cmlabels[i])
    plt.title('Confusion Matrix', size=15)
    plt.xlabel('Predicted Values', size=13)
    plt.ylabel('True Values', size=13)
    plt.show()
    
def printConfusionMatrixFromPrediction(y, y_pred):
    fig, ax = plt.subplots(figsize=(5, 4))
    plt.rcParams.update({'font.size': 14})
    cm = metrics.confusion_matrix(y, y_pred)
    ax = sns.heatmap(cm, annot=True, cmap='Blues', cbar=False, fmt='g')
    cmlabels = ['True Negatives', 'False Positives', 'False Negatives', 'True Positives']
    for i,t in enumerate(ax.texts):
        t.set_text(t.get_text() + "\n" + cmlabels[i])
    plt.title('Confusion Matrix', size=15)
    plt.xlabel('Predicted Values', size=13)
    plt.ylabel('True Values', size=13)
    plt.show()

from sklearn.metrics import roc_curve, auc
def rocAUC(X_proba, y):
    fp_rates, tp_rates, _ = roc_curve(y, X_proba)
    return auc(fp_rates, tp_rates)

def printROC(X_proba, y):
    fp_rates, tp_rates, _ = roc_curve(y, X_proba)
    roc_auc = auc(fp_rates, tp_rates)
    plt.subplot()
    plt.plot(fp_rates, tp_rates, color='green', lw=1, label='ROC curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], lw=1, linestyle='--', color='grey', label='Chance')
    plt.title('ROC Curve', size=15)
    plt.xlabel('False Positive Rate', size=13)
    plt.ylabel('True Positive Rate', size=13)
    plt.legend()
    plt.show()
    
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_validate, cross_val_predict
import pandas as pd
def crossValidationResults(model, X, y, cv, classification=True, regression_scoring=['explained_variance', 'r2', 'neg_root_mean_squared_error']):
    if classification:
        y_pred       = cross_val_predict(model, X, y, cv=cv)
        y_pred_proba = cross_val_predict(model, X, y, cv=cv, method='predict_proba')
        return y_pred, y_pred_proba
    else:
        val = cross_validate(model, X, y, cv=cv, scoring=regression_scoring)
        return pd.DataFrame.from_dict(val)

from IPython.display import display
def printCrossValidationResults(model, X, y, cv, classification=True, regression_scoring=['explained_variance', 'r2', 'neg_root_mean_squared_error']):
    print('\nCross-Validation Results\n----------------------------------------------')
    if classification:
        y_pred       = cross_val_predict(model, X, y, cv=cv)
        y_pred_proba = cross_val_predict(model, X, y, cv=cv, method='predict_proba')
        print('Accuracy: {:0.2%}'.format(accuracy_score(y, y_pred)))
        printClassificationReport(y, y_pred)
        printConfusionMatrixFromPrediction(y, y_pred)
        printROC(y_pred_proba[:,1], y)
    else:
        val = cross_validate(model, X, y, cv=cv, scoring=regression_scoring)
        df = pd.DataFrame.from_dict(val)
        display(df)
        display(pd.DataFrame(df.apply(lambda x : x.mean(), axis=0), columns={'mean'}).transpose())
        
# Continuous labels: Print the accuracy of training and testing
def printScoreReport(model, X_train, X_test, y_train, y_test, score_text, percent=False):
    # Evaluate the score of the training and testing using model.score
    print('\n{} Scores\n------------------------------------------------------'.format(score_text))
    if percent:
        print(f'Training: {model.score(X_train, y_train):0.2%}')
        print(f'Testing:  {model.score(X_test, y_test):0.2%}')
    else:
        print(f'Training: {model.score(X_train, y_train):0.4f}')
        print(f'Testing:  {model.score(X_test, y_test):0.4f}')
    
# Continuous labels: Print the accuracy of training and testing
def printAccuracyReport(model, X_train, X_test, y_train, y_test):
    # Evaluate the accuracy of the training and testing using model.score
    printScoreReport(model, X_train, X_test, y_train, y_test, 'Accuracy', True)

# Categorical labels: Print the accuracy of training and testing, the classification report, and confusion matrix
def printReport(model, X_train, X_test, y_train, y_test):
    # Print accuracy
    printAccuracyReport(model, X_train, X_test, y_train, y_test)
    
    # Predict y from X_test and print the classification report
    printClassificationReport(y_test, model.predict(X_test))

    # Plot a confusion matrix
    printConfusionMatrix(model, X_test, y_test)
    
    # Print ROC
    printROC(model.predict_proba(X_test)[:,1], y_test)
    
    
# Scaled and unscaled k-fold cross-validated logistic regression test for variable X, y, and k input
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, GridSearchCV, train_test_split
from sklearn.preprocessing import StandardScaler
def test(X, y, cv):
    # GridSearchCV
    # - Ignore warnings: lots of convergence warnings
    import warnings
    with warnings.catch_warnings():
        # Suppress warnings
        warnings.filterwarnings('ignore')

        # Standardized X
        X_scaled = pd.DataFrame(StandardScaler().fit_transform(X), columns=X.columns)

        # Unscaled grid search and model construction
        print('===== UNSCALED =====')
        param_grid = {'penalty': ['l1','l2'], 'max_iter': [100, 250, 500, 750, 1000], 'solver': ['liblinear','saga']}
        model = GridSearchCV(LogisticRegression(), param_grid, cv=cv).fit(X, y)
        lr = LogisticRegression(penalty=model.best_params_['penalty'], solver=model.best_params_['solver'], max_iter=model.best_params_['max_iter'])
        printCrossValidationResults(lr, X, y, cv)
        
        # Scaled grid search and model construction
        print('===== SCALED =====')
        model_scaled = GridSearchCV(LogisticRegression(), param_grid, cv=cv).fit(X_scaled, y)
        lr_scaled = LogisticRegression(penalty=model_scaled.best_params_['penalty'], solver=model_scaled.best_params_['solver'], max_iter=model_scaled.best_params_['max_iter'])
        printCrossValidationResults(lr_scaled, X_scaled, y, cv)
        

# Remove correlated values to minimize the effects of multicolinearity
import numpy as np
def removeCorrelated(df, threshold):
    cor = df.corr()
    mask = ~(cor.mask(np.tril(np.ones([len(cor)]*2, dtype=bool))).abs() > threshold).any()
    return df[mask.loc[mask[mask.index] == True].index]

import warnings
def gridSearchCV(model, param_grid, X, y, cv, scoring, n_jobs=-1):
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore')
        return GridSearchCV(model, param_grid, cv=cv, n_jobs=n_jobs).fit(X, y)
        
def printGridSearchCV(model, param_grid, X, y, cv, scoring, n_jobs=-1):
    m = gridSearchCV(model, param_grid, X, y, cv, scoring, n_jobs)
    printCrossValidationResults(m.best_estimator_, X, y, cv, False, scoring)
    print(m.best_params_)