# ############################################################################
# Author: Justin Pickel
# Date: 9/20/2020
# Class: CS 315
# Assigment: PA1
# Description:
# This program will take in a file of transtions, compute frequent items,
# frequent item pairs and frequent item triples. The program will then calculate
# the probabilities associated to the rules. After the calculations are done the
# results are outputed to a file named "output.txt" which is located in the current
# working directory.
# ############################################################################

from itertools import combinations 
from collections import Counter 
import time

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
    browsing_data = [] # list that will hold all tranactions as a nested list of tuples
    items = {} # reference dictionary used to convert items to numbers and numbers back to items
    C1 = {} # frequency count of items
    # open file and read the file
    with open(file) as file:
        # start a count at 1 to represent the first item
        count = 1
        for i in file.readlines():
            # strip each line and seperate that line by the given seperator "sep"
            basket = i.strip().split(sep)
            # for each item in the basket add it to the dictionary "items" and 
            # store the current count as the value also add it to the dictionary "C1"
            # if it exist then increment its frequency count
            for i in range(len(basket)):
                # try and see it item already exists
                try:
                    items[basket[i]] # see if it exist in the dictionary "items"
                    basket[i] = items[basket[i]] # replace item in the file with the new number associated to that item
                    C1[basket[i]] += 1 # if the item exist in "C1" increment the count
                # except the error thrown if the item doesn't exist
                except KeyError:
                    # item doesnt exist create a number representing the item
                    items[basket[i]] = count
                    # replace item with number representation
                    basket[i] = count
                    # add item to "C1" and make its frequency 1
                    C1[basket[i]] = 1
                    # increment count
                    count +=1
            #Turn the nested list of lists into a list of tuples
            browsing_data.append(tuple(basket))
    return browsing_data,items,C1

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
    # size of triangle matrix
    n = len(L1_ref.keys())
    # create the triangle matrix with enough elements to store all possible pairs
    triangle = make_triangle(n)
    # step through easch basket and take the intersection of the basket and frequent singles
    # the intersection of these two will be what make the pairs.
    for i in data:
        i = sorted(i)
        pairs = set(list(L1_ref.keys())) # set of frequent singles
        intersec = pairs.intersection(set(i)) # intersection of baskt with frequent singles
        combos = list(combinations(tuple(sorted(intersec)),2)) # make all possible pairs from teh intersection
        # step through each combination made from above and incremnt the 
        # frequency of this pair in the triangle matrix
        for j in combos:
            first = L1_ref[j[0]] # first element of the pair
            second = L1_ref[j[1]] # second element of the pair
            idx = triangle_index(first,second,n) # find triangle index to store the frequency
            triangle[idx] += 1 # incremtn frequency at this location
    return triangle

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
    # minus one from calulated index since pair (1,2) is stored at 1 lets store it at 0
    idx = ((i-1)*(n-(i/2))+j-i)-1 
    return int(idx)

def make_triangle(n):
    '''
    Helper function used to create a triangle matrix that is the appropiate size
    Parameter:
    n: the size to make the triangle matrix
    Returns:
    List of size n filled with zeros 
    '''
    # number of all possible pairs
    size = int(n*(n-1)/2) 
    return  [0 for i in range(size)]

def find_og_value(d,val):
    '''
    Helper function to convert newest number representation back to the old numbers
    Parameters:
    d: dictionary containing oldnumber(key):newnumber(value)
    val: new number reference that will be used to return the old number reference
    Returns:
    the original value stored in the dictionary
    '''
    # index of the value
    idx = list(d.values()).index(val) 
    # use the index from above to grab the key located at this index
    og_value = list(d.keys())[idx] 
    return og_value

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
    freq = {} # empty dict to hold the triples adn frequency
    triples = [] # a list of all possible triples
    keys = sorted(L2.keys()) # a list of frequent doubles
    # loop thrugh each frequent double -1
    for i in range(len(keys)-1):
        # loop through each frequent foule starting with the next double
        for j in range(i+1,len(keys)):
            # interesct the two pairs
            intersect = set(keys[i]).intersection(set(keys[j]))
            # check to see if they share a common element
            if len(intersect) == 1:
                # union the two doubles
                un = set(keys[i]).union(set(keys[j]))
                #see if the symetric diffrence is a frequent pair
                diff = un ^ intersect
                if tuple(sorted(diff)) in keys:
                    # store the triple as possible
                    triples.append(tuple(sorted(un)))
    # get all unique triples
    triples = set(triples)
    # order all the triples
    triples = sorted(triples)
    # loop through each basket
    for i in data:
        # create all possible triples in the current bucket
        combos = list(combinations(tuple(sorted(i)),3))
        # make the combos into a set
        combos = set(combos)
        # intersect the tripes set from the bucket with the possible triples
        inter = combos.intersection(set(triples))
        # for each triple add to a dictionary "freq" and increment its value
        for j in inter:
            # try to increment count if not in dicttionary then add it
            try:
                freq[j] += 1
            # add to dictionary if not in dictionary
            except KeyError:
                freq[j] = 1            
    return freq

def make_L(C1,s):
    '''
    A function that removes any items with a frequency less than support
    Parameters:
    C1: dictionary that represents the candidate items either single or triple
    s: integer that represents min support
    '''
    # create a dictionary that only has keys and values where value is >= support
    return {key:val for key, val in C1.items() if val >= s}

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
    L2 = {} # empty dictionary that will hold the double as a key and frequency as the value
    n = len(L1_ref.keys())
    #sort the frequnecy 
    freq_singles = sorted(L1_ref.values())
    # make all pairs using the new number reference
    combos = combinations(freq_singles,2)
    # for each pair made look in the triangle matrix for the frequency of this pair
    for i in combos:
        # find what idex to look at
        idx = triangle_index(i[0],i[1],n)
        # check if the value in the trangle matrix is >= support
        if triangle[idx] >= support:
            # grab the old reference number
            first = find_og_value(L1_ref,i[0])
            second = find_og_value(L1_ref,i[1])
            # add this pair to the dictionary and store its frequency count
            L2[(first,second)] = triangle[idx]
    return L2 
    
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
    new_dict = {}
    # start count
    count = 1
    # each frequent single
    for i in L1.keys():
        # add the frequent single as to "new_dict" and store its value as count
        new_dict[i] = count
        count += 1
    return new_dict

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
    double = {} # create an empty dictionary
    # for each frequent pair
    for i in L2.keys():
        # calculate the rule x=>y
        numerator = L2[i]
        denominator = L1[i[0]]
        prob = round((numerator/denominator),4)
        double[i] = prob
        # calculate the rule y=>x
        denominator = L1[i[1]]
        prob = round((numerator/denominator),4)
        double[(i[1],i[0])] = prob
    double = convert(ref,double)
    double = {k: v for k,v in sorted(double.items(), key=lambda item: item[1], reverse = True)}
    double = grab_top_five(double)
    return double

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
    triples = {} # create an empty dictionary
    for i in L3.keys():
        x = i[0]
        y = i[1]
        z = i[2]
        # calculate the rule (x,y)=> z
        numerator = L3[i]
        denominator = L2[(x,y)]
        prob = round(numerator/denominator,4)
        triples[(x,y,z)] = prob
        # calculate the rule (x,z)y=> y
        denominator = L2[(x,z)]
        prob = round(numerator/denominator,4)
        triples[(x,z,y)] = prob
        # calculate the rule (y,z)=> x
        denominator = L2[(y,z)]
        prob = round(numerator/denominator,4)
        triples[(y,z,x)] = prob
    triples = convert(ref,triples)
    triples = {k: v for k,v in sorted(triples.items(), key=lambda item: (item[1],item[0]), reverse = False)}
    triples = grab_top_five(triples)
    return triples

def grab_top_five(d):
    '''
    This is a helper function who grabs the first five entries of a dictionary
    Parameters:
    d: a dinctionary
    '''
    top5_dict = [] # empty list
    # lexographically order the ties
    d = {k: v for k,v in sorted(d.items(), key=lambda item: (item[1]), reverse = True)}
    # grab the first 5 items
    count = 0
    maxx = 0
    for i in d.keys():
        temp = []
        key = i
        if count == 5:
            break
        if d[key] != maxx:
            maxx = d[key]
            value = d[key]
            temp.extend(key)
            temp.append(str(value))
            top5_dict.append(tuple(temp))
            count += 1
    return top5_dict

def convert(ref,d):
    '''
    Helper function used to convert reference numbers into items
    Parameters:
    ref: a dictionary containing items naem as key and reference number as value
    d: A dictionary containg pair or triple as kay and confidence as the value
    Returns:
    results: a dictionary with pair or triple as key and confidence as value
    '''
    results = {} # empty dictionary
    # for each key in the dictionary 
    for i in d.keys():
        items = []
        # for each element in the key
        for j in i:
            # find the index of the value 
            idx = list(ref.values()).index(j)
            # use index to find the key
            item = list(ref.keys())[idx]
            # add to the items list
            items.append(item)
        # convert list into tuple and store as the key in "results"
        # and add the confidence as the value
        results[tuple(items)] = d[i]
    return results
            
def write_out(doubles,triples):
    '''
    A function that writes the key and value of a dictionary to a file
    Paramaeters:
    doubles: a dictionary containing doubles as the key and confidence as the value
    triples: a dictionary containing triples as the key and confidence as the value
    '''
    # open file
    f = open("output.txt", "w")
    f.write("OUTPUT A\n")
    # write all the doubles to the file
    for i in doubles:
        f.write(" ".join(i)+"\n")
    f.write("OUTPUT B\n")
    # write all the triples to the file
    for i in triples:
        f.write(" ".join(i)+"\n")
    f.close()    

def main():
    while True:
        print( "\nPress 'q' at any prompt to quit")
        file = input("\nEnter file path (e.x. browsing-data.txt (no quotes)): ")
        if file == "q":
            print( "Quitting Program")
            break
        sep = input("Enter files deliminator character (e.x. just hit spacebar for ' ' equivilent): ")
        if sep == "q":
            print( "Quitting Program")
            break
        support = int(input("Min Support: "))
        print("\n")
        if support == "q":
            print( "Quitting Program")
            break
        # read data
        itemset,reference,C1 = read_data(file,sep)
        # make L1
        L1 = make_L(C1,support)
        # make L1_ref
        L1_ref = make_ref_dict(L1)
        # make C2 and L2
        C2 = make_C2(itemset,L1_ref)
        L2 = make_L2(C2,L1_ref,support)
        # make C3 and L3
        C3 = make_C3(L2,itemset)
        L3 = make_L(C3,support)
        # calculate rules for doubles and triples
        double_prob = confidence_double(reference,L1,L2)
        trip_prob = confidence_trip(reference,L2,L3)
        # write out results
        write_out(double_prob,trip_prob)
        print("The results are available to view in the file output.txt")

main()