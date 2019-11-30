NUMBER_OF_ELEMENTS = 255
PRIMITIVE_POLYNOMIAL = int("111000011", 2)
POWER = 7
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


def x(k, a):
    if len(k) != NUMBER_OF_BYTES or len(a) != NUMBER_OF_BYTES:
        raise ValueError('The array length is not equal to {0}.'.
                         format(NUMBER_OF_BYTES))
    return list(b ^ c for b, c in (k, a))


def l(array_of_bytes):
    if len(array_of_bytes) != NUMBER_OF_BYTES:
        raise ValueError('The array length is not equal to {0}.'.
                         format(NUMBER_OF_BYTES))
    result = 0
    for i in range(NUMBER_OF_BYTES):
        result ^= multiply_elements(array_of_bytes[i], LINEAR_TRANSFORMATION_CONSTANTS[i])
    return result


def s(array_of_bytes):
    if len(array_of_bytes) != NUMBER_OF_BYTES:
        raise ValueError('The array length is not equal to {0}.'.
                         format(NUMBER_OF_BYTES))
    return list(NONLINEAR_SUBSTITUTION[e] for e in array_of_bytes)


def s_reversed(array_of_bytes):
    if len(array_of_bytes) != NUMBER_OF_BYTES:
        raise ValueError('The array length is not equal to {0}.'.
                         format(NUMBER_OF_BYTES))
    flipped_nonlinear_substitution = dict((v, i) for i, v in enumerate(NONLINEAR_SUBSTITUTION))
    return list(flipped_nonlinear_substitution[e] for e in array_of_bytes)


def r(array_of_bytes):
    if len(array_of_bytes) != NUMBER_OF_BYTES:
        raise ValueError('The array length is not equal to {0}.'.
                         format(NUMBER_OF_BYTES))
    temp = l(array_of_bytes)
    for i in range(NUMBER_OF_BYTES - 2, -1, -1):
        array_of_bytes[i + 1] = array_of_bytes[i]
    array_of_bytes[0] = temp
    return array_of_bytes


def r_reversed(array_of_bytes):
    if len(array_of_bytes) != NUMBER_OF_BYTES:
        raise ValueError('The array length is not equal to {0}.'.
                         format(NUMBER_OF_BYTES))
    temp = array_of_bytes[0]
    for i in range(NUMBER_OF_BYTES - 2):
        array_of_bytes[i] = array_of_bytes[i + 1]
    array_of_bytes[NUMBER_OF_BYTES - 1] = temp
    array_of_bytes[NUMBER_OF_BYTES - 1] = l(array_of_bytes)
    return array_of_bytes


def big_l(array_of_bytes):
    if len(array_of_bytes) != NUMBER_OF_BYTES:
        raise ValueError('The array length is not equal to {0}.'.
                         format(NUMBER_OF_BYTES))
    for _ in range(NUMBER_OF_BYTES):
        array_of_bytes = r(array_of_bytes)
    return array_of_bytes


def big_l_reversed(array_of_bytes):
    if len(array_of_bytes) != NUMBER_OF_BYTES:
        raise ValueError('The array length is not equal to {0}.'.
                         format(NUMBER_OF_BYTES))
    for _ in range(NUMBER_OF_BYTES):
        array_of_bytes = r_reversed(array_of_bytes)
    return array_of_bytes


def f(k, two_arrays_of_bytes):
    number_of_arrays = 2
    if len(two_arrays_of_bytes) != number_of_arrays:
        raise ValueError('The number of arrays is not equal to {0}.'.
                         format(number_of_arrays))
    if len(two_arrays_of_bytes[0]) != NUMBER_OF_BYTES or len(two_arrays_of_bytes[1]) != NUMBER_OF_BYTES:
        raise ValueError('The array length is not equal to {0}.'.
                         format(NUMBER_OF_BYTES))
    return [x(big_l(s(x(k, two_arrays_of_bytes[0]))), two_arrays_of_bytes[1]), two_arrays_of_bytes[0]]


def expand_key(key):
    constants_number = 2 * NUMBER_OF_BYTES
    constants = [[0] * NUMBER_OF_BYTES] * constants_number
    for i in range(constants_number):
        constants[i][NUMBER_OF_BYTES - 1] = i + 1


def string_to_byte_array(string):
    if len(string) != NUMBER_OF_BYTES * 2:
        raise ValueError('The array length is not equal to {0}.'.
                         format(NUMBER_OF_BYTES * 2))
    iterator = iter(string)
    return list(((HEX_BIN_DICTIONARY[a] << 4) ^ HEX_BIN_DICTIONARY[b]) for a, b in zip(iterator, iterator))


def byte_array_to_string(byte_array):
    bit_to_hex_dictionary = flip_dictionary(HEX_BIN_DICTIONARY)
    return ''.join(bit_to_hex_dictionary[a >> 4] + bit_to_hex_dictionary[a & 0b00001111] for a in byte_array)


def multiply_elements(a, b):
    return divide_polynomials(multiply_polynomials(a, b), PRIMITIVE_POLYNOMIAL)[1]


def sum_elements(a, b):
    return (a + b) % NUMBER_OF_ELEMENTS


def build_logarithmic_table(power, primitive_polynomial):
    """
    Builds a logarithmic table where a
    logarithm is mapped to the binary
    representation of the corresponding
    polynomial.
    The field is generated by the
    :param primitive_polynomial.
    :param power: the power in size of the
              power
    field GF(2     ).
    :return: the logarithmic table of
    the field.
    """
    if len(bin(primitive_polynomial)) - 3 != power:
        raise ValueError('The primitive polynomial {0:b} '
                         'is not of the specified power n = {1}'.
                         format(primitive_polynomial, power))
    logarithmic_table = {-1: 0}
    for i in range(power):
        logarithmic_table[i] = 1 << i
    logarithmic_table[power] = trim_polynomial(polynomial=primitive_polynomial, length=power)
    for i in range(power + 1, 2 ** power - 1):
        multiplied_by_x_polynomial = logarithmic_table[i - 1] << 1
        if multiplied_by_x_polynomial & (2 ** power):
            multiplied_by_x_polynomial ^= logarithmic_table[power]
        logarithmic_table[i] = trim_polynomial(polynomial=multiplied_by_x_polynomial, length=power)
    return logarithmic_table


def trim_polynomial(polynomial, length):
    """
    Cuts off extra bits form the
    polynomial.
    :param polynomial: a polynomial
    to trim.
    :param length: length of the
    target polynomial.
    :return: a cut-off polynomial.
    """
    return polynomial & ((2 ** length) - 1)


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
