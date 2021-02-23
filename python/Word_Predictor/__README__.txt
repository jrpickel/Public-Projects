Libraries used:

import random
import string
import timeit


Description: This program will read in text files and store every unique word 
             encounterd. The porgram can then make accurate prediction as to what word you 
             want to type based off the prefix entered.

Collaboration: Josh Pickel and myself have collaborated on the following topics.
             LinkedList to handle collision
 	     Node creation and attributes associated.
 	     Build function and the algorithm used to Map objects to entries
 	     Parsing algorithm used in the train() method (although we used differnt approches in the end)
 	     HashTable size
 	     Unique hashfuntion() using a method provided to us in lecture notes


Classes and methods Used:

class Node:
    '''
    Node class creates nodes for a singlely linked list data structure.
    Methods include:
    get_key()
    get_value()
    get_next()
    set_key()
    set_value()
    set_next()
    '''
    def __init__(self, key, value):
        '''
        Node constructor
        Paramaeters:
        key: value to be stored as the Nodes attribute.
        value: value to be stored as the Nodes value attribute.
        '''
        self.key = key
        self.value = value
        self.next = None
        
    def __str__(self):
        '''
        '''
        return "{"+str(self.key)+":"+str(self.value)+"}"

    def get_key(self):
        '''
        Return the Nodes Key attribute.
        '''
    
    def get_value(self):
        '''
        Returns the Nodes Value attribute.
        ''' 

    def get_next(self):
        '''
        Returns the Nodes next pointer.
        '''  

    def set_key(self, newkey):
        '''
        Allows you to set a Nodes key attribute.
        '''
    
    def set_value(self, newvalue):
        '''
        Allows you to set the Nodes Value attribute.
        '''  

    def set_next(self, newnext):
        '''
        Allows you to redirect the next pointer.
        '''

# adapted from Gina Sprint
class LinkedList:
    '''
    Creates a Single Linked List data structure with the following methods:
    add()
    append()
    remove()
    '''
    def __init__(self):
        '''
        Creates a new list that is empty. It needs no parameters and returns an empty list.
        '''
        self.head = None
        
    def __str__(self):
        '''
        
        '''
        list_str = ""
        curr = self.head
        while curr is not None:
            list_str += str(curr)
            list_str += "->"
            curr = curr.get_next()
        list_str += "None"
        return list_str
        
    def add(self, item):
        '''
        Adds a new item to the list. It needs the item and returns nothing.
        Parameters:
        item: item is a node being passed to the linked list.
        '''
        
    def append(self, item):
        '''
        Adds a new item to the end of the list making it the last item in the collection. 
        It needs the item and returns nothing.
        '''
            
    def remove(self, item):
            '''
            Removes the item from the list. It needs the item and modifies the list.
            ''' 
      
class HashTable:
    '''
    Creates a HashTable data structure. Collisions are handled through implementing a linked list.
    The following methods can be performed on the HashTable Data structure:
    put()
    get()
    remove()
    '''
    def __init__(self, size=571):
        '''
        Constructor for our HashTable. The HashTable as the following attributes:
        Parameters: size default size is 571 if another size is not passsed.
        Attributes:
        self.size: the size of the HashTable
        self.slots: The actual slots used for indexing.
        '''
        self.size = size
        self.slots = [None] * self.size # create a hashtable with this many slots
        
    def put(self, item):
        '''
        Place an item in the hash table.
        Return slot number if successful, -1 otherwise (no available slots, table is full)
        '''
        
    def get(self, key):
        '''
        returns slot position if item in hashtable, -1 otherwise
        '''
         
    def remove(self, item):
        '''
        Removes item.
        Returns slot position if item in hashtable, -1 otherwise
        '''
        
# adapted from Gina Sprint      
class Map(HashTable):
    '''
    This Class creates an ADS called Map. A Map is an advanced dictionary. The following methods can be used:
    __len__(): returns the len of the map
    __getitem__(): retrieves the node stored at a specific location.
    __setitem__(): sets the item at a specified location.
    __delitem__(): Removes item from teh Map
    __contains__(): boolean return if an item exist in the Map.
    put(): Adds and item to the Map
    get(): Retrieves an item from the Map
    remove(): Removes item from the Map
    hashfunction(): function used to generate a unique values. This value is used to determine a specific index.
    '''
    def __init__(self, size=571):
        '''
        Constructor for a Map object implements the HashTable constructor.
        Paramaters:
        size: default size is 571 if a value is not passed.
        '''
        
    def __str__(self):
        '''
        String representation
        '''
    
    def __len__(self):
        '''
        Return the number of key-value pairs stored in the map.
        '''
    
    def __getitem__(self, key):
        '''
        Retrieves the node stored at a specific location.
        Parameters:
        key: Value passed in order to find its location using the hashfunction
        returns the node associated with that Key, -1 otherwise.
        '''

    def __setitem__(self, key, data):
        '''
        Sets the item at a specified location.
        Parameters:
        key: value to be stored as the nodes key reference
        data: value to be stored as the nodes value reference
        '''
        
    def __delitem__(self, key):
        '''
        Removes item from the Map at a specified location
        Parameters:
        key: value passed in order to find its location using the hashfunction
        '''
        
    def __contains__(self, key):
        '''
        boolean return if an item exist in the Map.
        Parameters:
        key: value passed in order to find its location using the hashfunction
        if the value is -1 then the item does not exist.
        '''
   
    def put(self, key, value=1):
        '''
        Add a new key-value pair to the map. If the key is already in the map then replace the old value with the new value.
        '''
    
    def get(self, key):
        '''
        A method that allows you to get a node with the specified key stored as that nodes key reference, -1 otherwise.
        '''
    
    def remove(self, key):
        '''
        Removes key:value pair.
        '''  
    
    def hashfunction(self, item):
        '''
        "Salted" method
        '''
  
class DictEntry:
    
    # create a new entry given a word and probability
    def __init__(self,word, prob): # string, float 
        self.word = word
        self.prob = prob
    
    def __str__(self):
        '''
        
        '''
        s = "{"
        s += str(self.get_word())
        s += ":"
        s += str(self.get_prob())
        s += "}"
        return s    
        
    # getter for the word 
    def get_word(self): # returns string
        return self.word
    
    # getter for the probability
    def get_prob(self): # returns float
        return self.prob
    
    # does this word match the given pattern?
    def match_pattern(self,pattern): # returns string
    
# adapted from Gina Sprint
class WordPredictor:
    
    def __init__(self):
        self.word_to_count = Map()
        self.prefix_to_entry = Map()
        self.total = 0
        
    def train(self,training_file):
        '''
        A method that allows you to pass in a file and add the words from that file into your Map object.
        This method also parses all the words in the file and converts all letters to lowercase.
        Parameters:
        training_file: A file name used to do the training on.
        '''
        
    def train_word(self,word):
        '''
        A method that allows you to add a single word to our trained model
        '''
        
    def get_training_count(self):
        '''
        A method used t retrieve the total number of words encountered
        '''
    
    def get_word_count(self,word):
        '''
        A method used to look up the count value for a specific word
        '''
    
    def build(self):
        '''
        A method used to assign a prefix to a word that has the highest probability associated with the word.
        '''
                
    def get_best(self,prefix):
        '''
        A method used to return the most probable word associated witht eh given prefix.
        Paramaeter:
        prefix: the prefix that will be used to look up a word associated with it.
        '''
            
