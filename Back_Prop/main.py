from network import *
print("\n")


net = Network([3, 1])

net.nodes[1][0].weights = [1, 5, 2]
net.nodes[1][0].bias = 2

array = [1, -1, 2]

# loop (img / batch size)
# bacht loop (batch size)
net.set_input(array)
net_out = net.run(True)
print(net_out)


net.calc_cost(0)
#\batch loop
net.change_net_weights()
#\loop

n1 = Node([], [], 1)
n2 = Node([], [], -1)
n3 = Node([], [], 3)
n4 = Node([n1, n2 ,n3], [1,5,2], 0)
n4.bias = 2
n4.calc_output()
print(n4.output)
## program to show how nodes work

# import random as r

# def generate_rand_weights(nummber_of_items):
#     rand_list = []
#     for i in range(nummber_of_items):
#         rand_list.append(r.random())
#     return rand_list


# from node import *

# nummber_of_inp_nodes = 20

# inp_nodes = []

# for i in range(nummber_of_inp_nodes):
#     n = Node([], [], r.uniform(-10, 10))
#     inp_nodes.append(n)

# n1 = Node(inp_nodes, generate_rand_weights(nummber_of_inp_nodes), 0)
# n2 = Node(inp_nodes, generate_rand_weights(nummber_of_inp_nodes), 0)

# n1.calc_output()
# n2.calc_output()

# n3 = Node([n1, n2], [1,-1], 0)

# n3.calc_output()