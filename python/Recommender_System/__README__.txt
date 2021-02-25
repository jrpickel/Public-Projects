Libraries that are used in this program are as follows:

pandas
numpy
sklearn

The following sklearn method is used in the program:

from sklearn.metrics.pairwise import cosine_similarity

In order to run this program you can call the program name from the terminal as long as you are in the appropiate directory.
Once you run the program you will need to supply the following inputs:
The file of the dataset (assume relative path) (e.x. ratings.csv)
The file name for output (assume relative path) (e.x. output.txt)
The size of the neighbor set (e.x. 5)

Once all of these inputs are accepted the program will execute by first calculating the similarity scores for every item (movie).
Then the program will go through all the items (movies) find all the users who currently have not rated the item (movie) and then
select the top N (user specified size of neighbor set) most similar movies and calulate the predicted score for the user.
After the program has made all of its predictions it will dump the top 5 recomended movie's (movieId) for all users (userId) to the specified output file.

######################################## Information about the algorithm ########################################
This program built the items profile using the ratings for the item (movie).

This program calculates the similarity score by using the centered cosine similarity formula.

This item-item collaborative algorithm selects the top N (user specified size of neighbor set) similar movies
independent of user ratings to calculate the predicted rating of the movie for a specfic user.
#################################################################################################################
