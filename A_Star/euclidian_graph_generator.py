import string
from math import log,ceil,sqrt

alphabet = string.ascii_uppercase
a_c = len(alphabet)

print(alphabet,a_c)

class graph_vertex:
  def __init__(self, name, x, y):
    self.name = name
    self.position = (x, y)


def heuristic_ver(start,target): # Calculate straight distance using Pythagorean theorem
    x_distance = abs(start.position[0] - target.position[0]) 
    y_distance = abs(start.position[1] - target.position[1])
    return sqrt((x_distance**2)+(y_distance**2))

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
                path_len = heuristic_ver(j,i)
                tup = (j,path_len)
                graph[i].add(tup)
    return graph

graph_x = graph_generator(4)
print(type(graph_x))
for i in graph_x:
    string_g = str(i.name) + str(i.position) + ' Neighbors :'
    print(type(i))
    for j in graph_x[i]:
        string_h = str(j[0].name)+'-'+str(j[1])+ ' '
        string_g += string_h
        print(type(j))
    print(string_g)

# # vertex = graph_x['A']
# # posi = vertex.position
# # print(posi)
# # for i in graph_x:
# #     vertex_b = graph_x[i]
#     position = vertex_b.position
#     print(i,' ',position)

# lettir = get_letters(1)
# print(lettir)