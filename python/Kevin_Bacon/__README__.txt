Libraries need for this program include:

from collections import deque
# (pip install matplotlib)
import matplotlib.pyplot as plt
# (pip install networkx)
import networkx as nx

Decription: This program will promt the user to enter the name of an actor (refer to actors.txt for names)
	    Once an actor name is provided the program will calculate how many degrees the actor is from kevin bacon using network theory and breadth first search.
	    The program will also show you the corresponding network graphic.

Classes used in the program:

class Vertex:
    '''
    keep track of the vertices to which it is connected, and the weight of each edge
    '''
    def __init__(self, key):
        '''
        constructor for the vertex class
        '''
        self.ID = key
        self.connected_to = []

    def __str__(self):
        '''
        returns all of the vertices in the adjacency list, as represented by the connectedTo instance variable
        '''
        return str(self.ID)
    
    def add_neighbor(self, neighbor, title):
        '''
        add a connection from this vertex to another
        '''
        self.connected_to.append(Edge(title,self,neighbor))  #[neighbor] = Edge(title,self,neighbor) 
    
    def get_connections(self):
        '''
        returns all connecting attributed to the current vertex
        '''
        return self.connected_to  #.keys()    
    
class Edge:
    '''
    Edge object used to store a paretn vertex(from) and a child vertex(to)
    '''
    
    def __init__(self, title, parent = None, child = None):
        '''
        constructor for the edge class.
        Parameters:
        title: the name of the movie connected two actors(vertecies)
        parent: the 'from' vertex
        child: the 'to' vertex
        '''
        self.title = title
        self.parent = parent
        self.child = child
        
    def get_title(self):
        '''
        function that return the edges title
        '''
        return self.title
    
    def get_parent(self):
        '''
        function that returns the edges parent vertex
        '''
        return self.parent
    
    def get_child(self):
        '''
        function that returns the edges child vertex
        '''
        return self.child
    
    
class Graph:
    '''
    contains a dictionary that maps vertex names to vertex objects. 
    '''
    def __init__(self):
        '''
        constructor for the Graph object
        '''
        self.vert_list = {}
        self.num_vertices = 0
        
    def __str__(self):
        '''
        string representation of the graph object
        '''
        edges = ""
        for vert in self.vert_list.values():
            for vert2 in vert.get_connections():
                edges += "(%s, %s)\n" %(vert.get_ID(), vert2.get_ID())
        return edges

    def __contains__(self, n):
        '''
        overrides the in operator
        '''
        return n in self.vert_list
    
    def add_vertex(self, key):
        '''
        adding vertices to a graph 
        '''
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(key)
        self.vert_list[key] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        '''
        return the vertex in need
        '''
        if n in self.vert_list:
            return self.vert_list[n]
        else:
            return None    

    def add_edge(self, f, t, title):
        '''
        connecting one vertex to another
        '''
        if f not in self.vert_list:
            nv = self.add_vertex(f)
        if t not in self.vert_list:
            nv = self.add_vertex(t)
        self.vert_list[f].add_neighbor(self.vert_list[t], title)

    def get_vertices(self):
        '''
        returns the names of all of the vertices in the graph
        '''
        return self.vert_list.keys()

    def __iter__(self):
        '''
        for functionality
        '''
        return iter(self.vert_list.values())

Functions used in the program:

def make_dicts(filename):
    '''
    function that creates a key value pair object (Dictionary) from a given text file.
    Parameters:
    filename: A string contain either an absolute or relative file path.
    '''

def merged_dict(dict1,dict2,dict3):
    '''
    function that merges all dictionaries together.
    '''

def build_graph(main_dict):
    '''
    function that generates the main graph that will be used for searching for
    the shortest path.
    Paramaeters:
    main_dict: A dictionary that contains keys(movies) and values(list of [actor1,actor2...])
    '''

def bfs(g,start):
    '''
    Algorithim used to traverse a graph only adding one way edges from the vertex
    connecting to the root.
    Parameters:
    g: graph to traverse
    start: the root of the new_graph
    enqueue: append left
    dequeue: pop right
    '''

def tree_search(tree,target):
    '''
    function that searches the graph for a target. If the target is present then
    follow the path from teh target to the root.
    Parameters:
    tree: one way directed graph containing all the connections from the root back to the root
    target: the starting point of the path. All paths start from a given point(target) and work towards the root
    '''

def find_stats(actor_dict,graph):
    '''
    similar function to tree_search excluding all the print statements.
    This function is used to determine the bacon number of each actor. This value
    is stored in a dictionary "stats_dict".
    Parameters:
    actor_dict: A dictionary with key(actor number) and values(actor names)
    graph: A graph object with a root that is the destination actor. 
           ex. if we want the bacon number this graph will need to have 
           Kevin Bacon as the root.
    '''

def stats(actor_stats):
    '''
    function thats calcualates statistics about the graph created. Supported Statistics include
    the average bacon number of all actors excluding 0(not finite), and the actor with the largest finite bacon number
    Parameters:
    actor_stats: A dictionary with keys(actor name) and values(bacon number)
    '''

def reference_dict(actors):
    '''
    function used to help with accepting input values from the user. This dictionary
    makes a key that is the actors name in lowercase. The vlaue is the actors name as
    displayed in the original file.
    Parameters:
    actors: A dictionary with keys(actor number) and values(actor name)
    '''