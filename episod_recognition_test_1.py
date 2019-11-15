from episod_lib import get_all_episod, printe

# --------------------------------------------------------

def epirule_equals(source, new):
    if len(source) is not len(new):
        return False
    for index in range(len(source)):
        src_sym = source[index]
        new_sym = new[index]
        if src_sym is not new_sym:
            return False
    return True

def epirule_reversed(source, new):
    equal = epirule_equals(source, new)
    reverse = epirule_equals(list(reversed(source)), new)
    return reverse and not equal

# ----------------------------------------------

rules = {
    'equals':epirule_equals,
    'reversed':epirule_reversed
}

# --------------------------------------------------------

sequence = 'abLLOabOLLab'
episods = get_all_episod(sequence)

for from_i in range(len(episods)):
    for to_i in range(from_i+1, len(episods)):
        source = episods[from_i]
        new = episods[to_i]
        for rule, meth in rules.items():
            if meth(source,new):
                print(rule,source,new)