Libraries used:

import pandas as pd
import numpy as np

Decription: This program will learn to classify fortune cookies as either good fortune or bad fortunes by 
	    reading a fortune cookie sentence. First the program will remove any stop words from the fortune
            cookies text and will then begin to find a hyperplane that seperates the fortune cookies using
	    the single perceptron, the averaged perceptron, and a multiclass perceptron. The training and 
	    testing accuracies are written out to a file called output.txt.

Functions included in this program:

def vocab(file):
    '''
    A function that reads in and stores all the words in a file
    Parameters:
    file: A string that represents the file to be processed
    Returns: A list of all the word in the file
    '''

def label(file):
    '''
    A function that reads a file and stores all the values as classifyer labels.
    This fuction also converts all 0 to -1 for the binary classsifier.
    file: A string that represents the file to be processed
    Returns: A list of all the word in the file
    '''

def clean_vocab(vocab,stop_words):
    '''
    A function that removes the specified stop words from a list of words.
    Parameters:
    vocab: A list of all vocab words
    stop_words: A list of words to remove from the lsit of vocab words
    Returns: A list of words that do not contain the stop words
    '''

def matrix(file,new_vocab,stop_words):
    '''
    A function that creates a bitmap data frame to represent the data from a file.
    Parameters:
    file: A str representation of the file name or path
    new_vocab: A list of vocab words that have the stop words removed
    Returns: A data frame that represents a bitmap of the words in the file
    '''

def make_df(file):
    '''
    A function that makes a a data frame to hold the information from the file
    Parameters:
    file: A str that represent the name of the file to make into a data frame.
    Returns: A data frame representing the file.
    '''

def make_dict(df):
    '''
    A function that creates a dictionary to hold the current weighted vector of a
    sepcific class in the form of {class:[vector,survival]}.
    Parameters:
    df: A dataframe to be used for creating the dictionary
    Returns a dictionary in the form of {class:[vector,survival]}
    '''

def make_dict_avg(df):
    '''
    A function that creates a dictionary to hold all the weighted vectors of a
    sepcific class in the form of {class:[vector,survival,vector,survival]}.
    Parameters:
    df: A dataframe to be used for creating the dictionary
    Returns a dictionary in the form of {class:[vector,survival]}
    '''

def argmax(d,row):
    '''
    A function that computes the score of all weighted vectors agiant a specific
    class vector.
    Parameters:
    d: a dictionary that hold the current weighted vectors in the form
       {letter,[weighted_vector,survival]}
    row: the specific vector to classify
    Returns: the label associated with the weighted vector who created the max score.
    '''

def build_weight_binary(weights):
    '''
    A function that calculates the averaged weighted vector.
    Parameters:
    weights: A list of weighted vecotors and survival times used to compute the average weighted vector.
    Returns: An averaged weighted vector to be used for classification.
    '''

def build_weight(weights):
    '''
    A function that will compute the average weight of each class vector.
    Parameters:
    weights: A Dictionary that holds the logged weighted vectors and thier survival times.
    Returns: A dictionary thtat holds the averaged weighted vectors of each class.
    '''

def stop_words_list(file):
    '''
    A function the reads in all the stop words from a file.
    Parameters:
    file: A str that represents a file name or path.
    Returns: A list of words in the file
    '''

def perceptron_binary(df,T,Learn,df_label,testdf,testlabel):
    '''
    A function that trains and tests a standard binary classifier perceptron
    Parameters:
    df: A data frame containing the training data.
    T: The max number of iterations.
    df_label: A data frame that contains the labels for the training data.
    testdf: A data frame that contains the testing data.
    testlabel: A data frame that contains the labels for the testing data.
    Returns: A tuple containing a list that represents the weighted vector to 
             be used for classification, and eh training accuaracy.
    '''

def avg_perceptron_binary(df,T,Learn,df_label,testdf,testlabel):
    '''
    A function that creates a averaged binary perceptron given the following parameters
    Parameters:
    df: A data frame containing the training data
    T: The max number of iterations
    df_label: A data frame that contains the labels for the training data
    testdf: A data frame that contains the testing data
    testlabel: A data frame that contains the labels for the testing data
    Returns: A tuple containing a list of the averaged weighted vector and the
             the testing accuracy.
    '''

def test_binary(df,df_label,w):
    '''
    A function that counts the number of mistakes made during testing
    Parameters:
    w: A vector of weights to be used for classification
    Returns: An integer that represents the number of mistakes made during testing
    '''

def perceptron(df,df_test,Learn,T):
    '''
    A function that creates a perceptron given the following parameters
    Parameters:
    df: A dataframe containing the training data
    df_test: A data frame containing the testing data
    Learn: The learning rate to be used in training
    T: max number of iterations to perform
    Returns: a dictionary with the weighted vectors of each class
    '''

def perceptron_avg(df,df_test,Learn,T):
    '''
    A function that creates a averaged multiclass perceptron given the following parameters
    Parameters:
    df: A dataframe containing the training data
    df_test: A data frame containing the testing data
    Learn: The learning rate to be used in training
    T: max number of iterations to perform
    Returns: a dictionary with the averaged weighted vectors of each class
    '''

def test(df,w):
    '''
    A function used to count the number of mistakes made during testing.
    Parameters:
    df: A data frame containing the testing data.
    w: the averaged weighted vectors to be used in testing.
    Returns: A integer that represents number of mistakes
    '''

def write_out(file,mistakes,accuracy,which,how,avg_acc):
    '''
    A function that writes the output metrics to a file named "output.txt"
    Parameters:
    file: A str representing the file name or file path
    mistakes: A list that holds the numbers of mistakes made during training
    accuracy: A dictionary that hold the accuracy during training and testing
    which: A str that indicates which perceptron to write results for
    how: A str that is either 'w' or 'a' this determines if the file is to be in write mode or append mode
    avg_acc: A float that is representing the accuracy of the averaged perceptron after T iterations
    '''