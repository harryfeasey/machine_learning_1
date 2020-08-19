

def matches(data, hypothesis):
    matched = []

    for x, y in zip(data, hypothesis):
        matched_item = False
        if x == '?':
            matched_item = True
        elif x != '0' and (x == y or y == '0'):
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


def min_specializations(h, domains, x):
    results = []
    for i in range(len(h)):
        if h[i] == "?":
            for domain in domains[i]:
                if x[i] != domain:
                    h_new = h[:i] + (domain,) + h[i+1:]
                    results.append(h_new)
        elif h[i] != "0":
            h_new = h[:i] + ('0',) + h[i+1:]
            results.append(h_new)
    return results


def cea_trace(domains, training_examples):
    S = {('0',) * (len(domains))}
    G = {('?',) * (len(domains))}

    s_trace = [S]
    g_trace = [G]

    for data, output in training_examples:

        G = G.copy()
        S = S.copy()

        # if d is positive example
        if output:
            # Remove from G any hypotheses that do not match data
            G = {hyp for hyp in G.copy() if (matches(hyp, data))}

            for s in S.copy():

                # For each hypothesis s in S that does not match data:
                if not matches(s, data):
                    #  Remove s from S
                    S.remove(s)

                    #  Add to S all minimal generalisations, h of s such that:
                    Splus = min_generalizations(s, data)
                    for min in Splus:
                        # 1. h matches data
                        # 2. some member of G is more general than h
                        if any([matches(g, min) for g in G]):
                            S.add(min)

            # Remove from S any h that is more general than another hypothesis in S
            S.difference_update([h for h in S if
                                 any([matches(h, h1)
                                      for h1 in S if h != h1])])

        # if d is negative example
        else:
            # Remove from S any hypotheses that match data
            S = {hyp for hyp in S if not (matches(hyp, data))}

            # For each hypothesis g in G that matches data:
            #       Remove g from G
            #       Add to G all minimal generalisations, h, of g such that:
            #           1. h does not match data
            #           2. some member of S is more specific than h
            # Remove from G any h that is more specific than another hypothesis in G

            for g in G.copy():
                if matches(g, data):
                    G.remove(g)
                    Gminus = min_specializations(g, domains, data)

                    for min in Gminus:
                        if any([matches(min, s) for s in S]):
                            G.add(min)

            # remove hypotheses less general than any other in G
            G.difference_update([h for h in G if
                                 any([matches(g1, h)
                                      for g1 in G if h != g1])])

        # Update Traces
        g_trace.append(G)
        s_trace.append(S)

    return s_trace, g_trace

def all_agree(S, G, x):
    return {matches(s, x) for s in S} == {matches(g, x) for g in G}



domains = [
    {'T', 'F'},
    {'T', 'F'},
]

training_examples = [
    (('F', 'F'), True),
    (('T', 'T'), False),
]

S_trace, G_trace = cea_trace(domains, training_examples)
S, G = S_trace[-1], G_trace[-1]
print(S)
print(G)
print("(F, F)", all_agree(S, G, ('F', 'F')), "T")
print("(T, T)", all_agree(S, G, ('T', 'T')), "T")
print("(F, T)", all_agree(S, G, ('F', 'T')), "F")
print("(T, F)", all_agree(S, G, ('T', 'F')), "F")
print()