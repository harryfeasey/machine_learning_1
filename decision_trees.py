import math

class DTNode:
    def __init__(self, decision):
        self.children = []
        self.decision = decision

    def predict(self, input):
        if callable(self.decision):
            child = self.children[self.decision(input)]
            return child.predict(input)
        else:
            return self.decision

    def leaves(self):
        if not self.children:
            return 1
        return sum([child.leaves() for child in self.children])


def partition_by_feature_value(feature_index, dataset):

    features = []
    labels = {}

    for feature, label in dataset:

        if feature[feature_index] in labels:
            labels[feature[feature_index]].append((feature, label))
        else:
            labels[feature[feature_index]] = [(feature, label)]

    partition = [label for label in labels.values()]

    def separator(x):
        i = 0
        for item in labels.values():
            for feature, label in item:
                if feature == x:
                    return i
            i += 1

    return separator, partition


def p_k(dataset, classification):
    count = 0
    for feature, label in dataset:
        if label == classification:
            count += 1

    return count / len(dataset)


def misclassification(dataset):
    all_classes = get_classifications(dataset)
    p_ks = []
    for classification in all_classes:
        p_ks.append(p_k(dataset, classification))

    return 1 - max(p_ks)


def gini(dataset):
    # ∑k pk(1 - pk).

    all_classes = get_classifications(dataset)
    p_k_sum = 0
    for classification in all_classes:
        p_k_sum += p_k(dataset, classification) * (1 - p_k(dataset, classification))

    return p_k_sum


def entropy(dataset):
    # -∑k pk log(pk).
    all_classes = get_classifications(dataset)
    p_k_sum = 0
    for classification in all_classes:
        p_k_sum += p_k(dataset, classification) * (math.log(p_k(dataset, classification)))

    return -p_k_sum


def get_classifications(dataset):
    classifications = []
    for feature, label in dataset:
        classifications.append(label)

    return set(classifications)


def objective(dataset, k, criterion):
    separator, partition = partition_by_feature_value(k, dataset)
    obj = float('-inf')
    if len(partition) != 1:
        obj = sum([(len(part)/len(dataset)) * criterion(part) for part in partition])
    return obj

def max_(items):
    maximum = max(items)
    return items.index(maximum)

def train_tree(dataset, criterion):

    classes = get_classifications(dataset)
    all_labels = [x for _,x in dataset]
    all_features = [y for y,_ in dataset]
    most_common = max(set(all_labels), key=all_labels.count)

    if len(classes) == 1:
        return DTNode(classes.pop())
    elif len(all_features) == 0: # Empty feature set
        return DTNode(classes[max_([p_k(k, dataset) for k in classes])])

    obj_items = ([objective(dataset, k, criterion) for k in range(len(dataset[0][0]))])
    split_index = obj_items.index(max(obj_items))
    separator, partition = partition_by_feature_value(split_index, dataset)

    sub_tree = DTNode(separator)
    sub_tree.children = [train_tree(p, criterion) for p in partition]

    return sub_tree


dataset = [
    (("Sunny",    "Hot",  "High",   "Weak"),   False),
    (("Sunny",    "Hot",  "High",   "Strong"), False),
    (("Overcast", "Hot",  "High",   "Weak"),   True),
    (("Rain",     "Mild", "High",   "Weak"),   True),
    (("Rain",     "Cool", "Normal", "Weak"),   True),
    (("Rain",     "Cool", "Normal", "Strong"), False),
    (("Overcast", "Cool", "Normal", "Strong"), True),
    (("Sunny",    "Mild", "High",   "Weak"),   False),
    (("Sunny",    "Cool", "Normal", "Weak"),   True),
    (("Rain",     "Mild", "Normal", "Weak"),   True),
    (("Sunny",    "Mild", "Normal", "Strong"), True),
    (("Overcast", "Mild", "High",   "Strong"), True),
    (("Overcast", "Hot",  "Normal", "Weak"),   True),
    (("Rain",     "Mild", "High",   "Strong"), False),
]
t = train_tree(dataset, misclassification)
print(t.predict(("Overcast", "Cool", "Normal", "Strong")))
print(t.predict(("Sunny", "Cool", "Normal", "Strong")))
