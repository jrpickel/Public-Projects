import pandas as pd
import numpy as np

def vocab(file):
    '''
    A function that reads in and stores all the words in a file
    Parameters:
    file: A string that represents the file to be processed
    Returns: A list of all the word in the file
    '''
    vocab = []
    fileV = open(file,"r")
    for line in fileV:
        line = line.strip()
        temp = line.split(" ")
        vocab.extend(temp)
    return vocab

def label(file):
    '''
    A function that reads a file and stores all the values as classifyer labels.
    This fuction also converts all 0 to -1 for the binary classsifier.
    file: A string that represents the file to be processed
    Returns: A list of all the word in the file
    '''
    label = [] # empty list to store the lables
    fileL = open(file,"r")
    # loop through file and store the labels
    for line in fileL:
        line = line.strip()
        # convert the data from str to int
        if line == "1":
            label.append(1)
        # convert 0's to -1 for binary classifier
        else:
            label.append(-1)
    # create a data frome of the labels
    df_label = pd.DataFrame(label)
    return df_label

def clean_vocab(vocab,stop_words):
    '''
    A function that removes the specified stop words from a list of words.
    Parameters:
    vocab: A list of all vocab words
    stop_words: A list of words to remove from the lsit of vocab words
    Returns: A list of words that do not contain the stop words
    '''
    # remove stop words
    new_vocab = set(vocab) - set(stop_words)
    # sort the vocab words in alphabetical order
    new_vocab = sorted(list(new_vocab),reverse=False)
    return new_vocab

def matrix(file,new_vocab,stop_words):
    '''
    A function that creates a bitmap data frame to represent the data from a file.
    Parameters:
    file: A str representation of the file name or path
    new_vocab: A list of vocab words that have the stop words removed
    Returns: A data frame that represents a bitmap of the words in the file
    '''
    matrix = [] # an empty list to hold a list of binary values
    fileV = open(file,"r")
    # loop through the file and to compute the bitmap
    for line in fileV:
        array = [] # empty list that will hold the binary value if a word is present at the current line in the file.
        line = line.strip()
        temp = line.split(" ")
        temp = set(temp)-set(stop_words)
        # loop through the new_vocab words and see if the word exist at the current line 
        for j in new_vocab:
            # if the word does not exist at the current line then append a 0 to array
            if j not in list(temp):
                array.append(0)
            # else append a 1 aka the word does exist
            else:
                array.append(1)
        # append the bitmap values of the current row to the ist "matrix"
        matrix.append(array) # has the form [[0,1,1...],[1...],..]
    # create a dataframe from the nested list matrix. 
    df = pd.DataFrame(matrix,columns=new_vocab)
    return df

def make_df(file):
    '''
    A function that makes a a data frame to hold the information from the file
    Parameters:
    file: A str that represent the name of the file to make into a data frame.
    Returns: A data frame representing the file.
    '''
    images = [] # holds the 128 pixels of an image
    labels = [] # hold the specified label of the image
    file = open(file,'r')
    # loop through file and parse based on observation of file
    for line in file.readlines():
        temp = line.split("\t")
        if len(temp[1]) != 0:
            images.append(list(temp[1].strip("im")))
            labels.append(temp[2])
    # create a data frame using the information in the file
    df = pd.DataFrame(images[0:-1])
    # add a column named label to the data frame
    df['label'] = labels[0:-1]
    # convert data type of the pixels to an integer
    df.loc[:,df.columns[0:-1]] = df.loc[:,df.columns[0:-1]].astype('int')
    return df

def make_dict(df):
    '''
    A function that creates a dictionary to hold the current weighted vector of a
    sepcific class in the form of {class:[vector,survival]}.
    Parameters:
    df: A dataframe to be used for creating the dictionary
    Returns a dictionary in the form of {class:[vector,survival]}
    '''
    features = (df.shape[1])-1
    my_dict = {}
    keys = np.sort(df.label.unique())
    for i in keys:
        #my_dict[i] = np.array([0 for i in range(features)])
        my_dict[i] = [np.array([0 for i in range(features)]),1]  # used for average perceptron
    return my_dict

def make_dict_avg(df):
    '''
    A function that creates a dictionary to hold all the weighted vectors of a
    sepcific class in the form of {class:[vector,survival,vector,survival]}.
    Parameters:
    df: A dataframe to be used for creating the dictionary
    Returns a dictionary in the form of {class:[vector,survival]}
    '''    
    features = (df.shape[1])-1 # ignore the label column
    my_dict = {} # blank dictionary to hold the information
    keys = np.sort(df.label.unique()) # grab the unique labels
    for i in keys:
        my_dict[i] = []  # used for average perceptron
    return my_dict

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
    max_ = 0
    vector = [] # list that holds the label of the weighted vector who scored higher than max
    # loop through all vectors and see who created the hightest score.
    for i in d.keys():
        val = d[i][0].dot(row[0:-1])
        if len(vector) == 0: # if the list is empty append the first calculation as the max
                max_ = val
                vector.append(i)
        else:
            if val > max_: # if new score is greater than max replace the value of max
                vector.pop() # remove the current max and replace with new label
                max_ = val # replace the current max score
                vector.append(i) # append the label associated with the max score
    return vector[0]

def build_weight_binary(weights):
    '''
    A function that calculates the averaged weighted vector.
    Parameters:
    weights: A list of weighted vecotors and survival times used to compute the average weighted vector.
    Returns: An averaged weighted vector to be used for classification.
    '''
    temp = 0
    # loop through all stored vectors with survival times and calculate the average
    for i in weights:
        temp = temp + (i[0] * i[1])
    return temp

def build_weight(weights):
    '''
    A function that will compute the average weight of each class vector.
    Parameters:
    weights: A Dictionary that holds the logged weighted vectors and thier survival times.
    Returns: A dictionary thtat holds the averaged weighted vectors of each class.
    '''
    new_dict = {} # new dictionary that will hold the averaged weighted vectors
    # loop through every class to calculate the averaged weighted vector
    for i in weights.keys():
        temp = 0
        new_dict[i] = []
        denom = len(weights[i])
        # loop through every vector that has been logged
        for j in weights[i]:
            # calculate the averaged weighted sum of the weighted vectors
            temp = temp + (j[0] * j[1])
        # append the average weighted vectors to the dictionary
        new_dict[i].append(temp/denom)
    return new_dict

def stop_words_list(file):
    '''
    A function the reads in all the stop words from a file.
    Parameters:
    file: A str that represents a file name or path.
    Returns: A list of words in the file
    '''
    stop_words = [] # empty lmist to hold the stop words
    fileS = open(file,"r")
    # loop through all lines in the file and store the words in the list "stop_words"
    for line in fileS:
        stop_words.append(line.strip())
    return stop_words

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
    print("\nTraining binary perceptron...\n")
    mistakes = []
    accuracy = {'train': [],'test': []}
    # initilize the weight vector to be all zeros
    w = np.array([0 for i in range(df.shape[1])])
    train_rows = df.shape[0] # number of row in the training data frame
    test_rows = testdf.shape[0] # number of row in the testing data frame    
    # start max iter
    for i in range(T):
        count = 0 # initilize a mistake counter
        # loop through all rows in the training data
        for j in range(0,322):
            yt = df_label.loc[j].values # The true training label
            xi = df.loc[j].values # the vector to be calssified
            y_hat = np.sign(np.array(w).dot(xi)) # predicted value of the vector
            # if mistake then update weights and increase mistake count
            if (y_hat != yt):
                count += 1
                w = w + ((Learn*yt)*xi) # update weight vector
        # test perceptron
        mistakes.append(count) # keep track of number of mistakes made
        print("standard perceptron iter-{} num-mistakes-{}".format(i+1,count))
        wrong = test_binary(testdf,testlabel,w) # number of mistakes made during testing
        train_acc = round(((train_rows - count) / train_rows)*100,4) # compute train accuracy
        test_acc = round(((test_rows - wrong) / test_rows)*100,4) # compute test accuracy
        accuracy['train'].append(train_acc) # store train accuracy
        accuracy['test'].append(test_acc) # store train accuracy
        print("standard perceptron iter-{} training-accuracy {:.4f}% testing-accuracy {:.4f}%".format(i+1,train_acc,test_acc))
    print("training-accuracy-standard-perceptron {:.4f}% testing-accuracy-averaged-perceptron {:.4f}%".format(train_acc,test_acc))
    avg_acc = avg_perceptron_binary(df,T,Learn,df_label,testdf,testlabel)[1] # accuracy for average perceptron during testing
    which = "Binary Perceptron" # section name for output file
    how = 'w' # mode for output file
    write_out("output.txt",mistakes,accuracy,which,how,avg_acc) # write out the results
    return w,train_acc

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
    # initilize all class weights to zero and survival time to one.
    w = np.array([0 for i in range(df.shape[1])]) # weights that set to zero
    train_rows = df.shape[0] # number of row in the training data frame
    test_rows = testdf.shape[0] # number of row in the testing data frame      
    cm = 1 # survival time
    weights = [] # empty list to hold the log of weights and survival times
    print("\nTraining average binary perceptron...\n")
    for i in range(T):
        count = 0 # initilize the mistakes to zero
        # loop through all the rows in the training data frame.
        for j in range(0,322):
            yt = df_label.loc[j].values # actual label of the vecotr to be classified
            xi = df.loc[j].values # the vector to classify
            y_hat = np.sign(np.inner(w,xi)) # predicted class of the vector "xi"
            # if mistake then update the weights
            if (y_hat != yt):
                count +=1 # increment mistake counter
                weights.append((w,cm)) # log the weights before updating
                w = w + ((Learn*yt)*xi) # update the weight vector
                cm = 1 # reset the survival time
            else:
                cm += 1 # increment the survival time 
        print("standard perceptron iter-{} num-mistakes-{}".format(i+1,count))        
        weights.append((w,cm)) # append the last weights to include ina verage calculation
        new_w = build_weight_binary(weights) # new_w variable holds the averaged weighted vector
        # test the perceptron using the averaged weights
        wrong = test_binary(testdf,testlabel,new_w)
        train_acc = round(((train_rows - count) / train_rows)*100,4) # compute train accuracy
        test_acc = round(((test_rows - wrong) / test_rows)*100,4) # compute training accuracy
        print("standard perceptron iter-{} training-accuracy {:.4f}% testing-accuracy {:.4f}%".format(i+1,train_acc,test_acc))
    print("training-accuracy-standard-perceptron {:.4f}% testing-accuracy-averaged-perceptron {:.4f}%".format(train_acc,test_acc))
    return new_w,test_acc

def test_binary(df,df_label,w):
    '''
    A function that counts the number of mistakes made during testing
    Parameters:
    w: A vector of weights to be used for classification
    Returns: An integer that represents the number of mistakes made during testing
    ''' 
    # strat a mistake counter at zero
    wrong = 0
    # loop through all testing data 
    for j in range(df.shape[0]):
        yt = df_label.loc[j].values
        xi = df.loc[j].values
        y_hat = np.sign(np.inner(w,xi))
        # if mistake then increase number of mistakes made
        if y_hat != yt:
            wrong += 1
    return wrong

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
    mistakes = []
    accuracy = {'train': [],'test': []}    
    weight_dict = make_dict(df) # create the weighted dictionary
    train_rows = df.shape[0] # number of row in the training data frame
    test_rows = df_test.shape[0] # number of row in the testing data frame
    print("\nTraining multiclass perceptron...\n")
    # start max iter
    for i in range(T):
        count = 0
        # loop through all rows of data
        for j in range(df.shape[0]):
            row = df.loc[j,df.columns]
            y_hat = argmax(weight_dict,row)  # determine which class produced the max score
            yt = row['label'] # varible to hold the true label
            # if predicted label is not equal to true label update weights
            if y_hat != yt:
                cm = weight_dict[yt][1] # grab survival time will always be one for non average perceptron
                # update weights and reset survival time
                weight_dict[yt][0] = (cm*weight_dict[yt][0]) + np.array(Learn*row[0:-1]) 
                weight_dict[y_hat][0] = (weight_dict[y_hat][0]) - np.array(Learn*row[0:-1])
                count += 1 # count number of mistakes
        mistakes.append(count) # keep track of number of mistakes made
        # compute training accuracy and testing accuracy
        train_acc = round(((train_rows-count)/train_rows)*100,4) # compute train accuracy
        print("iteration-{} no-of-mistakes {}".format(i+1,count))
        test_mistake = test(df_test,weight_dict) # test the perceptron and record how many mistakes are made
        test_acc = round(((test_rows-test_mistake)/test_rows)*100,4) # compute test accuracy
        accuracy['train'].append(train_acc) # store train accuracy
        accuracy['test'].append(test_acc) # store test accuracy      
        print("iteration-{} training-accuracy {:.4f}% testing-accuracy {:.4f}%\n".format(i+1,train_acc,test_acc))
    avg_acc = perceptron_avg(df,df_test,Learn,T)[1] # accuracy for average perceptron during testing
    which = "Multiclass Perceptron" # section name for output file
    how = 'a' # mode for output file
    write_out("output.txt",mistakes,accuracy,which,how,avg_acc) # write out the results
    return weight_dict

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
    weight_dict = make_dict(df) # create the weighted dictionary
    weight_dict_avg = make_dict_avg(df) # create a dictionary to hold the log of weights and survival times
    train_rows = df.shape[0] # number of row in the training data frame
    test_rows = df_test.shape[0] # number of row in the testing data frame
    print("\nTraining average multiclass perceptron...\n")
    # start max iter
    for i in range(T):
        count = 0 
        cm = 1
        # loop through all rows in the data frame
        for j in range(df.shape[0]):
            row = df.loc[j,df.columns] # vector to classify
            y_hat = argmax(weight_dict,row) # compute predicted class label
            yt = row['label'] # true class label
            # if predicted label is not equal to true label update weights
            if y_hat != yt:
                # append old weights to the average dictionary to log them for later
                weight_dict_avg[yt].append([weight_dict[yt][0],weight_dict[yt][1]])
                weight_dict_avg[y_hat].append([weight_dict[y_hat][0],weight_dict[y_hat][1]])
                # update current weights and reset survival to 1
                weight_dict[yt][0] = (weight_dict[yt][0]) + np.array(Learn*row[0:-1])
                weight_dict[yt][1] = 1
                weight_dict[y_hat][0] = (weight_dict[y_hat][0]) - np.array(Learn*row[0:-1])
                weight_dict[y_hat][1] = 1
                count += 1 # count number of mistakes
            else:
                # if weighted vector survived increase survival count
                weight_dict[y_hat][1] += 1
        # append the last updated weights to the average weight dictionary to log for later       
        weight_dict_avg[yt].append([weight_dict[yt][0],weight_dict[yt][1]])
        weight_dict_avg[y_hat].append([weight_dict[y_hat][0],weight_dict[y_hat][1]])    
        # calculate the average weight vector for each class to use in testing
        new_w = build_weight(weight_dict_avg)
        # test the average weightedd vector agiasnt the test data
        train_acc = round(((train_rows-count)/train_rows)*100,4) # compute training accuracy
        print("iteration-{} no-of-mistakes {}".format(i+1,count))
        test_mistake = test(df_test,new_w) # record how many mistakes were made during training
        test_acc = round(((test_rows-test_mistake)/test_rows)*100,4) # compute testing accuracy
        print("iteration-{} training-accuracy {:.4f}% testing-accuracy {:.4f}%\n".format(i+1,train_acc,test_acc))
    return new_w,test_acc 

def test(df,w):
    '''
    A function used to count the number of mistakes made during testing.
    Parameters:
    df: A data frame containing the testing data.
    w: the averaged weighted vectors to be used in testing.
    Returns: A integer that represents number of mistakes
    '''
    count = 0 # start mistake counter
    # loop through all rows in testing data frame
    for i in range(df.shape[0]):
        row = df.loc[i,df.columns]
        y_hat = argmax(w,row)
        yt = row['label']
        # if mistake then increment mistake count
        if y_hat != yt:
            count += 1
    return count

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
    output = open(file,how) # open file
    count = 1 # start count for iteration
    keys = list(accuracy.keys()) # grabs the keys of the dictionary
    # if in append mode create a space
    if how == 'a':
        output.write("\n")
    output.write("Metrics for %s\n"%(which)) # write header for section
    for i in mistakes: # write out the mistakes for each iteration
        output.write("iteration-{} {}\n".format(count,i))
        count += 1
    output.write("\n")
    count = 1
    for j in range(len(accuracy[keys[0]])): # write out the accuracies for each iteration for training and testing
        output.write("iteration-{} {:.4f}% {:.4f}%\n".format(count,accuracy['train'][j],accuracy['test'][j]))
        count += 1
    # write out the accuaracy for standard perceptron during testing and accuracy for averaged perceptron during testing. 
    output.write("\n{:.4f}% {:.4f}%\n".format(accuracy['train'][-1],avg_acc))
    output.close()
    
def main():
    stop_words = stop_words_list("stoplist.txt") # create lis tof stop words
    traindata = vocab("traindata.txt") # create a list of vocab words from the training data
    trainclean = clean_vocab(traindata,stop_words) # remove stop words from the vocab words 
    trainmatrix = matrix("traindata.txt",trainclean,stop_words) # create a data frame that represents the training data
    trainlabel = label("trainlabels.txt") # create a data frame that stores the labels for the training data
    
    testdata = vocab("testdata.txt") # create a list of vocab words from the testing data
    testclean = clean_vocab(testdata,stop_words) # remove the stop words from the testing vocab 
    testmatrix = matrix("testdata.txt",trainclean,stop_words) # create a data frame that represents the testing data
    testlabel = label("testlabels.txt") # create a data frame that stores the labels for the testing data
    
    stand_w = perceptron_binary(trainmatrix,20,1,trainlabel,testmatrix,testlabel) # execute the standard binary classifier
    
    df_train = make_df("ocr_train.txt") # make the training data frame
    df_test = make_df("ocr_test.txt") # make the testing data frame
    weights = perceptron(df_train,df_test,1,20) # train and build a standard multiclass perceptron

main()

#df_train = make_df("ocr_train.txt") # make the training data frame
#df_test = make_df("ocr_test.txt") # make the testing data frame
#w,acc,avg = perceptron_avg(df_train,df_test,1,20) # train and build a standard multiclass perceptron