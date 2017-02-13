import math

def get_percentile(l, p) :
    """
        function that returns the p-th percentile from a list

        :param l    The original list
        :param p    The percentile
        :return     The number at that specific percentile
    """
    cpy = list(l)
    cpy.sort()

    poz = len(cpy) * p
    poz = math.ceil(poz)

    return cpy[poz]