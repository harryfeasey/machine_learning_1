

def matches(data, hypothesis):
    matched = []

    for x, y in zip(hypothesis, data):
        matched_item = False
        if x != "0":
            if x == "?":
                matched_item = True
            elif x == y or y == "0":
                matched_item = True
        matched.append(matched_item)

    return all(matched)


def min_generalizations(h, x):
    h_new = list(h)

    for i in range(len(h)):

        if not matches(h[i:i + 1], x[i:i + 1]):
            if h[i] != '0':
                h_new[i] = '?'
            else:
                h_new[i] = x[i]

    return [tuple(h_new)]


def cea_trace(domains, training_examples):
    S = set(('0',) * (len(training_examples) + 1))
    G = set(('?',) * (len(training_examples) + 1))

    s_trace = [S]
    g_trace = [G]
    print(S, G)

    for data, output in training_examples:

        # if d is positive example
        if output:
            # Remove from G any hypotheses that do not match data
            G = {hyp for hyp in G if (matches(data, hyp))}
            print(G)

            # For each hypothesis s in S that does not match data:
            #       Remove s from S
            #       Add to S all minimal generalisations, h of s such that:
            #           1. h matches data
            #           2. some member of G is more general than h
            # Remove from S any h that is more general than another hypothesis in S

            # Update Traces
            g_trace.append(G)
            s_trace.append(S)

        # if d is negative example
        else:
            # Remove from S any hypotheses that match data
            S = {hyp for hyp in S if not (matches(data, hyp))}

            # For each hypothesis g in G that matches data:
            #       Remove g from G
            #       Add to G all minimal generalisations, h, of g such that:
            #           1. h does not match data
            #           2. some member of S is more specific than h
            # Remove from G any h that is more specific than another hypothesis in G

            # Update Traces
            g_trace.append(G)
            s_trace.append(S)

    return s_trace, g_trace


domains = [
    {'red', 'blue'}
]

training_examples = [
    (('red',), True)
]

S_trace, G_trace = cea_trace(domains, training_examples)
print(len(S_trace), len(G_trace))
print(all(type(x) is set for x in S_trace + G_trace))
S, G = S_trace[-1], G_trace[-1]
print(len(S), len(G))
