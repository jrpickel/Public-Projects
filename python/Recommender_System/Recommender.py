import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def mean(df_tabular):
    '''
    A function who subtracts the movies average rating from each rating
    Parameters:
    df_tabular: A datafram that hold all movie rating by a user in the form
                Index: movieId 
                Columns: userId 
                Cell: rating
    Returns:
    df: A dataframe in the same form as the input but the ratings will reflect 
        the subtraction of the mean.
    '''
    print("Creating dataframes.....\n")
    # create a deep copy to aviod aliasing
    df = df_tabular.copy(deep=True)
    # loop through all the movies and subtract the movies mean from the movies
    # ratings
    for i in df.index:
        avg = df.loc[i].mean() # calculate the average
        df.loc[i] = df.loc[i] - avg # subtract the avg fromt the row
    return df

def predict(df_sim,df_tabular,N):
    '''
    A function that will grab all users who do not have a rating for a movie.
    The function will then grab the top 5 most similar movies to a movie and 
    grab the users who we can predict a value for the movie. The function then
    calculates the predict value for the movie across all users.
    Parameters:
    df_sim: a dataframe that hold the similarity scores across all movies
    df_tabular: A dataframe that hold all the ratings a user gave a movie
    N: Is an int that determine the size of the neighbor set
    Returns:
    final_predict: A dictionary of the form {userId:{movieId:predicted_rating}}
    '''
    # dictionary to hold predictions in the form {movieId:{userId:predicted_value}}
    rating_predict = {}
    print("Calculating predictions....."+"\n")
    # loop through all movies
    for i in df_sim.index.tolist():
        # grab top 5 most similar movies to current movie "i"
        top_5 = df_sim.loc[i,df_sim.columns != i].sort_values(ascending=False).iloc[0:N] # Change for neighbors !!!!!!
        # assign df_tabular to users for reference throughout this functionn
        users = df_tabular
        # grab users without a rating for the given movie "i"
        wanted_users = users.loc[i,users.loc[i,].values == 0]
        # grab the ratings of the most similar movies to movie "i" from users who have not rated movie "i"
        users = users.loc[top_5.index,wanted_users.index].loc[top_5.index,]
        # calculate predicted scores for current movie "i" for users without ratings for movie "i"
        temp = round((users.multiply(top_5,axis=0).sum(axis=0))/sum(top_5),4)
        # store results in a dict as a series
        rating_predict[i] = temp
    # convert result dictionary to dataframe
    ratings_matrix = pd.DataFrame(rating_predict)
    # dictionary to hold predictions in the form {userId:{movieId:predicted_value}}
    final_predict = {}
    # loop through all users and grab the top 5 highest predicted movies
    for j in ratings_matrix.index:
        # grab the top 5 movies for a user and store result as a series
        temp = ratings_matrix.loc[j].sort_values(ascending=True)
        # store predicted values in a dict with the value as a dict in the form {userId:{movieId:predicted_rating}}
        final_predict[j] = sort_Values(temp)
    return final_predict

def sort_Values(series):
    '''
    A function used to sort the recommended movie's.
    Parameters:
    series: a series that holds the movie's and ratings for a user.
    Returns:
    new_vals: The top 5 recommended movies.
    '''
    # convert the series to a dictionary of the form {movieId:rating}
    vals = series.to_dict()
    # sort by ratings in ascending order.
    new_vals = {k:v for k,v in sorted(vals.items(), key= lambda item: (item[1],item[0]),reverse = False )}
    # sort by movieId in descending order.
    new_vals = {k:v for k,v in sorted(vals.items(), key= lambda item: item[1],reverse = True )}
    # grab the top 5 entries
    new_vals = {k:v for k,v in list(new_vals.items())[0:5]}
    return new_vals

def write_out(final_predict,file):
    '''
    A function used to write results toa file name 'output.txt'
    Parameters:
    final_predict: A diction of the form {userId:{movieId:prediction_value}}
    '''
    # open a file named 'output.txt' in write mode
    file = open(file,"w")
    # loop through all the dictionaries entries
    for i in final_predict.keys():
        # create a list that will hold userId and movieId's
        temp = [i]
        # extend the list to include all values 
        temp.extend(list(final_predict[i]))
        # convert the lsit of int's to string representation
        res = (" ").join([str(elem) for elem in temp])
        # write the values in the list out to the file
        file.write(res +"\n")
    # close the file
    file.close()
    print("The program has finished"+ "\n")
    return

def main():
    while True:
        print( "\nPress 'q' at any prompt to quit")
        file = input("\nEnter the file of the dataset (assume relative path) (e.x. ratings.csv): ")
        if file == "q":
            print( "Quitting Program")
            break
        outfile = input("Enter file name for output (assume relative path): ")
        if outfile == "q":
            print( "Quitting Program")
            break
        N = int(input("Size of neighbor set: "))
        print("\n")
        if N == "q":
            print( "Quitting Program")
            break
        
        # read excel data
        df = pd.read_csv(file,header = 0)
        
        # pivot the table
        df_tabular = df.pivot(index='movieId',columns='userId',values='rating')
        
        # the replacement value used for non ratings.
        key = 0
        
        # labels
        rows = df_tabular.index.tolist()
        
        # subtract mean from row
        df2 = mean(df_tabular)
        df2 = df2.fillna(key)
        
        # calculate the cosine similarity scores
        res = cosine_similarity(df2.values.tolist())
        
        # turn the similarity matrix into the dataframe
        df_sim = pd.DataFrame(res,columns=[i for i in rows],index=[i for i in rows])
        
        # fill values with 0
        df_tabular = df_tabular.fillna(0)
        
        # create predicts for users
        predictions = predict(df_sim,df_tabular,N)
        
        # write results to a file named "output.text"
        write_out(predictions,outfile)        