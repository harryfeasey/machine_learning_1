

def cea_trace(domains, training_examples):
    S = ['0']*(len(training_examples) + 1)
    G = ['?']*(len(training_examples) + 1)

    s_trace = [S]
    g_trace = [G]
    print(S, G)

    for data, output in training_examples:
        if output:
            pass
            # Remove from G any hypotheses that do not match data

        # For each hypothesis s in S that does not match data
            # Remove s from S
            # Add to S all minimal generalisations, h of s such that:
                # h matches d
                # some member of G is more general than h





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