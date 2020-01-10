import random as r
from node import *
import math as mth

class Network:

    def __init__(self, layers):
        self.layers = layers
        self.nodes = []
        self.cost = []

        for i in range(len(self.layers)):
            self.nodes.append([])
            
            for j in range(self.layers[i]):
                if i == 0:
                    n = Node([], [], r.uniform(-1,1))
                    self.nodes[i].append(n)
                else:
                    n = Node(self.nodes[i-1], self.generate_rand_weights(len(self.nodes[i-1])), 0)
                    self.nodes[i].append(n)


    def run(self, does_return):
        # print("network running")

        for i in range(len(self.nodes)):
            if i == 0:
                pass
            else:
                for j in range(len(self.nodes[i])):
                    self.nodes[i][j].calc_output()

        # what was the highest output

        highest_output = [0, 0]
        for n in range(len(self.nodes[-1])):
            if self.nodes[-1][n].output > highest_output[0]:
                highest_output = [self.nodes[-1][n].output, n]

        if does_return:
            # print("done running and calculated output \n")
            return highest_output
        
        # print("done calculating output \n")


    def calc_cost(self, dis_out):
        # print("network calculating cost")
        for layer in self.nodes:
            for node in layer:
                # calc this_out_for node
                if self.nodes.index(layer) == 0:
                    break
                elif self.nodes.index(layer) == len(self.nodes)-1:
                    if layer.index(node) == dis_out:
                        node.dis_outpt = 1
                    else:
                        node.dis_outpt = 0
                else:
                    if type(node.dis_outpt) == list:
                        sum = 0
                        for dis in node.dis_outpt:
                            sum += dis
                        node.dis_outpt = sum/len(node.dis_outpt)
                        if node.dis_outpt > .5:
                            node.dis_outpt = 1
                        else:
                            node.dis_outpt = 0

                for w in node.weights:
                    if node.dis_outpt > .5:
                        if w > .5:
                            if type(node.change[node.weights.index(w)]) == list: 
                                node.change[node.weights.index(w)].append(1)
                                
                                # set dis_out for prev node
                                if type(node.inputs[node.weights.index(w)].dis_outpt) == list:
                                    node.inputs[node.weights.index(w)].dis_outpt.append(1)
                                else:
                                    node.inputs[node.weights.index(w)].dis_outpt = [1]
                            else:
                                node.change.append(1)
                                # set dis_out for prev node
                                if type(node.inputs[node.weights.index(w)].dis_outpt) == list:
                                    node.inputs[node.weights.index(w)].dis_outpt.append(1)
                                else:
                                    node.inputs[node.weights.index(w)].dis_outpt = [1]

                        if w <= .5:
                            if type(node.change[node.weights.index(w)]) == list: 
                                node.change[node.weights.index(w)].append(0)
                                # set dis_out for prev node
                                if type(node.inputs[node.weights.index(w)].dis_outpt) == list:
                                    node.inputs[node.weights.index(w)].dis_outpt.append(0)
                                else:
                                    node.inputs[node.weights.index(w)].dis_outpt = [0]
                            else:
                                node.change.append(0)
                                # set dis_out for prev node
                                if type(node.inputs[node.weights.index(w)].dis_outpt) == list:
                                    node.inputs[node.weights.index(w)].dis_outpt.append(0)
                                else:
                                    node.inputs[node.weights.index(w)].dis_outpt = [0]
                    if node.dis_outpt <= .5:
                        if w > .5:
                            if type(node.change[node.weights.index(w)]) == list: 
                                node.change[node.weights.index(w)].append(0)
                                # set dis_out for prev node
                                if type(node.inputs[node.weights.index(w)].dis_outpt) == list:
                                    node.inputs[node.weights.index(w)].dis_outpt.append(0)
                                else:
                                    node.inputs[node.weights.index(w)].dis_outpt = [0]
                            else:
                                node.change.append(0)
                                # set dis_out for prev node
                                if type(node.inputs[node.weights.index(w)].dis_outpt) == list:
                                    node.inputs[node.weights.index(w)].dis_outpt.append(0)
                                else:
                                    node.inputs[node.weights.index(w)].dis_outpt = [0]
                        if w <= .5:
                            if type(node.change[node.weights.index(w)]) == list: 
                                node.change[node.weights.index(w)].append(1)
                                # set dis_out for prev node
                                if type(node.inputs[node.weights.index(w)].dis_outpt) == list:
                                    node.inputs[node.weights.index(w)].dis_outpt.append(1)
                                else:
                                    node.inputs[node.weights.index(w)].dis_outpt = [1]
                            else:
                                node.change.append(1)
                                # set dis_out for prev node
                                if type(node.inputs[node.weights.index(w)].dis_outpt) == list:
                                    node.inputs[node.weights.index(w)].dis_outpt.append(1)
                                else:
                                    node.inputs[node.weights.index(w)].dis_outpt = [1]

        # for i in range(len(self.nodes)-1, 0, -1):
        #     if i == 0:
        #         pass
        #     else:
        #         for j in range(len(self.nodes[i])):

        #             if (i == len(self.nodes)-1):
        #                     if (j == dis_out):
        #                         self.nodes[i][j].dis_outpt = 1
        #                     else:
        #                         self.nodes[i][j].dis_outpt = 0

        #             for w in range(len(self.nodes[i][j].weights)):
                        
        #                 if (self.nodes[i][j].inputs[w].dis_outpt > .5):
        #                     self.nodes[i][j].inputs[w].dis_outpt = 1
        #                 else:
        #                     self.nodes[i][j].inputs[w].dis_outpt = 0

        #                 dCdW = (2 * (self.nodes[i][j].output - self.nodes[i][j].dis_outpt)) * (self.nodes[i][j].output) * (self.nodes[i][j].inputs[w].output)
                        

        #                 try:
        #                     if type(self.nodes[i][j].change[w]) is list:
        #                         self.nodes[i][j].change[w].append(dCdW)
        #                     else:
        #                         self.nodes[i][j].change.append([dCdW])
        #                 except:
        #                     self.nodes[i][j].change.append([dCdW])
    

        # print("network done calculating cost \n")
    

    def change_net_weights(self):
        # print("network changing weights")

        for i in range(len(self.nodes)):
            if i == 0:
                pass
            else:
                for j in range(len(self.nodes[i])):
                    self.nodes[i][j].avr_change()
                    self.nodes[i][j].change_weights()

        # print("network done changing weights \n")

    
    def set_input(self, input):
        try:
            for i in range(len(self.nodes[0])):
                self.nodes[0][i].output = input[i]
        except:
            print("inputs should be as long as the first layer of nodes")
        


    def generate_rand_weights(self, nummber_of_items):
        rand_list = []
        for i in range(nummber_of_items):
            rand_list.append(r.uniform(-1,1))
        return rand_list

    def randomize_net(self, multiplier):
        for i in range(len(self.nodes)):
            if i == 0:
                pass
            else:
                for j in range(len(self.nodes[i])):
                    for w in self.nodes[i][j].weights:
                        if r.random() < multiplier:
                            w += r.random() * r.randint(-1, 1)
                    self.nodes[i][j].bias += r.randint(-1, 1) * r.random()
