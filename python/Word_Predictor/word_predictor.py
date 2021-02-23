# ########################################################################################
# Programmer: Justin Pickel
# Class: CptS 215 Fall 2019
# Programming Assignment #4
# 10/19/19
#
# Description: This program will read in text files and store every unique word 
# encounterd. The porgram can then make accurate prediction as to what word you 
# want to type based off the prefix entered.

#        Collaboration: Josh Pickel and myself have collaborated on the following topics.
# LinkedList to handle collision
# Node creation and attributes associated.
# Build function and the algorithm used to Map objects to entries
# Parsing algorithm used in the train() method (although we used differnt approches in the end)
# HashTable size
# Unique hashfuntion() using a method provided to us in lecture notes
# ########################################################################################

import random
import string
import timeit

# adapted from Gina Sprint
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
        return self.key
    
    def get_value(self):
        '''
        Returns the Nodes Value attribute.
        '''
        return self.value    

    def get_next(self):
        '''
        Returns the Nodes next pointer.
        '''
        return self.next    

    def set_key(self, newkey):
        '''
        Allows you to set a Nodes key attribute.
        '''
        self.key = newkey
    
    def set_value(self, newvalue):
        '''
        Allows you to set the Nodes Value attribute.
        '''
        self.value = newvalue    

    def set_next(self, newnext):
        '''
        Allows you to redirect the next pointer.
        '''
        self.next = newnext

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
        item.set_next(self.head) # redirect items next pointer to teh head reference.
        self.head = item         # make the head refernce to the new node
        
    def append(self, item):
        '''
        Adds a new item to the end of the list making it the last item in the collection. 
        It needs the item and returns nothing.
        '''
        curr = self.head 
        if curr == None:    # if the LinkedList is e,pty add a Node
            self.add(item)
        else:               # else add a node to he end of the linked list
            while curr.get_next() is not None:
                curr = curr.get_next()
            curr.set_next(item)
            
    def remove(self, item):
            '''
            Removes the item from the list. It needs the item and modifies the list.
            '''
            current = self.head
            previous = None
            found = False
            # loop through the linked list until item is found then remove it
            while not found: 
                if current.get_key() == item: 
                    found = True
                else:
                    previous = current
                    current = current.get_next()
            #if item is the first in the list then reassign the head 
            if previous == None:
                self.head = current.get_next
            # else it is not in the front so remove and redirect pointers.
            else:
                previous.set_next(current.get_next())    

# adpated form gina Sprint        
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
        key = item.get_key() # store the key value of the item
        hashvalue = self.hashfunction(key) # unique hash code
        slot_placed = -1
        
        # if the HashTables slot is empty make it a linkedlist.
        if self.slots[hashvalue] == None:   
            self.slots[hashvalue] = LinkedList()
            self.slots[hashvalue].append(item) # append item to linkedlist.
            slot_placed = hashvalue
            return slot_placed # return index value of slot item was palced.
        
        # if the slot is a linkedlist append the item.
        elif self.slots[hashvalue] != None:   
            self.slots[hashvalue].append(item) # append the item.
            slot_placed = hashvalue  
            return slot_placed # return index value of slot item was palced.
        
        else:
            return slot_placed
        
    def get(self, key):
        '''
        returns slot position if item in hashtable, -1 otherwise
        '''
        startslot = self.hashfunction(key) # unique hast code
        stop = False
        found = False
        position = startslot
        # if HashTable slot is empty return -1 
        if self.slots[position] == None:
            return -1
        # else loop through the linked list in the current HashTable slot until found == True
        else:
            node = self.slots[position].head
            while node != None and not found and not stop:            
                if node.get_key() == key:
                    found = True
                else:
                    node = node.get_next()
                    if node == None:
                        stop = True
            # if you found the Node containing the key retrun the Node
            if found:
                return node
            # else return -1 if not found
            else:
                return -1
            
    def remove(self, item):
        '''
        Removes item.
        Returns slot position if item in hashtable, -1 otherwise
        '''
        startslot = self.hashfunction(item) # unique hash code
        position = startslot
        # if HashTable slot is empty return -1 nothing to remove
        if self.slots[position] == None:
            return -1
        # else grab the linked list stored at the slot and call the remove method with the Node needing to be removed
        else:
            LL = self.slots[position]
            LL.remove(item)
            return 1
        
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
        super().__init__(size)
        
    def __str__(self):
        '''
        String representation
        '''
        count = 0
        s = ""
        for slot in self.slots:
            if slot != None:
                node = slot.head
                if node == None:
                    s += "["+str(count)+"]"+"  Empty\n"
                else:
                    s += "["+str(self.hashfunction(node.get_key()))+"]"+ "--"
                    s += str(slot)+"\n"
                count += 1
        return s
    
    def __len__(self):
        '''
        Return the number of key-value pairs stored in the map.
        '''
        count = 0
        # loop through each slot and then each linkedlist within each slot and count the number of Nodes
        for i in range(self.size):
            item = self.slots[i].head
            while item != None:
                count += 1
                item = item.get_next()
        # return ttoal number of Nodes in the HashTable.
        return count
    
    def __getitem__(self, key):
        '''
        Retrieves the node stored at a specific location.
        Parameters:
        key: Value passed in order to find its location using the hashfunction
        returns the node associated with that Key, -1 otherwise.
        '''
        return self.get(key)

    def __setitem__(self, key, data):
        '''
        Sets the item at a specified location.
        Parameters:
        key: value to be stored as the nodes key reference
        data: value to be stored as the nodes value reference
        '''
        self.put(key,data)
        
    def __delitem__(self, key):
        '''
        Removes item from the Map at a specified location
        Parameters:
        key: value passed in order to find its location using the hashfunction
        '''
        self.remove(key)
        
    def __contains__(self, key):
        '''
        boolean return if an item exist in the Map.
        Parameters:
        key: value passed in order to find its location using the hashfunction
        if the value is -1 then the item does not exist.
        '''
        return self.get(key) != -1

            
    def put(self, key, value=1):
        '''
        Add a new key-value pair to the map. If the key is already in the map then replace the old value with the new value.
        '''
        node = Node(key,value) # create a new Node object.
        temp = super().get(key) # temp variable stores the Node related to the current key.
        if temp != -1: # if temp is in the HashTable
            if type(temp.value) == int:
                temp.set_value(temp.value+value) # change the current value for the temp Node to the current value plus 1
        else:
            slot = super().put(node) # else just add the node since it doesnt exist yet.
        return
    
    def get(self, key):
        '''
        A method that allows you to get a node with the specified key stored as that nodes key reference, -1 otherwise.
        '''
        node = super().get(key) # Node that matches the current key
        if type(node) == Node: # if the temp node is of Node type then return the Node
            return node
        return -1 # else return -1 becuase it does not exist
    
    def remove(self, key):
        '''
        Removes key:value pair.
        '''
        super().remove(key) # call on HahTables remove method passing it a key
        return    
    
    def hashfunction(self, item):
        '''
        "Salted" method
        '''
        return item.__hash__() % self.size# generate unique hash code

# adapted from Gina Sprint    
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
        pass
    
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
        L = [] # empty array to store every letter
        array = [] # empty array to store the words once cleaned
        set_ascii = set([i for i in range(96,123)]) # a set containing all the ascii values for a-z
        set_ascii.add(39) # adding the single apostrophe to the ascii set
        other_char = (set([i for i in range(0,128)])-set_ascii) # all other char ascii values that we dont want
        try:
            with open(training_file,"r") as f: # open the training file to start reading in the file
                for line in f.readlines():
                    L.extend(line.lower()) # convert all letters to lowercase
                start = 0 # start count
                end = 0 # end count
                for i in range(len(L)): # loop through all letters from the file
                    if ord(L[i]) in other_char: # if the character is in the ascii set then conver tto a space
                        L[i] = " "
                    end+=1 # increment the end slice by 1
                    if L[i] is " ": # if the character is a space
                        temp = L[start:end] # collect all the letters from start to end
                        temp = "".join(temp) # join all the letters collected to form a word
                        temp = temp.strip() # strip any remaing white space
                        if temp != "": # if we are looking at a word then put it in the map
                            self.word_to_count.put(temp)
                            self.total += 1
                        start = end # move up the start index
        except FileNotFoundError: # if the file cannont be reaad then throw an exception
            print( "Could not open training file: %s" %(training_file))
        
    def train_word(self,word):
        '''
        A method that allows you to add a single word to our trained model
        '''
        word = word.lower() # convert word to lowercase
        self.total += 1 # increase the total number of words encountered
        return self.word_to_count.put(word) # put the word into the Map object
        
    def get_training_count(self):
        '''
        A method used t retrieve the total number of words encountered
        '''
        return self.total
    
    def get_word_count(self,word):
        '''
        A method used to look up the count value for a specific word
        '''
        try: 
            value = self.word_to_count.get(word).value # if the word exist return its count
            return value
        
        except AttributeError: # if the word doesnt exist return 0
            return 0
    
    def build(self):
        '''
        A method used to assign a prefix to a word that has the highest probability associated with the word.
        '''
        for i in range(self.word_to_count.size): # for evey slot in the hash table loop over them
            if self.word_to_count.slots[i] != None: # as long as a linked list is stored in teh slot then loop through the linked list.
                node = self.word_to_count.slots[i].head
                # as long as a linked list is stored in teh slot then loop through the linked list.
                while node != None:
                    word = node.key # store the word associated with thw current Node
                    count = node.value # store the value associated with the current Node
                    prob = (count)/(self.total) # calculate the probability
                    temp = DictEntry(word,prob) # create a new DictEntry object witht he current word and the calculated probability
                    start = 0 # start index starts at 0
                    end = 1 # end index starts at 1
                    for e in range(len(word)): # for generate every possible prefix from the current word and assign a DictEntry object to it.
                        prefix = word[start:end]
                        if self.prefix_to_entry.__contains__(prefix): # if the current prefix is stored int he Map object then comapre porobabilities
                            current = self.prefix_to_entry.get(prefix).value.get_prob()
                            if temp.get_prob() > current: # if the current word stored witht he prefix is less than the word we are on switch them
                                self.prefix_to_entry.get(prefix).value = temp
                        else:
                            self.prefix_to_entry.put(prefix,temp) # else if it does not exist yet create a new entry to the Map object
                        end+=1
                    node = node.get_next()
                
    def get_best(self,prefix):
        '''
        A method used to return the most probable word associated witht eh given prefix.
        Paramaeter:
        prefix: the prefix that will be used to look up a word associated with it.
        '''
        if self.prefix_to_entry.get(prefix) != -1: # if the prefix exist in our Map object then return the word associated with it.
            return self.prefix_to_entry.get(prefix).value
            

def random_load_test(wp):

    '''



    '''

    print("\nrandom load test: ")

    VALID = string.ascii_lowercase

    TEST_NUM = 10000

    hits = 0

    for i in range(TEST_NUM):

        prefix = ""

        for j in range(0, random.randint(1, 6), 1):

            prefix += VALID[random.randrange(0, len(VALID))]

        de = wp.get_best(prefix)

        if (de != None) and (de.get_word() != "null"):

            hits += 1



    print("Hit = %.2f%%" %(hits / TEST_NUM * 100))


# adapted form Sirini Badri
def main():

    '''
    A function used for testing purposes
    '''

    # train a model on the first bit of Moby Dick

    wp = WordPredictor()

    print("bad1 = %s" %wp.get_best("the"))

    wp.train("moby_start.txt")

    print("training words = %d" %(wp.get_training_count()))



    # try and crash things on bad input

    print("bad2 = %s" %wp.get_best("the"))

    wp.train("thisfiledoesnotexist.txt")

    print("training words = %d\n" %(wp.get_training_count()))



    words = ["the", "me", "zebra", "ishmael", "savage"]

    for word in words:

        print("count, %s = %d" %(word, wp.get_word_count(word)))

    wp.train("moby_end.txt")

    print()

    # check the counts again after training on the end of the book

    for word in words:

        print("count, %s = %d" %(word, wp.get_word_count(word)))

    print()



    # Get the object ready to start looking things up

    wp.build()



    # do some prefix loopups

    test = ["a", "ab", "b", "be", "t", "th","w", "archang"]

    for prefix in test:

        if (wp.get_best(prefix)):

            print("%s -> %s\t\t\t%.6f" %(prefix, wp.get_best(prefix).get_word(), wp.get_best(prefix).get_prob()))

        else:

            print("%s -> %s\t\t\t%s" %(prefix, "None", "None"))

    print("training words = %d\n" %(wp.get_training_count()))



    # add two individual words to the training data

    wp.train_word("beefeater")

    wp.train_word("BEEFEATER!")

    wp.train_word("Pneumonoultramicroscopicsilicovolcanoconiosis")



    # The change should have no effect for prefix lookup until we build()

    test_2 = ['b', 'pn']

    for prefix in test_2:

        if (wp.get_best(prefix)):

            print("before, %s -> %s\t\t%.6f" %(prefix, wp.get_best(prefix).get_word(),  wp.get_best(prefix).get_prob()))

        else:

            print("before, %s -> %s\t\t%s" %(prefix, "None",  "None"))

    wp.build()

    for prefix in test_2:

        if (wp.get_best(prefix)):

            print("after, %s -> %s\t\t%.6f" %(prefix, wp.get_best(prefix).get_word(), wp.get_best(prefix).get_prob()))

        else:

            print("after, %s -> %s\t\t%s" %(prefix, "None", "None"))

    print("training words = %d\n" %(wp.get_training_count()))



    # test out training on a big file, timing the training as well

    start = timeit.default_timer()

    wp.train("mobydick.txt")

    wp.build()

    for prefix in test:

        if (wp.get_best(prefix)):

            print("%s -> %s\t\t\t%.6f" %(prefix, wp.get_best(prefix).get_word(), wp.get_best(prefix).get_prob()))

        else:

            print("%s -> %s\t\t\t%s" %(prefix, "None", "None"))

    print("training words = %d\n" %(wp.get_training_count()))

    stop = timeit.default_timer()

    elapsed = (stop - start)

    print("elapsed (s): %.6f" %(elapsed))



    # test lookup using random prefixes between 1-6 characters

    start = timeit.default_timer()

    random_load_test(wp)

    stop = timeit.default_timer()

    elapsed = (stop - start)

    print("elapsed (s): %.6f" %(elapsed))



main()