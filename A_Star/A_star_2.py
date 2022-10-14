from math import inf, sqrt
from heapq import heappop, heappush
import string
from math import log,ceil

alphabet = string.ascii_uppercase
a_c = len(alphabet)

print(alphabet,a_c)

class graph_vertex:
  def __init__(self, name, x, y):
    self.name = name
    self.position = (x, y)


def heuristic(start,target): # Calculate straight distance using Pythagorean theorem
    x_distance = abs(start.position[0] - target.position[0]) 
    y_distance = abs(start.position[1] - target.position[1])
    return sqrt((x_distance**2)+(y_distance)**2)

def get_letters(number):
    letters = ''
    if number == 1:
        letters += alphabet[0]
    else:
        number_of_letters = ceil(log(number,a_c))
        for i in range(1,number_of_letters+1):
            index_of_letter = number // (a_c**(number_of_letters - i))
            if (number_of_letters - i) >= 1 and (number%(a_c**(number_of_letters - i)))==0:
                letters += alphabet[index_of_letter-2]
            else:
                letters += alphabet[index_of_letter-1]
            num = number % (a_c**(number_of_letters - i))
            number = num
    return(letters)


def graph_generator(a):
    graph = {}
    x_a = 0
    y_a = 0
    for i in range(1,(a**2)+1):
        if y_a > (a-1):
            x_a += 1
            y_a = 0
        vertex_letter = get_letters(i)
        vertex = graph_vertex(vertex_letter,x_a,y_a)
        graph[vertex] = set()
        y_a += 1
    for i in graph:
        position = i.position
        x_b = i.position[0]
        y_b = i.position[1]
        for j in graph:
            x_c = j.position[0]
            y_c = j.position[1]
            if j == i:
                pass
            elif (abs(x_c - x_b) < 2) and (abs(y_c - y_b) < 2):
                path_len = heuristic(j,i)
                tup = (j,path_len)
                graph[i].add(tup)
    return graph


graph_x = graph_generator(3)
# for i in graph_x:
#     string_g = str(i.name) + str(i.position) + ' Neighbors :'
#     for j in graph_x[i]:
#         string_h = str(j[0].name)+'-'+str(j[1])+ ' '
#         string_g += string_h
#     print(string_g)
destinations = [a for a in graph_x] # List of all vertices
destinations_letters = [a.name for a in destinations] # List of all 1st letters in destination
i = 0 # pointer for dict creation
destinations_letters_dictionaty = {} # Dict linking destination with it's 1st letter for easy user input
for letter in destinations_letters:
    destinations_letters_dictionaty[letter] = destinations[i]
    i += 1

def a_star(graph, start, target): # A*
  count = 0
  print("Starting A* algorithm!")
  paths_and_distances = {}
  # paths_and_distances[vertex][0] is heuristic path calculated from coordinates
  # paths_and_distances[vertex][1] is path len
  # paths_and_distances[vertex][2] represents steps you need to take to get from start to target
  for vertex in graph: # preset paths_and_distances[0] = inf [1] = inf [3] = [start.name] path always begins with start
    paths_and_distances[vertex] = [inf,inf, [start.name]]
  
  paths_and_distances[start][1] = 0 # path length at start is 0
  paths_and_distances[start][0] = 0 # heuristic path length at start is 0
  vertices_to_explore = [(0, start)] #1st vertex to explore
  while vertices_to_explore and paths_and_distances[target][0] == inf: # when target is not inf we found our target
    current_distance, current_vertex = heappop(vertices_to_explore) # pop from heap vertices_to_explore
    for neighbor, edge_weight in graph[current_vertex]: # setting all distances for neighbor
      new_hdistance = current_distance + edge_weight + heuristic(neighbor, target)
      new_path = paths_and_distances[current_vertex][2] + [neighbor.name]
      new_distance = current_distance + edge_weight
    #   print("Checking {}\n".format(neighbor.name))
      if new_distance < paths_and_distances[neighbor][0]:
        paths_and_distances[neighbor][0] = new_hdistance
        paths_and_distances[neighbor][1] = new_distance
        paths_and_distances[neighbor][2] = new_path
        heappush(vertices_to_explore, (new_hdistance, neighbor)) # push all neighbors to vertices_to_explore heap if they are not inf
        # print("\nmatch At " + vertices_to_explore[0][1].name)
        #testing
  print("Found a path in {0} steps. Path length: {2} Path: {1}".format(count,paths_and_distances[target][2],paths_and_distances[target][1]))
  
  return paths_and_distances[target][1]


def get_start(): # user input for start
  start_point_letter = ""
  while start_point_letter not in destinations_letters:
      start_point_letter = input("Where are you coming from? Type in the corresponding letter: ")
      if start_point_letter in destinations_letters:
        start_point = destinations_letters_dictionaty[start_point_letter]
        return start_point   
      else:
        print("Error try again\n")
  

def get_end(): # user input for end
    end_point_letter = ""
    while end_point_letter not in destinations_letters:
      end_point_letter = input("Ok, where are you headed? Type in the corresponding letter: ")
      if end_point_letter in destinations_letters:
        end_point = destinations_letters_dictionaty[end_point_letter]
        return end_point   
      else:
        print("Error tyr again\n")

def show_destination(): # show map of destination and letter linking them for user input
    for k,v in destinations_letters_dictionaty.items():
        print("{} - {}".format(k,v.name))

def greet(): # all in one
    print("Hello")
    show_destination()
    a = get_start()
    b = get_end()
    a_star(graph_x,a,b)
greet()