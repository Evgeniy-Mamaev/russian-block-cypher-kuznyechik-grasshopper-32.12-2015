import unittest

from kuznyechiktransformations import s, string_to_byte_array, byte_array_to_string, s_reversed, r, multiply_elements, \
    multiply_polynomials, divide_polynomials, PRIMITIVE_POLYNOMIAL, big_l

STRING = "ffeeddccbbaa99881122334455667700"


class KuznyechikTest(unittest.TestCase):

    def test_s(self):
        assert byte_array_to_string(s(string_to_byte_array(STRING))) == "b66cd8887d38e8d77765aeea0c9a7efc"
        assert byte_array_to_string(s(string_to_byte_array("b66cd8887d38e8d77765aeea0c9a7efc"))) == \
               "559d8dd7bd06cbfe7e7b262523280d39"
        assert byte_array_to_string(s(string_to_byte_array("559d8dd7bd06cbfe7e7b262523280d39"))) == \
               "0c3322fed531e4630d80ef5c5a81c50b"
        assert byte_array_to_string(s(string_to_byte_array("0c3322fed531e4630d80ef5c5a81c50b"))) == \
               "23ae65633f842d29c5df529c13f5acda"

    def test_s_reversed(self):
        assert byte_array_to_string(s_reversed(s(string_to_byte_array(STRING)))) == STRING

    def test_r(self):
        assert byte_array_to_string(
            r(string_to_byte_array("00000000000000000000000000000100"))) == "94000000000000000000000000000001"
        assert byte_array_to_string(
            r(string_to_byte_array("94000000000000000000000000000001"))) == "a5940000000000000000000000000000"
        assert byte_array_to_string(
            r(string_to_byte_array("a5940000000000000000000000000000"))) == "64a59400000000000000000000000000"
        assert byte_array_to_string(
            r(string_to_byte_array("64a59400000000000000000000000000"))) == "0d64a594000000000000000000000000"

    def test_big_l(self):
        assert byte_array_to_string(
            big_l(string_to_byte_array("64a59400000000000000000000000000"))) == "d456584dd0e3e84cc3166e4b7fa2890d"
        assert byte_array_to_string(
            big_l(string_to_byte_array("d456584dd0e3e84cc3166e4b7fa2890d"))) == "79d26221b87b584cd42fbc4ffea5de9a"
        assert byte_array_to_string(
            big_l(string_to_byte_array("79d26221b87b584cd42fbc4ffea5de9a"))) == "0e93691a0cfc60408b7b68f66b513c13"
        assert byte_array_to_string(
            big_l(string_to_byte_array("0e93691a0cfc60408b7b68f66b513c13"))) == "e6a8094fee0aa204fd97bcb0b44b8580"

    def test_multiply_elements(self):
        print(multiply_elements(156, 231))
        print(divide_polynomials(multiply_polynomials(156, 231), PRIMITIVE_POLYNOMIAL)[1])
        assert multiply_elements(156, 231) == divide_polynomials(multiply_polynomials(156, 231), PRIMITIVE_POLYNOMIAL)[
            1]

    def test_string_to_byte_array(self):
        assert (string_to_byte_array(STRING)) == [
            0b11111111, 0b11101110, 0b11011101, 0b11001100, 0b10111011, 0b10101010, 0b10011001, 0b10001000,
            0b00010001, 0b00100010, 0b00110011, 0b01000100, 0b01010101, 0b01100110, 0b01110111, 0b00000000]

    def test_byte_array_to_string(self):
        assert byte_array_to_string(string_to_byte_array(STRING)) == STRING


if __name__ == '__main__':
    unittest.main()
