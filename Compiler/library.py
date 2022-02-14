## additional imports
from util import bit_decompose
from Compiler.comparison import less_than_eq_gc


##SUPPORT## --> Add to library.py from this point

# R is cint/ int input, k is the bitsize
# returns a python array with the sbits of x
def extract_bits(R, k):
    return bit_decompose(R, k)


# x is sregint input, k is the bitsize
# returns a python array with the sbits of x
def extract_sbits(x, k):
    response = []
    for i in range(k):
        bit = sbit()
        bitsint(bit, x, i)
        response.append(bit)
    return response


## FUNCTIONALITY PPML ##
# UTILS
# FILLING, RETURN ARRAYS and LISTS

# R_p and R_2 are empty arrays, k is the bitsize
# fills R_p and _R2 with k dabits
def fill_dabit_array(R_p, R_2, k):
    # randomness
    _R_p, _R_2 = get_random_dabit(k)

    # recording
    _R_2_sregint = sregint(_R_2, k)
    _R_p.store_in_mem(R_p.address)
    _R_2_sregint.store_in_mem(R_2.address)


# R_p and R_2 are empty lists, k is the bitsize
# fills R_p and _R2 with k dabits
def fill_dabit_list(R_p, R_2, k):
    # randomness
    for _ in range(k):
        r_p, r_2 = get_random_dabit()
        R_p.append(r_p)
        R_2.append(r_2)


# k is the bitsize
# returns arrays of dabits of size k
def get_dabit_list(k):
    # intstantiation
    R_p = []
    R_2 = []
    fill_dabit_list(R_p, R_2, k)
    return R_p, R_2


# k is the bitsize
# returns arrays of dabits of size k
def get_dabit_array(k):
    # intstantiation
    R_p = Array(k, sint)
    R_2 = Array(k, sregint)
    fill_dabit_array(R_p, R_2, k)
    return R_p, R_2


# _p is the bound, k is the bitsize
# returns bounded arrays by p
def get_dabit_array_p(_p, k):
    R_p = Array(k, sint)
    R_2 = Array(k, sregint)

    @while_do(lambda x: x == 1, 1)
    def loop_body(i):
        fill_dabit_array(R_p, R_2, k)
        i = less_than_eq_gc(_p, R_2, k).reveal()
        return i

    return R_p, R_2


# CONSTRUCTING r_p and r_2 (inestable) randomness

# k is the bisize
# returns an integer base p, bit expansion and mod 2, to obtain dabits randomness.
# ideal method for randomness < 64 bits
# TODO: make it vectorized
def combine_dabit(R_p, R_2, k):
    r_p = sint(0)
    r_2 = sregint(0)
    for i in range(k):
        bit_p = R_p[i]
        temp = sregint()
        if isinstance(R_2[i], sbit):
            bit_2 = R_2[i]
        else:
            bit_2 = sbit()
            bitsint(bit_2, R_2[i], 0)

        r_p = (2 ** i) * bit_p + r_p
        sintbit(temp, r_2, bit_2, i)
        r_2 = temp
    return r_p, r_2


# FUNCTIONALITY - RETURNING RANDOMNESS

# k is the bitsize
def get_random_from_vector_dabit(k):
    R_p = Array(k, sint)
    R_2 = Array(k, sregint)
    fill_dabit_array(R_p, R_2, k)
    r_p, r_2 = combine_dabit(R_p, R_2, k)
    return r_p, R_p, r_2, R_2


# k is the bitsize
def get_random_from_dabit_list(k):
    R_p = []
    R_2 = []
    fill_dabit_list(R_p, R_2, k)
    r_p, r_2 = combine_dabit(R_p, R_2, k)
    return r_p, R_p, r_2, R_2


# _p is the bound, k is the bitsize
def get_random_p_from_dabit(_p, k):
    R_p, R_2 = get_dabit_array_p(_p, k)
    r_p, r_2 = combine_dabit(R_p, R_2, k)
    return r_p, R_p, r_2, R_2


# k is the bisize
# returns an integer base p, bit expansion and mod 2, to obtain dabits randomness.
# Do Not use vectors
# TODO: make it vectorized
def get_random_from_single_dabits(k):
    r_p = sint(0)
    r_2 = sregint(0)
    R_p = Array(k, sint)
    R_2 = Array(k, sregint)
    for i in range(k):
        bit_p = sint()
        bit_2 = sbit()
        dabit(bit_p, bit_2)
        _bit_2 = sregint(bit_2)
        R_p[i] = bit_p
        R_2[i] = _bit_2
        r_p = 2 ** i * (bit_p) + r_p
        r_2 = 2 ** i * (_bit_2) + r_2
    return r_p, R_p, r_2, R_2
