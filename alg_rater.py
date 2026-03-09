import re

# add a check that the alg has to be in cubeshape, no misalign

def legal_move(m: int) -> int:
    """makes the move legal

    Args:
        m (int): -10 ~ 12 (i think)

    Returns:
        int: -5 ~ 6
    """
    if m < -5:
        return m + 12
    elif m > 6:
        return m - 12
    return m

def karnify(scramble: str) -> str:
    """karnifies the scramble

    Args:
        scramble (str): the scramble, 
                    e.g. "A/-3,0/-1,2/1,-2/-1,2/3,3/-2,-2/3,3/-3,0/-1,2/3,3/3,3/-2,4/A"

    Returns:
        str: after karnifying, e.g. "A U' d3 e m' e U' d e e T' A"
    """
    # slice separator
    sep = " / " if " / " in scramble else "/" if "/" in scramble else " "
    scramble = dict_replace(" " + scramble.replace(sep, " ") + " ", INV_NORM).replace(",", "").strip()
    scramble = re.sub(r" +", " ", scramble)
    return scramble

def unkarnify(scramble: str) -> str:
    """unkarnifies the scramble

    Args:
        scramble (str): the scramble, e.g. "A U' d3 e m' e U' d e e T' A"

    Returns:
        str: before karnifying, e.g. "A/-3,0/-1,2/1,-2/-1,2/3,3/-2,-2/3,3/-3,0/-1,2/3,3/3,3/-2,4/A"
    """
    return add_commas(" / ".join(
        filter(lambda a: a,dict_replace(dict_replace(" "+scramble+" ", NORM), NORM).split(" "))))

def add_commas(scramble: str) -> str:
    """adds commas to the scramble (part of unkarnifier)

    Args:
        scramble (str): e.g. "10/-30/-12/1-2/-12/33/-2-2/33/-30/-12/33/33/-24/-10"

    Returns:
        str: "1,0/-3,0/-1,2/1,-2/-1,2/3,3/-2,-2/3,3/-3,0/-1,2/3,3/3,3/-2,4/-1,0"
    """
    # slice separator
    sep = " / " if " / " in scramble else "/" if "/" in scramble else " "

    ret = scramble.split(sep)
    for i, m in enumerate(ret):
        if "," in m or m.lower() == "a":
            continue
        match len(m):
            case 2:
                ret[i] = m[0] + "," + m[1]
            case 3:
                ret[i] = m[0:2] + "," + m[2] if m[0] == "-" else m[0] + "," + m[1:]
            case 4:
                ret[i] = m[0:2] + "," + m[2:]
            case _:
                raise ValueError("this move is not valid: " + m)
    return sep.join(ret)

def dict_replace(s: str, d: dict) -> str:
    """Replace occurrences of keys of a dictionary in a string by the values.

    Args:
        s (str): the string to be replaced
        d (dict): the dictionary to pull from

    Returns:
        str: substituted string
    """
    keys = d.keys()
    pattern = re.compile("|".join(re.escape(k) for k in keys))
    while pattern.sub(lambda m: d[m.group(0)], s) != s:
        s = pattern.sub(lambda m: d[m.group(0)], s)
    return s

def ob_karn(a: str) -> bool:
    """checks whether alg is in karn by checking if letters are present

    Args:
        a (str): alg

    Returns:
        bool: verdict
    """
    l = list(a)
    l2 = [not i.isalpha() for i in l]
    return not all(l2)

GOOD = [
    "1,1", "-1,-1", "2,2", "-2,-2",
    "2,-1", "-2,1", "1,-2", "-1,2",
    "3,0", "-3,0", "0,3", "0,-3", "3,3", "3,-3", "-3,-3", "-3,3",
    "4,1", "-4,-1", "1,4", "-1,-4",
    "2,-4", "-2,4", "4,-2", "-4,2",
    "5,-1", "-5,1"
]

# def sep_index(a: str) -> int:
#     """returns the index of of the split of a move, english counting

#     Args:
#         a (str): e.g. "6-3"

#     Returns:
#         int: e.g. 1
#     """
#     l = list(a)
#     inx = 0
#     for char in l:
#         inx += 1
#         if char.isdigit():
#             break
#     return inx

def compl(a: str) -> str:
    """returns the complement move

    Args:
        a (str): e.g. "6,-3"

    Returns:
        str: e.g. "0,3"
    """
    l = a.split(",")
    return ",".join([str(legal_move(6+int(l[0]))), str(legal_move(6+int(l[1])))])

def l_f(a: str) -> str:
    """returns the layer-flipped move

    Args:
        a (str): e.g. "2,-1", "6,3"

    Returns:
        str: e.g. "-1,2", "3,6"
    """
    l = a.split(",")
    return ",".join([l[1], l[0]])

def add_moves(m1: str, m2: str) -> int:
    """adds two moves

    Args:
        m1 (str): e.g. "1,-2"
        m2 (str): e.g. "2,5"

    Returns:
        int: the added movement, e.g. 6
    """
    m1s = m1.split(",")
    m2s = m2.split(",")
    return int(m1s[0])+int(m2s[0]) + int(m1s[1])+int(m2s[1])

# def comma(a: str) -> str:
#     """adds a comma for the moves

#     Args:
#         a (str): e.g. "6-3"

#     Returns:
#         str: e.g. "6,-3"
#     """
#     inx = sep_index(a)
#     return ",".join([a[0:inx], a[inx:]])

CLOSEST = {
    -5: "6", -4: "-3", -3: "-3", -2: "-3", -1: "0", 0: "0",
    1: "0", 2: "3", 3: "3", 4: "3", 5: "6", 6: "6"
}

def normalize(a: str, k = None, leave: bool = True) -> str:
    """normalizes the alg

    Args:
        a (str): alg to be normalized
        k (bool | None): whether to be in karn, defaulted to follow alg
        leave (bool): whether to leave the alg alone and not normalize

    Returns:
        str: normalized alg
    """
    # no paren, no []
    a = re.sub(r"\[.*\]|\(|\)", "", a).strip().replace("\\", " ")
    k_i = ob_karn(a) # whether the scram is in karn
    k = k_i if k is None else k # whether to put it in karn

    if k_i:
        a = a.replace("/", " ")
        # turn it into numbers
        a = dict_replace(a, NORM)
        # no slash, no paren, potential comma
    else:
        # potential slash, potential paren, potential comma
        if "/" in list(a):
            # slash present, can safely replace space
            a = re.sub(r" ", "", a) # X space
            a = "/".join([f"{legal_move(int(i.split(",")[0]))},{legal_move(int(i.split(",")[1]))}"
                            for i in a.split("/")]) # make moves legal
            a = re.sub(r"\/", " ", a) # slash to space
        else:
            # no slash, prob karn in numbers
            a = re.sub(r" +", " ", a) # X mutiple spaces
            a = " ".join([f"{legal_move(int(i.split(",")[0]))},{legal_move(int(i.split(",")[1]))}"
                            for i in a.split(" ")]) # make moves legal
    a = add_commas(re.sub(r",", "", a)) # normalize commas

    # now alg in "1,0 5,-1 -5,1 -4,0"
    alst = a.split(" ")
    alst[-1] = "-1,0" if int(alst[-1][-1]) % 3 == 0 else "0,1"

    # now alg in "1,0 5,-1 -5,1 -1,0"
    l_fing = False
    facing_d = False # whether we need to l_f this move
    for i in range(1, len(alst) -2): # avoid checking the last actual move also
        m = alst[i]
        m = l_f(m) if facing_d else m
        if (not leave and m not in GOOD):
            m = compl(m)
            l_fing = not l_fing
        facing_d = not facing_d if l_fing else facing_d
        alst[i] = m
    # change the last move here
    alst[-2] = l_f(alst[-2]) if facing_d else alst[-2]
    alst[-2] = compl(alst[-2]) if not (l_fing == facing_d) else alst[-2]
    last_move = alst[-2]
    a = "/".join(alst)

    # now we can do formatting
    if k:
        a = re.sub(" ", "/", a) # space to slash
        a = karnify(a)
    comment = "" if last_move in [*GOOD, "-4,5", "-5,4", "6,3", "-1,5"] else " (bad finish)"
    comment += "" if alst[0][-1] == a[-1:] else " (alignment changes)"
    return a + comment

INV_NORM = {
    " U U' U U' ": " U4 ",
    " U' U U' U ": " U4' ",
    " D D' D D' ": " D4 ",
    " D' D D' D ": " D4' ",
    " u u' u u' ": " u4 ",
    " u' u u' u ": " u4' ",
    " d d' d d' ": " d4 ",
    " d' d d' d ": " d4' ",

    " U U' U ": " U3 ",
    " U' U U' ": " U3' ",
    " D D' D ": " D3 ",
    " D' D D' ": " D3' ",
    " u u' u ": " u3 ",
    " u' u u' ": " u3' ",
    " d d' d ": " d3 ",
    " d' d d' ": " d3' ",
    " F F' F ": " F3 ",
    " F' F F' ": " F3' ",
    " f f' f ": " f3 ",
    " f' f f' ": " f3' ",

    " U U' ": " W ",
    " U' U ": " W' ",
    " D D' ": " B ",
    " D' D ": " B' ",
    " u u' ": " w ",
    " u' u ": " w' ",
    " d d' ": " b ",
    " d' d ": " b' ",
    " F F' ": " F2 ",
    " F' F ": " F2' ",
    " f f' ": " f2 ",
    " f' f ": " f2' ",

    " U U ": " UU ",
    " U' U' ": " UU' ",
    " D D ": " DD ",
    " D' D' ": " DD' ",

    " 6,0 ": " U2 ",
    " 6,3 ": " U2D ",
    " 6,-3 ": " U2D' ",
    " 6,6 ": " U2D2 ",
    " 0,6 ": " D2 ",
    " 3,6 ": " UD2 ",
    " -3,6 ": " U'D2 ",

    " 3,0 ": " U ",
    " -3,0 ": " U' ",
    " 0,3 ": " D ",
    " 0,-3 ": " D' ",
    " 3,-3 ": " E ",
    " -3,3 ": " E' ",
    " 3,3 ": " e ",
    " -3,-3 ": " e' ",
    " 2,-1 ": " u ",
    " -1,2 ": " d ",
    " -4,-1 ": " F' ",
    " -1,-4 ": " f' ",
    " 2,-4 ": " T ",
    " -4,2 ": " t' ",
    " 2,2 ":" m ",
    " -1,-1 ": " M' ",
    " 5,-1 ":" u2 ",
    " -1,5 ": " d2 ",
    " -2,1 ":" u' ",
    " 1,-2 ":" d' ",
    " 4,1 ":" F ",
    " 1,4 ":" f ",
    " -2,4 ": " T' ",
    " 4,-2 ": " t ",
    " -2,-2 ":" m' ",
    " 1,1 ": " M ",
    " -5,1 ": " u2' ",
    " 1,-5 ": " d2' ",
    " -5,-2 ": " K' ",
    " 5,2 ": " K ",
    " 2,5 ": " k ",
    " -2,-5 ": " k' "
}
NORM = {v: k for k, v in INV_NORM.items()}

# since it's in CS then i can use one bit to represent the alignment
ALIGNMENT = ["a", "A"]
SLICESTARTS = ["\\", "/"]

MOVE_VALUES = {
    # 3 is a mediocre move
    # D
    "A/0,3": 9,
    "a/0,3": 3,
    "A\\0,3": 10,
    "a\\0,3": 3,
    # D2*
    "A/0,6": 1,
    "a/0,6": 5,
    "A\\0,6": 2,
    "a\\0,6": 5,
    # D'
    "A/0,-3": 9,
    "a/0,-3": 6,
    "A\\0,-3": 5,
    "a\\0,-3": 6,
    # U
    "A/3,0": 7,
    "a/3,0": 8,
    "A\\3,0": 3,
    "a\\3,0": 8,
    # e
    "A/3,3": 4,
    "a/3,3": 3,
    "A\\3,3": 7,
    "a\\3,3": 6,
    # UD2
    "A/3,6": 1,
    "a/3,6": 3,
    "A\\3,6": 2,
    "a\\3,6": 2,
    # E
    "A/3,-3": 7,
    "a/3,-3": 4,
    "A\\3,-3": 5,
    "a\\3,-3": 3,
    # U2
    "A/6,0": 6,
    "a/6,0": 2,
    "A\\6,0": 7,
    "a\\6,0": 2,
    # U2D
    "A/6,3": 7,
    "a/6,3": 1,
    "A\\6,3": 8,
    "a\\6,3": 1,
    # U2D2
    "A/6,6": 1,
    "a/6,6": 0,
    "A\\6,6": 3,
    "a\\6,6": 1,
    # U2D'
    "A/6,-3": 5,
    "a/6,-3": 2,
    "A\\6,-3": 3,
    "a\\6,-3": 1,
    # U'
    "A/-3,0": 3,
    "a/-3,0": 10,
    "A\\-3,0": 5,
    "a\\-3,0": 7,
    # E'
    "A/-3,3": 5,
    "a/-3,3": 4,
    "A\\-3,3": 7,
    "a\\-3,3": 5,
    # U'D2
    "A/-3,6": 3,
    "a/-3,6": 6,
    "A\\-3,6": 3,
    "a\\-3,6": 1,
    # e'
    "A/-3,-3": 4,
    "a/-3,-3": 6,
    "A\\-3,-3": 3,
    "a\\-3,-3": 3,

    # d*
    "/1,-2": 2,
    "\\1,-2": 7,
    "/-1,2": 9,
    "\\-1,2": 5,
    # d2*
    "/1,-5": 1,
    "\\1,-5": 1,
    "/-1,5": 5,
    "\\-1,5": 2,
    # f*
    "/1,4": 4,
    "\\1,4": 7,
    "/-1,-4": 6,
    "\\-1,-4": 2,
    # M*
    "/1,1": 2,
    "\\1,1": 10, 
    "/-1,-1": 10,
    "\\-1,-1": 2,
    # u*
    "/2,-1": 10,
    "\\2,-1": 3,
    "/-2,1": 7,
    "\\-2,1": 9,
    # m*
    "/2,2": 5,
    "\\2,2": 5,
    "/-2,-2": 7,
    "\\-2,-2": 2,
    # k*
    "/2,5": 5,
    "\\2,5": 3,
    "/-2,-5": 4,
    "\\-2,-5": 4,
    # T*
    "/2,-4": 7,
    "\\2,-4": 3,
    "/-2,4": 6,
    "\\-2,4": 8,
    # 44*
    "/4,4": 3,
    "\\4,4": 7,
    "/-4,-4": 6,
    "\\-4,-4": 2,
    # F*
    "/4,1": 3,
    "\\4,1": 6,
    "/-4,-1": 8,
    "\\-4,-1": 2,
    # t*
    "/4,-2": 6,
    "\\4,-2": 5,
    "/-4,2": 8,
    "\\-4,2": 6,
    # 4-5*
    "/4,-5": 1,
    "\\4,-5": 2,
    "/-4,5": 7,
    "\\-4,5": 3,
    # 55*
    "/5,5": 1,
    "\\5,5": 1,
    "/-5,-5": 1,
    "\\-5,-5": 0,
    # K*
    "/5,2": 3,
    "\\5,2": 5,
    "/-5,-2": 6,
    "\\-5,-2": 7,
    # u2*
    "/5,-1": 5,
    "\\5,-1": 3,
    "/-5,1": 6,
    "\\-5,1": 7,
    # 5-4*
    "/5,-4": 2,
    "\\5,-4": 1,
    "/-5,4": 6,
    "\\-5,4": 7
}

def get_move_value(startA: bool, upslice: bool, m: str) -> int:
    """get the ergonomicness of a move

    Args:
        startA (bool): whether the move starts with top misalign
        upslice (bool): whether the move is done upslice
        m (str): the move, e.g. "3,-3"

    Returns:
        int: the ergonomicness on a scale of 1-10
    """
    ms = m.split(",")
    if int(ms[0]) % 3 == 0:
        return MOVE_VALUES[ALIGNMENT[startA] + SLICESTARTS[upslice] + m]
    # not a multiple of 3, don't need alignments
    return MOVE_VALUES[SLICESTARTS[upslice] + m]

# constants and weights
WEIGHT1 = 10
WEIGHT2 = 50 # = the step weight * slice weight
WEIGHT3 = 10

alg = input()
alg = normalize(alg,False,False)

r = alg.split("/")
del r[-1] # we don't care about the end abf and the comments

# -------------- PHASE 1 ----------------------
ergo_up = 0
ergo_down = 0
# debug
ergo_up_text = ""
ergo_down_text = ""
for i, move in enumerate(r):
    if i == 0:
        # since we assume the state is no misalign
        is_top_A = int(move.split(",")[0]) % 3 != 0
        odd_slice = True
        continue
    ergo_up += get_move_value(is_top_A, odd_slice, move)
    ergo_up_text += str(get_move_value(is_top_A, odd_slice, move)) + "+"
    ergo_down += get_move_value(is_top_A, not odd_slice, move)
    ergo_down_text += str(get_move_value(is_top_A, not odd_slice, move)) + "+"
    is_top_A = is_top_A != (int(move.split(",")[0]) % 3 != 0)
    odd_slice = not odd_slice

PHASE1 = WEIGHT1 * max(ergo_up, ergo_down)
master_text = ergo_up_text if ergo_up >= ergo_down else ergo_down_text
if abs(ergo_up - ergo_down) >= 10:
    # specify downslice upslice
    alg.replace(" ", "/" if ergo_up > ergo_down else "\\", 1)

# ----------------------- PHASE 2 -----------------------
PHASE2 = WEIGHT2 * alg.count("/")
master_text += f" - {WEIGHT2} * {alg.count("/")} slices"

# ------------------------ PHASE 3 ---------------------
del r[0]
total_movement = 0
for i, move in enumerate(r):
    if i == len(r) - 1:
        break
    total_movement += add_moves(move, r[i+1])
PHASE3 = WEIGHT3 * total_movement
master_text += f" - {WEIGHT3} * {total_movement} moves"

FINAL = PHASE1 - PHASE2 - PHASE3

# return (alg, ergo_up, ergo_down)
# print(alg, ergo_up_text[:-1]+"="+str(ergo_up), ergo_down_text[:-1]+"="+str(ergo_down), sep="\n")
