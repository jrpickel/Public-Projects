import pandas as pd
import numpy as np
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.linear_model import SGDClassifier
from itertools import*
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix

def clean_data(file):
    '''
    A function used to read in a csv file and converts all categorical variables to numeric values.
    Returns: A DataFrame object
    '''
    # read in the specified file
    df = pd.read_csv(file,header = 0)
    # replace all the values with the given value
    df = df.replace("Yes",1)
    df = df.replace("No",0)
    df = df.replace("Male",1)
    df = df.replace("Female",0)
    df = df.replace("< 1 Year",1)
    df = df.replace("> 2 Years",2)
    df = df.replace("1-2 Year",3)
    return df.iloc[:,1:]

def feature_combination(df):
    '''
    A function that creates all the possible combination of features
    Parameters: A DataFrame that hold the features of interest
    Returns: A nested list containing all the combinations as tuples.
    '''
    # new df that removes the response column as a possible feature
    new_df = df.iloc[:,0:10] 
    all_possible = [] # balnk list
    # a list of teh possible features
    features = new_df.columns.tolist()
    # loop through features and create multiple combinations each with increasing length
    for i in range(2,len(features)):
        all_possible.extend(list(combinations(features,i)))
    return all_possible

def train_model(df,features):
    '''
    A function that will train a given model.
    Parameters:
    df: a DataFrame that holds the training data
    features: A tuple that has the features that will be used to test
    Returns: A three trained machine learning models that will be used for testing
    '''
    X_train = df.loc[:,features] # training data
    y_train = df.loc[X_train.index,'Response'].tolist() # training labels
    # create adn train the three diffrent models on the training data
    svm = SVC(kernel = 'rbf', C = 1,gamma= 0.1).fit(X_train, y_train)
    knn = KNeighborsClassifier(n_neighbors=3).fit(X_train,y_train)
    clf = DecisionTreeClassifier().fit(X_train,y_train)
    return svm,knn,clf
    
def test_model(df,features,model):
    '''
    A function that will test a given model.
    Parameters:
    df: a DataFrame that holds the testing data
    features: A tuple that has the features that will be used to test
    model: A machine learning model that will be used for testing
    Returns: A float value that represents the accuracy of the model
    '''
    X_test = df.loc[:,features] # test data
    y_test = df.loc[X_test.index,'Response'].tolist() # test labels
    accuracy = model.score(X_test, y_test) # accuracy score
    return accuracy

def main():   
    train = clean_data('train.csv') # read in and clean the training data file
    test = clean_data('test.csv') # read in and clean the testing data file
    feature_combo = feature_combination(train) # create all the possible feature combinations
    # dictionary named stats that will hold all of the results
    stats = {'svm':{'Accuracy':[],'Feature':[]},'knn':{'Accuracy':[],'Feature':[]},'clf':{'Accuracy':[],'Feature':[]}}
    count = 1
    # loop through all feature sand build a moel for each of them
    for i in feature_combo:
        print("{:.2f}% complete".format((count/len(feature_combo))*100))
        svm,knn,clf = train_model(train,i)
        stats['svm']['Accuracy'].append(test_model(test,i,svm))
        stats['svm']['Feature'].append(i)
        stats['knn']['Accuracy'].append(test_model(test,i,knn))
        stats['knn']['Feature'].append(i)
        stats['clf']['Accuracy'].append(test_model(test,i,clf))
        stats['clf']['Feature'].append(i)
        count += 1
    
    # create data frame's to tabulate all the results.
    df_svm = pd.DataFrame(stats['svm'])
    df_knn = pd.DataFrame(stats['knn'])
    df_clf = pd.DataFrame(stats['clf'])
    
    # create data frame that has only the highest accuracy features.
    df_svm_max = df_svm.loc[df_svm['Accuracy'] >= df_svm['Accuracy'].max(),:]
    df_knn_max = df_knn.loc[df_knn['Accuracy'] >= df_knn['Accuracy'].max(),:]
    df_clf_max = df_clf.loc[df_clf['Accuracy'] >= df_clf['Accuracy'].max(),:]
    
    # merge all the data sets.
    new_df = df_svm_max.append(df_knn_max)
    new_df = new_df.append(df_clf_max)
    new_df['Model'] = ['svm', 'svm', 'svm', 'svm', 'svm', 'svm', 'svm', 'svm', 'knn', 'knn', 'clf', 'clf', 'clf', 'clf']
    new_df.to_csv('output.csv',index=False)

main()