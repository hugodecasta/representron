seq1 = 'defdefdefLLLOOLLLdefdefdef'
seq2 = 'abcabcabcLLLOOLLLaaaaaaaaa'

def create_network(sequence):
    net = {'@':sequence[0],None:[]}
    for i in range(len(sequence)):
        sym = sequence[i]
        next_sym = None
        if i < len(sequence)-1:
            next_sym = sequence[i+1]
        if sym not in net:
            net[sym] = []
        net[sym].append(next_sym)
    return net

def is_direct(stack):
    f_sym = stack[0]
    for sym in stack:
        if not sym == f_sym:
            return False
    return True

def find_episods(net):
    episods = []
    sym_to_process = [net['@']]
    current_episod = {}
    while len(sym_to_process) > 0:
        sym = sym_to_process[0]
        del sym_to_process[0]
        stack = net[sym]
        if current_episod == {}:
            current_episod['@'] = sym
        current_episod[sym] = stack
        if not is_direct(stack):
            episods.append(current_episod)
            current_episod = {}
        else:
            for ssym in stack:
                if ssym not in sym_to_process:
                    sym_to_process.append(ssym)
    return episods

net = create_network(seq1)
epi = find_episods(net)
print(net)
print(epi)