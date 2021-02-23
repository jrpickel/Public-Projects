Description: This program will read twitter feeds from a text file. When two
              files are given the program will sort each file and  then merge the two files
              by the time(including year,month,day,time)) of the tweet. The program will then return a new
              file containing the merged and sort tweets. The most recent tweet
              will be at the top.

Functions in the program:

def read_records(filename):
    '''a function that given a filename creates a Scanner object and creates a record for each line in the file and returns a list containing the records
    Parameter filename: name of file that you want to read from.
    Returns: a list of records each record being a single line from the file.
    '''

def insert_sort(A):
    '''Function used to insure each file is pre sorted
    Paratmeter A: an array to perform insertion sort on
    '''

def create_record(sobj):
    '''a function that takes in a Scanner object and creates a record then returns a list representing the record
    Parameter sobj: scanner object
    Returns: a list containg the fields tweeter,tweet,date.
    '''

def is_more_recent(record1,record2):
    '''a function that compares two records based on date and returns True if the first record is more recent than the second and False otherwise
    Parameter record1: the first record to compare.
    Parameter record2: the second record to compare aginast
    Returns: a boolean value
    '''

def merge_and_sort_tweets(list1,list2):
    ''' a function that merges two lists of records based placing more recent records before earlier records and returns the merged records as a single list
    Parameter list1: first list to pull from.
    Parameter list2: second list to pull from.
    Returns: a single merged list of tweets sorted in reverse chronological order from list1 and list2 
    '''

def int_to_str(elem):
    '''A function used to convert int data types into str data types
    Parameter elem: the element to check for int data types
    '''

def write_records(list1):
    '''a function that takes in a list of records and writes to the file output each record on it's own line.
    Parameter list1: the list in which we write from.
    Returns: a file named "sorted_tweets.txt" with text from list1
    '''

def most_tweets(list1,list2):
    '''A function that takes in two lists and compare the lengths of each. Depending on length
    a certain print function is displayed based on conditions.
    Parameter list1: first list to measure
    Parameter list2: second list to measure
    '''

def bottom_five(list1):
    '''A function that indexes the last 5 elements from a list and reference them
    in reverse order. Meaning the last element is presented first.
    Parameter merged_list: a list in which you want to index the last 5 elements
    '''

def main():
    '''
    At the command line move to the proper directory and type the following:
    tweet1.txt,tweet2.txt,twitter_sort.py
    '''