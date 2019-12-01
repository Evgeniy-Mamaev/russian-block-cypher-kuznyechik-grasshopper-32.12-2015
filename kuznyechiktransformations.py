PRIMITIVE_POLYNOMIAL = int("111000011", 2)
NUMBER_OF_BYTES = 16
LINEAR_TRANSFORMATION_CONSTANTS = [148, 32, 133, 16, 194, 192, 1, 251, 1, 192, 194, 16, 133, 32, 148, 1]
NONLINEAR_SUBSTITUTION = [252, 238, 221, 17, 207, 110, 49, 22, 251, 196, 250, 218, 35, 197, 4, 77, 233,
                          119, 240, 219, 147, 46, 153, 186, 23, 54, 241, 187, 20, 205, 95, 193, 249, 24, 101,
                          90, 226, 92, 239, 33, 129, 28, 60, 66, 139, 1, 142, 79, 5, 132, 2, 174, 227, 106, 143,
                          160, 6, 11, 237, 152, 127, 212, 211, 31, 235, 52, 44, 81, 234, 200, 72, 171, 242, 42,
                          104, 162, 253, 58, 206, 204, 181, 112, 14, 86, 8, 12, 118, 18, 191, 114, 19, 71, 156,
                          183, 93, 135, 21, 161, 150, 41, 16, 123, 154, 199, 243, 145, 120, 111, 157, 158, 178,
                          177, 50, 117, 25, 61, 255, 53, 138, 126, 109, 84, 198, 128, 195, 189, 13, 87, 223,
                          245, 36, 169, 62, 168, 67, 201, 215, 121, 214, 246, 124, 34, 185, 3, 224, 15, 236,
                          222, 122, 148, 176, 188, 220, 232, 40, 80, 78, 51, 10, 74, 167, 151, 96, 115, 30, 0,
                          98, 68, 26, 184, 56, 130, 100, 159, 38, 65, 173, 69, 70, 146, 39, 94, 85, 47, 140, 163,
                          165, 125, 105, 213, 149, 59, 7, 88, 179, 64, 134, 172, 29, 247, 48, 55, 107, 228, 136,
                          217, 231, 137, 225, 27, 131, 73, 76, 63, 248, 254, 141, 83, 170, 144, 202, 216, 133,
                          97, 32, 113, 103, 164, 45, 43, 9, 91, 203, 155, 37, 208, 190, 229, 108, 82, 89, 166,
                          116, 210, 230, 244, 180, 192, 209, 102, 175, 194, 57, 75, 99, 182]
HEX_BIN_DICTIONARY = {
    '0': int("0000", 2),
    '1': int("0001", 2),
    '2': int("0010", 2),
    '3': int("0011", 2),
    '4': int("0100", 2),
    '5': int("0101", 2),
    '6': int("0110", 2),
    '7': int("0111", 2),
    '8': int("1000", 2),
    '9': int("1001", 2),
    'a': int("1010", 2),
    'b': int("1011", 2),
    'c': int("1100", 2),
    'd': int("1101", 2),
    'e': int("1110", 2),
    'f': int("1111", 2),
}

"""
General note: digital indexes can be used either for pointing an index in an array 
or for showing upper (power) or lower literal index.
"""


def x(k, a):
    """
    X[k]: V 128 → V 128.
    X[k](a) = k ⊕ a, where k, a ∈ V 128.
    :param k: array of bytes of size 16.
    :param a: array of bytes of size 16.
    """
    if len(k) != NUMBER_OF_BYTES or len(a) != NUMBER_OF_BYTES:
        raise ValueError('The array length is not equal to {0}.'.
                         format(NUMBER_OF_BYTES))
    return list(b ^ c for b, c in zip(k, a))


def l(array_of_bytes):
    """
    l(a 15 , ..., a 0 ) = ∇(148 ∙ ∆(a 15 ) + 32 ∙ ∆(a 14 ) + 133 ∙ ∆(a 13 ) + 16 ∙ ∆(a 12 ) +
    194 ∙ ∆(a 11 ) + 192 ∙ ∆(a 10 ) + 1 ∙ ∆(a 9 ) + 251 ∙ ∆(a 8 ) + 1 ∙ ∆(a 7 ) + 192 ∙ ∆(a 6 ) +
    194 ∙ ∆(a 5 ) + 16 ∙ ∆(a 4 ) + 133 ∙ ∆(a 3 ) + 32 ∙ ∆(a 2 ) + 148 ∙ ∆(a 1 ) + 1 ∙ ∆(a 0 )).
    :param array_of_bytes: array of bytes of size 16.
    """
    if len(array_of_bytes) != NUMBER_OF_BYTES:
        raise ValueError('The array length is not equal to {0}.'.
                         format(NUMBER_OF_BYTES))
    result = 0
    for i in range(NUMBER_OF_BYTES):
        result ^= multiply_elements(array_of_bytes[i], LINEAR_TRANSFORMATION_CONSTANTS[i])
    return result


def s(array_of_bytes):
    """
    S: V 128 → V 128.
    S(a) = S(a 15 ||...||a 0 ) = π(a 15 )||...||π(a 0 ),
    where a = a 15 ||...||a 0 ∈ V 128 , a i ∈ V 8 , i = 0, 1, ..., 15.
    :param array_of_bytes: array of bytes of size 16.
    """
    if len(array_of_bytes) != NUMBER_OF_BYTES:
        raise ValueError('The array length is not equal to {0}.'.
                         format(NUMBER_OF_BYTES))
    return list(NONLINEAR_SUBSTITUTION[e] for e in array_of_bytes)


def s_reversed(array_of_bytes):
    """
    S -1 : V 128 → V 128, a reverse transformation to the S.
    S -1 (a) = S (a 15 ||...||a 0 ) = π -1 (a 15 )||...||π -1 (a 0 ),
    где a = a 15 ||...||a 0 ∈ V 128 , a i ∈ V 8 , i = 0, 1, ..., 15,
    π -1 – a substitution, reversed to the substitution π.
    :param array_of_bytes: array of bytes of size 16.
    """
    if len(array_of_bytes) != NUMBER_OF_BYTES:
        raise ValueError('The array length is not equal to {0}.'.
                         format(NUMBER_OF_BYTES))
    flipped_nonlinear_substitution = dict((v, i) for i, v in enumerate(NONLINEAR_SUBSTITUTION))
    return list(flipped_nonlinear_substitution[e] for e in array_of_bytes)


def r(array_of_bytes):
    """
    R: V 128 → V 128
    R(a) = R(a 15 ||...||a 0 ) = l(a 15 , ..., a 0 )||a 15 ||...||a 1 ,
    where a = a 15 ||...||a 0 ∈ V 128 , a i ∈ V 8 , i = 0, 1, ..., 15.
    :param array_of_bytes: array of bytes of size 16.
    """
    if len(array_of_bytes) != NUMBER_OF_BYTES:
        raise ValueError('The array length is not equal to {0}.'.
                         format(NUMBER_OF_BYTES))
    temp = l(array_of_bytes)
    for i in range(NUMBER_OF_BYTES - 2, -1, -1):
        array_of_bytes[i + 1] = array_of_bytes[i]
    array_of_bytes[0] = temp
    return array_of_bytes


def r_reversed(array_of_bytes):
    """
    R -1 : V 128 → V 128
    A reversed transformation to the transformation R.
    R -1 (a) = R -1 (a 15 ||...||a 0 ) =
    = a 14 ||a 13 ||...||a 0 ||l(a 14 , a 13 , ..., a 0 , a 15 ),
    where a = a 15 ||...||a 0 ∈ V 128 , a i ∈ V 8 , i = 0, 1, ..., 15.
    :param array_of_bytes: array of bytes of size 16.
    """
    if len(array_of_bytes) != NUMBER_OF_BYTES:
        raise ValueError('The array length is not equal to {0}.'.
                         format(NUMBER_OF_BYTES))
    temp = array_of_bytes[0]
    for i in range(NUMBER_OF_BYTES - 1):
        array_of_bytes[i] = array_of_bytes[i + 1]
    array_of_bytes[NUMBER_OF_BYTES - 1] = temp
    array_of_bytes[NUMBER_OF_BYTES - 1] = l(array_of_bytes)
    return array_of_bytes


def big_l(array_of_bytes):
    """
    L: V 128 → V 128.
    L(a) = R 16 (a),
    where a ∈ V 128.
    :param array_of_bytes: array of bytes of size 16.
    """
    if len(array_of_bytes) != NUMBER_OF_BYTES:
        raise ValueError('The array length is not equal to {0}.'.
                         format(NUMBER_OF_BYTES))
    for _ in range(NUMBER_OF_BYTES):
        array_of_bytes = r(array_of_bytes)
    return array_of_bytes


def big_l_reversed(array_of_bytes):
    """
    L -1 : V 128 → V 128.
    L -1 (a) = (R -1 ) 16 (a),
    where a ∈ V 128 ;
    :param array_of_bytes: array of bytes of size 16.
    """
    if len(array_of_bytes) != NUMBER_OF_BYTES:
        raise ValueError('The array length is not equal to {0}.'.
                         format(NUMBER_OF_BYTES))
    for _ in range(NUMBER_OF_BYTES):
        array_of_bytes = r_reversed(array_of_bytes)
    return array_of_bytes


def f(k, two_arrays_of_bytes):
    """
    F [k]: V 128 × V 128 → V 128 × V 128
    F [k](a 1 , a 0 ) = (LSX[k](a 1 ) ⊕ a 0 , a 1 ),
    where k, a 0 , a 1 ∈ V 128.
    :param k: array of bytes of size 16.
    :param two_arrays_of_bytes: two arrays of bytes of size 16.
    """
    number_of_arrays = 2
    if len(two_arrays_of_bytes) != number_of_arrays:
        raise ValueError('The number of arrays is not equal to {0}.'.
                         format(number_of_arrays))
    if len(two_arrays_of_bytes[0]) != NUMBER_OF_BYTES or len(two_arrays_of_bytes[1]) != NUMBER_OF_BYTES:
        raise ValueError('The array length is not equal to {0}.'.
                         format(NUMBER_OF_BYTES))
    return x(big_l(s(x(k, two_arrays_of_bytes[0]))), two_arrays_of_bytes[1]), two_arrays_of_bytes[0]


def expand_key(key):
    """
    The algorithm of expanding keys uses iteration constants
    C i ∈ V 128 , i = 1, 2, ..., 32, which can be defined as follows:
    C i = L(Vec 128 (i)), i = 1, 2, ..., 32.
    Iterative keys K i ∈ V 128 , i = 1, 2, ..., 10, are being produced using the key
    K = k 255 ||...||k 0 ∈ V 256 , k i ∈ V 1 , i = 0, 1, ..., 255, and are defined:
    K 1 = k 255 ||...||k 128 ;
    K 2 = k 127 ||...||k 0 ;
    (K 2i + 1 , K 2i + 2 ) = F [C 8(i - 1) + 8 ]...F [C 8(i - 1) + 1 ](K 2i - 1 , K 2i ), i = 1, 2, 3, 4.
    :param key: array of bytes of size 32.
    """
    if len(key) != NUMBER_OF_BYTES * 2:
        raise ValueError('The array length is not equal to {0}.'.
                         format(NUMBER_OF_BYTES * 2))
    constants_number = 2 * NUMBER_OF_BYTES
    constants = []
    for i in range(constants_number):
        constants.append([0] * NUMBER_OF_BYTES)
        constants[i][NUMBER_OF_BYTES - 1] = i + 1
        constants[i] = big_l(constants[i])
    iterative_keys = [[0] * NUMBER_OF_BYTES] * 10
    iterative_keys[0] = key[0: NUMBER_OF_BYTES]
    iterative_keys[1] = key[NUMBER_OF_BYTES: NUMBER_OF_BYTES * 2]
    for i in range(4):
        iterative_keys[2 * (i + 1)], iterative_keys[2 * (i + 1) + 1] = \
            f(constants[8 * i], (iterative_keys[2 * i], iterative_keys[2 * i + 1]))
        for j in range(1, 8):
            iterative_keys[2 * (i + 1)], iterative_keys[2 * (i + 1) + 1] = \
                f(constants[8 * i + j], (iterative_keys[2 * (i + 1)], iterative_keys[2 * (i + 1) + 1]))
    return iterative_keys


def encrypt(iterative_keys, a):
    """
    E K 1 , ..., K 10 (a) = X[K 10 ]LSX[K 9 ]...LSX[K 2 ]LSX[K 1 ](a).
    :param iterative_keys: pair of arrays of bytes of size 16.
    :param a: array of bytes of size 16. an open text.
    """
    for i in range(9):
        a = big_l(s(x(iterative_keys[i], a)))
    return x(iterative_keys[9], a)


def decrypt(iterative_keys, b):
    """
    D K 1 , ..., K 10 (a) = X[K 1 ]S L -1 X[K 2 ]...S L -1 X[K 9 ]S L -1 X[K 10 ](a).
    :param iterative_keys: pair of arrays of bytes of size 16.
    :param b: array of bytes of size 16. an closed text.
    """
    for i in range(9, 0, -1):
        b = s_reversed(big_l_reversed(x(iterative_keys[i], b)))
    return x(iterative_keys[0], b)


def string_to_byte_array(string):
    """
    Converts a string to a byte array of size 16.
    :param string: string to convert.
    """
    if len(string) != NUMBER_OF_BYTES * 2 and len(string) != NUMBER_OF_BYTES * 4:
        raise ValueError('The array length is not equal to {0} or {1}.'.
                         format(NUMBER_OF_BYTES * 2, NUMBER_OF_BYTES * 4))
    iterator = iter(string)
    return list(((HEX_BIN_DICTIONARY[a] << 4) ^ HEX_BIN_DICTIONARY[b]) for a, b in zip(iterator, iterator))


def byte_array_to_string(byte_array):
    """
    Converts a byte array of size 16 to a string.
    :param byte_array: array to convert.
    """
    bit_to_hex_dictionary = flip_dictionary(HEX_BIN_DICTIONARY)
    return ''.join(bit_to_hex_dictionary[a >> 4] + bit_to_hex_dictionary[a & 0b00001111] for a in byte_array)


def multiply_elements(a, b):
    """
    Multiplies two elements in a GF(2 8) with the specified above generator polynomial
    :param a: the first param.
    :param b: the second param.
    """
    return divide_polynomials(multiply_polynomials(a, b), PRIMITIVE_POLYNOMIAL)[1]


def flip_dictionary(dictionary):
    """
    Flips a dictionary: key <-> value.
    :param dictionary: a dictionary where
    to flip values and keys.
    :return: a flipped dictionary.
    """
    return dict((v, k) for k, v in dictionary.items())


def divide_polynomials(polynomial1, polynomial2):
    """
    quotient:
            11101000111
           _________________
    11001 | 100100100000001
            110010000000000
            ________________
             10110100000001
             11001000000000
             _______________
              1111100000001
              1100100000000
              ______________
                11000000001
                11001000000
                ____________
                    1000001
                    1100100
                    ________
                     100101
                     110010
                     _______
                      10111
                      11001
                      ______
            reminder:  1110

    :param polynomial1: 1st polynomial.
    :param polynomial2: 2nd polynomial.
    :return: the quotient and the remainder.
    """
    quotient = 0
    reminder = polynomial1
    while len(bin(reminder)) >= len(bin(polynomial2)):
        shift = len(bin(reminder)) - len(bin(polynomial2))
        reminder ^= polynomial2 << shift
        quotient ^= 1 << shift
    return quotient, reminder


def multiply_polynomials(polynomial1, polynomial2):
    """
                                      power
    Multiplies two polynomials in GF(2     ).
    :param polynomial1: 1st polynomial.
    :param polynomial2: 2nd polynomial.
    :return: the product of two polynomials.
    """
    result = 0
    for i in range(len(bin(polynomial2)) - 2):
        if polynomial2 & (1 << i):
            result ^= polynomial1 << i
    return result
