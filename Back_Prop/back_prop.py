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