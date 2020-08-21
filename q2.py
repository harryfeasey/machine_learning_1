import math
def argmax(items):
    maximum = max(items)
    return items.index(maximum)
def argmin(items):
    minimum = min(items)
    return items.index(minimum)

class DTNode:
    def __init__(self, decision):
        self.decision = decision
        self.children = []

    def predict(self, v):
        if callable(self.decision):
            return self.children[self.decision(v)].predict(v)
        return self.decision

    def leaves(self):
        if len(self.children) == 0:
            return 1
        return sum([c.leaves() for c in self.children])

def partition_by_feature_value(index, data):
    order = list(set([d[0][index] for d in data]))
    separator = lambda f: order.index(f[index])
    partition = [[] for _ in order]
    for val in data:
        partition[separator(val[0])].append(val)
    return (separator, partition)

def proportion(classification, data):
    total = 0
    for _, c in data:
        if c == classification:
            total += 1
    return total / len(data)

def classes(data):
    return list(set([d[1] for d in data]))

def gini(data):
    H = 0
    for k in classes(data):
        prop = proportion(k, data)
        H += prop*(1 - prop)
    return H

def entropy(data):
    H = 0
    for k in classes(data):
        prop = proportion(k, data)
        if prop != 0:
            H += prop*math.log(prop)
    return -H

def misclassification(data):
    return 1 - max([proportion(k, data) for k in classes(data)])

def objective(criterion, k, data):
    separator, partition = partition_by_feature_value(k, data)
    if len(partition) == 1:
        return float('-inf')
    return sum([(len(p)/len(data)) * criterion(p) for p in partition])

def train_tree(data, criterion):
    classes = list(set([d[1] for d in data]))
    if len(classes) == 1:   # All classified the same
        return DTNode(data[0][1])
    if len(data[0]) == 0:   # Empty feature set
        return DTNode(classes[argmax([proportion(k, data) for k in classes])])

    split = argmax([objective(criterion, k, data) for k in range(len(data[0][0]))])
    separator, partition = partition_by_feature_value(split, data)

    node = DTNode(separator)
    node.children = [train_tree(p, criterion) for p in partition]

    return node



scale_dataset = []
with open('balance_scale.data', 'r') as f:
    for line in f.readlines():
        out, *features = line.strip().split(",")
        scale_dataset.append((tuple(features), out))

car_dataset = []
with open('car.data', 'r') as f:
    for line in f.readlines():
        *features, out = line.strip().split(",")
        car_dataset.append((tuple(features), out))

t = train_tree(scale_dataset, misclassification)
print((len(scale_dataset)/t.leaves()))
s = train_tree(car_dataset, misclassification)
print((len(car_dataset)/s.leaves()))
