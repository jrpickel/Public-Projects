Libraries Used:

from itertools import combinations 
from collections import Counter 
import time

Description:
	This program will take in a file of transtions, compute frequent items,
	frequent item pairs and frequent item triples. The program will then calculate
	the probabilities associated to the rules. After the calculations are done the
	results are outputed to a file named "output.txt" which is located in the current
	working directory.

Functions use din the program:

def read_data(file,sep):
    '''
    This function will read in data from the given file and create three items.
    The first item is the trasaction data which will be stored as a nested list
    of tuples and all items will be converted to a numerical representation. The numerical
    representation is based on the occurence of the item. The second item is a 
    dictionary which will hold all the items as the key and the numerical 
    representation of the item as the value. The third item is another dictionary
    which will hold the numerical representation of an item as the key and the
    frequency of that item as the value. This item will serve as the Canidate keys
    Parameters:
    file: the file to be processed
    sep: the deliminator the file uses to seperate transactions
    Returns:
    A tuple consisting of a list named "browsing_data", a dictionary named "items",
    and another dictionary named "C1"
    '''

def make_C2(data,L1_ref):
    '''
    This function will create all Canidate keys of size 2 and store thier 
    frequency in a triangular matrix. 
    Parameters:
    data: this is all the transaction baskets
    L1_ref: this is the reference dictionary containing a new reference number to 
         the old reference numbers. (used for triangle matrix formula) 
    Returns:
    A triangle matrix with frequency count stored in each element.
    '''

def triangle_index(i,j,n):
    '''
    Helper function used calculate the index of the triangle matrix
    Parameters: 
    i: first element of the pair
    j: Second element of the pair
    n: size of the matrix
    Returns:
    an integer value that indicates the index of the triangle matrix to store the frequency
    '''

def make_triangle(n):
    '''
    Helper function used to create a triangle matrix that is the appropiate size
    Parameter:
    n: the size to make the triangle matrix
    Returns:
    List of size n filled with zeros 
    '''

def find_og_value(d,val):
    '''
    Helper function to convert newest number representation back to the old numbers
    Parameters:
    d: dictionary containing oldnumber(key):newnumber(value)
    val: new number reference that will be used to return the old number reference
    Returns:
    the original value stored in the dictionary
    '''

def make_C3(L2,data):
    '''
    A function that will make all possible triples from the frequent doubles.
    This function will also go through each basket and generate all possible 
    triples within the basket. It then takes the intersection of the possible triples and
    the triples from the basket and counts the those triples.
    Parameters:
    L2: dictionary of frequent pairs in the form {(item1,item2):frequency....}
    data: this is all the transaction baskets
    Returns:
    dictionary named "freq" which is in the form {(item1,item2,item3):frequency.....}
    '''

def make_L(C1,s):
    '''
    A function that removes any items with a frequency less than support
    Parameters:
    C1: dictionary that represents the candidate items either single or triple
    s: integer that represents min support
    '''

def make_L2(triangle,L1_ref,support):
    '''
    A function that will create a dictionary to that holds the frequent doubles.
    This funtion takes in a triangle amtrix and produces a dictionary.
    Parameters:
    trianlge: A triangle amatrix containing the frequency of a pair
    L1_ref: A dictionary that holds the old number as a key and the new number as
            a value
    support: an integer defining the min support level
    '''

def make_ref_dict(L1):
    '''
    A function that makes a reference dictionary to hold old numbers and new numbers
    Parameters:
    L1: A dictionary that holds the old number as the key and the old number
        as the value
    Returns:
    new_dict: A new dictionary that holds the old number as the key and the 
              old number as the value
    '''

def confidence_double(ref,L1,L2):
    '''
    This function calculates the confidence for the rules x=>y and y=>x of all
    frequent pairs.
    Parameters:
    ref: a dictionary that contains the items as the key and number reference of
         the item as the value in the form {item1:reference number}
    L1: A dictionary that cotains the frequent singles in the form {item1:frequency}
    L2: A dictionary that contains the frequent doubles in teh form {(item1,item2): frequency}
    Returns:
    double: A Dictionary containing the pair as the key and the confidence as the value
            if the form {(item1,item2): confidence}
    '''

def confidence_trip(ref,L2,L3):
    '''
    This function calculates the confidence for the rules (x,y)=> z , (x,z)y=> y
    (y,z)=> x of all frequent triples.
    Parameters:
    ref: a dictionary that contains the items as the key and number reference of
         the item as the value in the form {item1:reference number}
    L2: A dictionary that contains the frequent doubles in the form 
        {(item1,item2): frequency}
    L3: A dictionary that contains the frequent triples in the form 
        {(item1,item2,item3): frequency}
    Returns:
    triples: A Dictionary containing the triples as the key and the confidence as the value
            if the form {(item1,item2,item3): confidence}
    ''' 

def grab_top_five(d):
    '''
    This is a helper function who grabs the first five entries of a dictionary
    Parameters:
    d: a dinctionary
    '''

def convert(ref,d):
    '''
    Helper function used to convert reference numbers into items
    Parameters:
    ref: a dictionary containing items naem as key and reference number as value
    d: A dictionary containg pair or triple as kay and confidence as the value
    Returns:
    results: a dictionary with pair or triple as key and confidence as value
    '''

def write_out(doubles,triples):
    '''
    A function that writes the key and value of a dictionary to a file
    Paramaeters:
    doubles: a dictionary containing doubles as the key and confidence as the value
    triples: a dictionary containing triples as the key and confidence as the value
    '''


