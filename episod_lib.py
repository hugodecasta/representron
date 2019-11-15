
# ------------------------------------------------------

def printeo(epi_occu):
    for episod,nb in epi_occu.items():
        print('"'+episod+'"',nb)

# ------------------------------------------------------

def printe(episods):
    for index,episod in episods.items():
        print(index,':',episod)

# ------------------------------------------------------

def prints(seq):
    print(''.join([str(elm) for elm in seq]))

# ------------------------------------------------------

def find_all(episod, sequence, only_one=False):
    indexes = []
    ft_index = -1
    ep_index = 0
    ep_len = 0
    for index in range(len(sequence)):
        sym = sequence[index]
        if sym == episod[ep_index]:
            if ft_index == -1:
                ft_index = index
            ep_len += 1
            ep_index += 1
        if ep_len == len(episod):
            indexes.append(ft_index)
            if only_one:
                return indexes
            ft_index = -1
            ep_index = 0
            ep_len = 0
    return indexes

def appears(episod, sequence):
    return len(find_all(episod,sequence,True)) > 0

def replace_all(episod, replacer, sequence):
    new_sequence = []
    indexes = find_all(episod, sequence)
    index = 0
    while index < len(sequence):
        if index in indexes:
            new_sequence.append(replacer)
            index += len(episod)
        else:
            new_sequence.append(sequence[index])
            index += 1
    return new_sequence

# ------------------------------------------------------

def get_all_episod(sequence):
    episods = list()
    for le in range(2,len(sequence)):
        for i in range(0,len(sequence)-le):
            episod = sequence[i:i+le]
            episods.append(episod)
    return episods

def get_all_episod_occurance(sequence):
    episods = {}
    for le in range(2,len(sequence)):
        for i in range(0,len(sequence)-le):
            episod = tuple(sequence[i:i+le])
            if not episod in episods:
                nb = len(find_all(episod,sequence))
                episods[episod] = nb
    return episods

# ------------------------------------------------------

def sort_episod_occurance(episods):

    appear = {}
    can_keep = {}

    for sym in episods:
        appear[sym] = []
        can_keep[sym] = True
        for ssym in episods:
            if appears(sym,ssym) and not ssym == sym:
                appear[sym].append(ssym)

    for sym,nb in episods.items():
        if nb == 1 or not can_keep[sym]:
            can_keep[sym] = False
            continue
        for ssym in appear[sym]:
            nb2 = episods[ssym]
            elsewhere = nb > nb2
            if elsewhere:
                can_keep[ssym] = False
            else:
                can_keep[sym] = False

    return dict([(sym,nb) for sym,nb in episods.items() if can_keep[sym]])

# ------------------------------------------------------

def create_episod_index(epi_occu, sequence):
    next_index = 0
    for sym in sequence:
        try:
            if sym >= next_index:
                next_index = sym + 1
        except:
            continue
    episods = {}
    for episod in epi_occu:
        episods[next_index] = episod
        next_index += 1
    return episods

# ------------------------------------------------------

def rewrite(sequence,episods):
    new_sequence = sequence[:]
    for index,episod in episods.items():
        new_sequence = replace_all(episod,index,new_sequence)
    return new_sequence

# ------------------------------------------------------

def get_episods(sequence):
    epi_occu = get_all_episod_occurance(sequence)
    epi_occu_sorted = sort_episod_occurance(epi_occu)
    episods = create_episod_index(epi_occu_sorted, sequence)
    return episods

# ------------------------------------------------------

def analyse_sequence(sequence):
    episods = get_episods(sequence)
    new_seq = rewrite(sequence,episods)
    return episods,new_seq

# ------------------------------------------------------

def analyse_stack(sequence):
    new_seq = sequence[:]
    do_next = True
    abstract = []
    while do_next:
        episods,next_seq = analyse_sequence(new_seq)
        abstract.append((new_seq,episods,next_seq))
        new_seq = next_seq
        do_next = len(list(episods.keys())) > 1
    return abstract

# ------------------------------------------------------