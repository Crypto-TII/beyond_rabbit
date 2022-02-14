## SUPPORT --> Add to comparison.py from this point

# R is a constant public value, and k is the bitsize
# returns a python array of regints with the bit expansion of R (sbit)
def decompose_to_regints(R, k):
    from library import extract_bits
    bits = extract_bits(R, k)
    response = [regint(bit) for bit in bits]

    return response


## FUNCTIONALITY


# R is a constant public value, x is sbit bit expansion of x, and k is the bitsize
# returns R <= x
def less_than_eq_gc(R, x, k):
    """
      res = R <? x (logarithmic rounds version)

      R: clear integer register
      x: array of secret bits
      """

    use_preOpL = 1
    R_bits = decompose_to_regints(R, k)

    y = [sbit() for _ in range(k)]
    z = [None for _ in range(k)]
    w = [None for _ in range(k)]

    for i in range(k):
        if isinstance(x[i], sbit):
            val = sregint(x[i])
        elif isinstance(x[i], sregint):
            val = x[i]
        else:
            raise CompilerError("NotImplemented")
        bitsint(y[i], val ^ (R_bits[i]), 0)
        y[i] = ~y[i]

    z[k - 1] = y[k - 1]
    w[k - 1] = ~y[k - 1]

    y = y[::-1]

    def and_op(x, y, z=None):
        return x & y

    if use_preOpL:
        z = PreOpL(and_op, y)[::-1]

    for i in range(k - 1, 0, -1):  # no optimizing
        w[i - 1] = z[i - 1] ^ z[i]

    out = [sbit() for _ in range(k)]
    for i in range(k):
        bitsint(out[i], R_bits[i] & sregint(w[i]), 0)

    total = out[0]
    for i in range(1, k):
        total = total ^ out[i]

    return ~total


# absolute comparison between 2 sregints
# returns R <= x
# TODO generic and  non generic have redundant funcionality
def less_than_eq_gc_generic(X_bits, Y_bits, k):
    """
      res = R <? x (logarithmic rounds version)

      R: clear integer register
      x: array of secret bits
      """

    use_preOpL = 1

    y = [sbit() for _ in range(k)]
    z = [None for _ in range(k)]
    w = [None for _ in range(k)]

    for i in range(k):
        val = X_bits[i]
        y[i] = val ^ (Y_bits[i])
        y[i] = ~y[i]

    z[k - 1] = y[k - 1]
    w[k - 1] = ~y[k - 1]

    y = y[::-1]

    def and_op(x, y, z=None):
        return x & y

    if use_preOpL:
        z = PreOpL(and_op, y)[::-1]

    for i in range(k - 1, 0, -1):  # no optimizing
        w[i - 1] = z[i - 1] ^ z[i]

    out = [sbit() for _ in range(k)]
    for i in range(k):
        out[i] = X_bits[i] & w[i]

    total = out[0]
    for i in range(1, k):
        total = total ^ out[i]
    return ~total


# R is a constant public value, x is sbit bit expansion of x, and k is the bitsize
# returns R <= x (sregint)
def less_than_eq_gc_sregint(R, x, k):
    return sregint(less_than_eq_gc(R, x, k))


# R is a constant public value, x is sbit bit expansion of x, and k is the bitsize
# returns R <= x (sint)
def less_than_eq_gc_sint(R, x, k):
    return sint(less_than_eq_gc(R, x, k))


# hack for circular dependency
from instructions import *
