from collections import deque
import matplotlib.pyplot as plt
import networkx as nx

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
    
    
def make_dicts(filename):
    '''
    function that creates a key value pair object (Dictionary) from a given text file
    '''
    my_dict = {}
    in_file = open(filename, "r", encoding="utf-8")
    # loop through file and split the line between the "|" char
    for line in in_file.readlines():
        line = line.strip()
        line = line.split("|")
        # if the first value exist in the dictionary then append the new edge
        if line[0] in my_dict:
            my_dict[line[0]].append(line[1])
        # else add the first value to the dictionary and store the value
        else:
            my_dict[line[0]] = [line[1]]
    # close the file
    in_file.close() 
    return my_dict
 
def merged_dict(dict1,dict2,dict3):
    '''
    function that merges all dictionaries together.
    '''
    my_dict = {} # create a new dictionary to store all appropriate values
    keys = list(dict3.keys()) # make a list of all the keys in my dictionary
    # loop through ever key in the dictionary and replace numerical values with names
    for i in keys:
        temp_key = dict2[i][0]
        my_dict[temp_key] = [] # store an empty list as the value of a certain key
        temp_list = dict3[i]
        # loop through all keys in dict2 and replace numerical values with names
        for i in temp_list:
            temp_val = dict1[i][0]
            my_dict[temp_key].append(temp_val)
    return my_dict

def build_graph(main_dict):
    '''
    function that generates the main graph that will be used for searching for
    the shortest path.
    Paramaeters:
    main_dict: A dictionary that contains keys(movies) and values(list of [actor1,actor2...])
    '''
    g = Graph() # create a new graph object
    keys = list(main_dict.keys()) # create a list of keys to iterate over
    # for each key(movie) in the main_dictionary step into the list of values(actors)
    # and for every actor in the list create an edge for evey actor combination
    for i in keys:
        lst = main_dict[i]
        for e in range(len(lst)):
            for k in range(e+1,len(lst)):
                g.add_edge(lst[e],lst[k],i)
                g.add_edge(lst[k],lst[e],i)
    return g # return the graph object

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
    frontier_queue = deque()
    frontier_queue.appendleft(start)
    discovered_set = set([start]) # set containing all visited vertecies
    new_g = Graph() # make a new graph that will store one way edges from a vertex to its parent
    new_g.add_vertex(start.ID) # add the starting vertex(root) to the new_graph obj
    # loop through all connections and add them to the queue to be processed once the queue
    # is empty stop looping.
    while len(frontier_queue) > 0:
        curr_v = frontier_queue.pop() # pop the first item in the queue(the root)
        for adj_v in curr_v.get_connections(): # look at evey vertex that is connected to the root
            if adj_v.child not in discovered_set: # if it has not been processed add it to the discovered queue
                new_g.add_edge(adj_v.child.ID,curr_v.ID,adj_v.title) # create an edge from the child to the parent
                frontier_queue.appendleft(adj_v.child) # add the newly discovered vertex to the queue to be processed
                discovered_set.add(adj_v.child) # add the vertex to the discovered list
    return new_g


def tree_search(tree,target):
    '''
    function that searches the graph for a target. If the target is present then
    follow the path from teh target to the root.
    Parameters:
    tree: one way directed graph containing all the connections from the root back to the root
    target: the starting point of the path. All paths start from a given point(target) and work towards the root
    '''
    count = 0
    elabel = {} # dictionary object used for creating graph labels
    # if target is in the tree then start at the target
    # otherwise print("Actor has no path")
    if target in tree.vert_list:
        start = tree.vert_list[target]
        edge = start.connected_to
        # until we reacha vertex that has no edges(root) keep moving to a new vertex
        while len(edge) > 0:
            # infromation stored in the edge object
            info = edge[0]
            # add a key(tuple) and value(movie title) to the edge label dictionary ex. {(actor1,actor2):"movie1"}
            elabel[(info.parent.ID,info.child.ID)] = info.title 
            print(str(info.parent.ID) + " appeared in " + info.title +" "+ str(info.child.ID)) # print the information to the user
            vertex = edge[0].child # move up the vertex object
            edge = vertex.connected_to # reassign edge for the while loop conditional check
            count += 1
    else:
        print("Actor has no path\n")
    # networkx visualization instructions
    edges = list(elabel.keys()) # list of all edge objects
    G = nx.DiGraph() # create a new networkx digrapgh
    G.add_edges_from(edges) # add edges to teh graph this also creates nodes(vertecies) for the digraph object
    pos = nx.spring_layout(G) # pos argument is set to "spring"
    plt.figure(figsize=(7,7)) # create a matplotlib plot window size 7x7
    nx.draw(G,labels={node:node for node in G.nodes()},width=2,node_size=5000,pos=pos,style="dotted") # draw the digraphs nodes(vertecies)
    nx.draw_networkx_edge_labels(G,pos,edge_labels=elabel) # draw the edge labels
    plt.axis('off') #turn off the plot axis
    print(str(target)+"'s"+" number is " + str(count)+"\n") # print out the bacon number found

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
    stat_dict = {} # dictionary to store stats
    actors = list(actor_dict.values()) # create a list obj with all actors
    # loop through all actors and determine a bacon number for each actor
    for i in actors:
        count = 0
        if i[0] in graph.vert_list:
            start = graph.vert_list[i[0]]
            edge = start.connected_to
            # until we hit the root keep looping
            while len(edge) > 0:
                vertex = edge[0].child
                edge = vertex.connected_to
                count += 1 # increase count by 1 for ever path we take
            stat_dict[i[0]] = count 
    return stat_dict # return the stat dictionary

def stats(actor_stats):
    '''
    function thats calcualates statistics about the graph created. Supported Statistics include
    the average bacon number of all actors excluding 0(not finite), and the actor with the largest finite bacon number
    Parameters:
    actor_stats: A dictionary with keys(actor name) and values(bacon number)
    '''
    stats = list(actor_stats.values()) # list of all the values stored in the actor_stats dict
    names = list(actor_stats.keys()) # list of all the names of the actors in which a bacon number was determined
    summ = sum(stats) # sum of all the values in stat_dict
    num = len(stats) # the number of entries in the stat_dict
    avg = summ/num # average bacon number
    maxx = max(stats) # max bacoon number
    index = stats.index(maxx) # index value associated tot eh max number
    biggest_bacon = names[index] # actor associated witht he max bacon number
    print("Average Bacon Number is: "+ str(avg))
    print("The actor with the largest bacon Number is: " + biggest_bacon)
    
def reference_dict(actors):
    '''
    function used to help with accepting input values from the user. This dictionary
    makes a key that is the actors name in lowercase. The vlaue is the actors name as
    displayed in the original file.
    Parameters:
    actors: A dictionary with keys(actor number) and values(actor name)
    '''
    ref_dict = {} # create a new dictionary
    values = list(actors.values()) # create a iterable list of all the actors names
    # loop through the list and convert every actors name to lowercase and then store that as the key
    # in teh ref_dict variable and the value will be the actos name as appeared in the file.
    for i in values:
        ref_dict[i[0].lower()] = i[0]
    return ref_dict # return s the ref_dict variable

def main():
    actors = make_dicts(r"actors.txt")
    movies = make_dicts(r"movies.txt")
    movie_actor = make_dicts(r"movie-actors.txt")
    main_dict = merged_dict(actors,movies,movie_actor)
    ref_dict = reference_dict(actors)
    graph = build_graph(main_dict)
    
    root = "Kevin Bacon"
    x = bfs(graph,graph.get_vertex(root))
    
    while True:
        print("\nTo quit the program, type return as the answer to the prompt\n")
        search = input("Enter the name of an actor: ")
        search = search.lower()
        if search == "return":
            print("Ending Bacon Game")
            break
        try:
            search_val = ref_dict[search]
            tree_search(x,search_val)
        except KeyError:
            
            print("Actor not found please enter a valid actor")
            
main()