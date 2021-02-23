from scanner import Scanner
import sys
# ########################################################################################
# Programmer: Justin Pickel
# Class: CptS 215 Fall 2019
# Programming Assignment #1
# 9/6/19
#
# Description: This program will read twitter feeds from a text file. When two
#              files are given the program will sort each file and  then merge the two files
#              by the time(including year,month,day,time)) of the tweet. The program will then return a new
#              file containing the merged and sort tweets. The most recent tweet
#              will be at the top.
# ########################################################################################

def read_records(filename):
    '''a function that given a filename creates a Scanner object and creates a record for each line in the file and returns a list containing the records
    Parameter filename: name of file that you want to read from.
    Returns: a list of records each record being a single line from the file.
    '''
    record_list = []                            # create a blank list.
    sorted_record = []
    s = Scanner(filename)                       # create a scanner object.
    for lines in open(filename).readlines():    # read every line as long as we have a line to read.
        temp = create_record(s)
        record_list.append(temp)                # append the current line to the blank list.
    sorted_list = insert_sort(record_list)
    return sorted_list

def insert_sort(A):
    '''Function used to insure each file is pre sorted
    Paratmeter A: an array to perform insertion sort on
    '''
    for e in range(-5,-1):                      # insertion sort algorithim from MIT press 3rd edition "introduction to algorithms" pg.18
        for j in range(1,len(A)):               # used this book in cs 122 data structures. to perform sorting.
            key = A[j][-e]                      # store a key value to compare
            i = j-1                             # i starts at the first element in the list
            while(i >= 0 and A[i][-e] < key):   # while the values need to be sorted continue to move the element higher up in the list
                temp = A[i+1]                   # keep memory of the element needing to be switched
                A[i+1] = A[i]                   # switch the memory slots
                A[i] = temp                     # assign the memory slot to the temporary value
                i -= 1                          # decrement i
            A[i+1][-e] = key                    # assign a new key to compare and continue the for loop
    return A                                    # return the sorted array

def create_record(sobj):
    '''a function that takes in a Scanner object and creates a record then returns a list representing the record
    Parameter sobj: scanner object
    Returns: a list containg the fields tweeter,tweet,date.
    '''
    record_list = []                # create a empty list to store the record fields.
    sobj.readchar()                     # move past the @ symbol.
    
    tweeter = sobj.readtoken()      # grab the tweeters name using scanner object.
    record_list.append(tweeter)         # append to list.
    
    tweet = sobj.readstring()       # grab the tweet using scanner object.
    record_list.append(tweet)           # append to list.
    
    year = int(sobj.readtoken())    # grab the year of the tweet using scanner object.
    record_list.append(year)
    
    month = int(sobj.readtoken())   # grab the month of the tweet using scanner object.
    record_list.append(month)
    
    day = int(sobj.readtoken())     # grab the day of the tweet using scanner object.
    record_list.append(day)
    
    time = sobj.readtoken()         # grab the time of the tweet using scanner object.
    record_list.append(time)

    return record_list              # returns the record into a list of the diffrent fields.

def is_more_recent(record1,record2):
    '''a function that compares two records based on date and returns True if the first record is more recent than the second and False otherwise
    Parameter record1: the first record to compare.
    Parameter record2: the second record to compare aginast
    Returns: a boolean value
    '''
    flag = True
    temp = " ".join(record1[2:])         # creat a temp variable to store the date(y+m+d+time)
    temp2 = " ".join(record2[2:])        # creat a temp variable to store the date(y+m+d+time)
    flag = True                          # initilze the varible "flag" to True.
    if temp < temp2:                     # if record1 is not more recent than record 2.
        flag = False                     # switch the "flag" variable to False.
    return flag                          # return the "flag" variable.
    
def merge_and_sort_tweets(list1,list2):
    ''' a function that merges two lists of records based placing more recent records before earlier records and returns the merged records as a single list
    Parameter list1: first list to pull from.
    Parameter list2: second list to pull from.
    Returns: a single merged list of tweets sorted in reverse chronological order from list1 and list2 
    '''
    newlist1 = [i for i in list1]                         # create copy of the lists being passed in so we can delete them as we sort and not affect our lists that we passed.
    newlist2 = [i for i in list2]
    merged_list = []                                      # make a blank list.
    while(len(newlist1) + len(newlist2) > 0):             # keep comparing and sort as long as we have something to compare and sort.
        if len(newlist1) == 0 and len(newlist2) != 0:     # case 1 if list1 is empty but list2 is not.
            temp1 = int_to_str(newlist2[0])               # make sure it is all str data type so we can perform .join on it.
            merged_list.append(" ".join(temp1))           # append the record from the list that is not empty.
            del(newlist2[0])
        elif len(newlist2) == 0 and len(newlist1) != 0:   # case 2 if list2 is empty and list1 is not.
            temp2 = int_to_str(newlist1[0])               # make sure it is all str data type so we can perform .join on it.
            merged_list.append(" ".join(temp2))           # append the record from the list that is not empty.
            del(newlist1[0])
        else:                                             # case 3 both lists1 and list2 are not empty.
            temprecord1 = int_to_str(newlist1[0])         # temporay record created from the first record in list 1.
            temprecord2 = int_to_str(newlist2[0])         # temporay record created from the first record in list 2.
            if is_more_recent(temprecord1,temprecord2):   # see if temprecord1 is before temprecord2.
                temp3 = int_to_str(temprecord1)           # make sure it is all str data type so we can perform .join on it.
                merged_list.append(" ".join(temp3))       # then append temprecord1 to our blank list.
                del(newlist1[0])                          # delete that record from our copied list1.
            else: 
                temp4 = int_to_str(temprecord2)           # make sure it is all str data type so we can perform .join on it.
                merged_list.append(" ".join(temp4))       # else append temprecord2 to our blank list.
                del(newlist2[0])                          # delete record from our copied list2.
    return merged_list

def int_to_str(elem):
    '''A function used to convert int data types into str data types
    Parameter elem: the element to check for int data types
    '''
    for i in range(len(elem)):      # loop through the elements until you find one thats an int type and change to str type.
        if type(elem[i]) == int:
            elem[i] = str(elem[i])
    return elem

def write_records(list1):
    '''a function that takes in a list of records and writes to the file output each record on it's own line.
    Parameter list1: the list in which we write from.
    Returns: a file named "sorted_tweets.txt" with text from list1
    '''
    with open('sorted_tweets.txt',"w") as outfile:              # open a file in write mode named "sorted_tweets.txt".
        for lines in list1:                             
            outfile.write(lines+"\n")                   # write every line in the list to "sorted_tweets.txt".
        outfile.close()                                 # close the file.
        
def most_tweets(list1,list2):
    '''A function that takes in two lists and compare the lengths of each. Depending on length
    a certain print function is displayed based on conditions.
    Parameter list1: first list to measure
    Parameter list2: second list to measure
    '''
    if len(list1)==len(list2):      # if they are the smae length then print both names.
        name1 =  "text1.txt"   
        name2 =  "text2.txt"
        length = len(list1)
        print("{} and {} both contained the same number of tweets {}".format(name1,name2,length))
    elif len(list1)>len(list2):     # compare the length of list1 with length of list 2.
        length = len(list1)         # reassign variable length to the length of list1.
        name =  "text1.txt"         # grab the file name associated to that list.
        print("{} contained the most tweets with {}".format(name,length))
    else:   
        length = len(list2)         # reassign variable length to the length of list1.
        name =  "text2.txt"         # grab the file name associated to that list.
        print("{} contained the most tweets with {}".format(name,length))
        
def bottom_five(list1):
    '''A function that indexes the last 5 elements from a list and reference them
    in reverse order. Meaning the last element is presented first.
    Parameter merged_list: a list in which you want to index the last 5 elements
    '''
    s = Scanner("")                 # creates a scanner object.
    for i in range(1,6):            
        s.fromstring(list1[-i])     # index using reverse indexing.
        tweeter = s.readtoken()     # grab the tweeter.
        tweet = s.readstring()      # grab the tweet.
        print(tweeter+" "+tweet)    # print the tweeter and tweet together.


def main():
    '''
    At the command line move to the proper directory and type the following:
    tweet1.txt,tweet2.txt,twitter_sort.py
    '''
    answer = input("are you running this from the command line? enter(y/n)")
    if answer.lower() == 'y':
        print("Reading files...")
        first_list = read_records(sys.argv[1])
        second_list = read_records(sys.argv[2])
        most_tweets(first_list,second_list)
        print("Merging files...")
        merged_list = merge_and_sort_tweets(first_list,second_list)
        print("Writing file...")
        write_records(merged_list)
        print("File written. Displaying 5 earliest tweeters and tweets.")
        bottom_five(merged_list)
    else:
        first_list = read_records('tweet1.txt')
        second_list = read_records('tweet2.txt')
        most_tweets(first_list,second_list)
        print("Merging files...")
        merged_list = merge_and_sort_tweets(first_list,second_list)
        print("Writing file...")
        write_records(merged_list)
        print("File written. Displaying 5 earliest tweeters and tweets.")
        bottom_five(merged_list)        
        
main()