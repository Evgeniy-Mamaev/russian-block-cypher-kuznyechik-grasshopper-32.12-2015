import os
import unittest
from copy import deepcopy

from blockciphers import ecb2, ecb2_reversed
from kuznyechiktransformations import expand_key, string_to_byte_array, byte_array_to_string, NUMBER_OF_BYTES

KEY = "8899aabbccddeeff0011223344556677fedcba98765432100123456789abcdef"


class BlockCiphersTest(unittest.TestCase):

    def test_ecb2(self):
        arrays = list(string_to_byte_array(string) for string in ["1122334455667700ffeeddccbbaa9988",
                                                                  "00112233445566778899aabbcceeff0a",
                                                                  "112233445566778899aabbcceeff0a00",
                                                                  "2233445566778899aabbcceeff0a0011"])
        result = ecb2(
            expand_key(string_to_byte_array(KEY)),
            arrays)
        string_result = list(byte_array_to_string(a) for a in result)
        assert string_result == ["7f679d90bebc24305a468d42b9d4edcd",
                                 "b429912c6e0032f9285452d76718d08b",
                                 "f0ca33549d247ceef3f5a5313bd4b157",
                                 "d0b09ccde830b9eb3a02c4c5aa8ada98"]

    def test_ecb2_reversed(self):
        arrays = list(string_to_byte_array(string) for string in ["7f679d90bebc24305a468d42b9d4edcd",
                                                                  "b429912c6e0032f9285452d76718d08b",
                                                                  "f0ca33549d247ceef3f5a5313bd4b157",
                                                                  "d0b09ccde830b9eb3a02c4c5aa8ada98"])
        result = ecb2_reversed(
            expand_key(string_to_byte_array(KEY)),
            arrays)
        string_result = list(byte_array_to_string(a) for a in result)
        assert string_result == ["1122334455667700ffeeddccbbaa9988",
                                 "00112233445566778899aabbcceeff0a",
                                 "112233445566778899aabbcceeff0a00",
                                 "2233445566778899aabbcceeff0a0011"]

    def test_tests(self):
        # delete a decrypted .pdf before the test
        if os.path.isfile("test_pdf/result.pdf"):
            os.remove("test_pdf/result.pdf")
        open_text = []
        key_text = [0] * NUMBER_OF_BYTES * 2
        cipher_text = []
        # what to encrypt
        with open("test_pdf/plaintext.pdf", "rb") as text:
            break_sig = 0
            while True:
                text_segment = [0] * NUMBER_OF_BYTES
                for i in range(NUMBER_OF_BYTES):
                    read = text.read(1)
                    if len(read) == 0:
                        text_segment[i] = 1
                        break_sig = 1
                        break  # end of file
                    text_segment[i] = ord(read)
                open_text.append(text_segment)
                if break_sig:
                    break  # end of file
        # the key
        with open("test_pdf/key", "rb") as key:
            for i in range(NUMBER_OF_BYTES * 2):
                key_text[i] = ord(key.read(1))
                if key_text[i] == '':
                    break  # end of file
        # what should be obtained after encryption
        with open("test_pdf/ciphertext", "rb") as cipher:
            break_sig = 0
            while True:
                to_append = 1
                text_segment = [0] * NUMBER_OF_BYTES
                for i in range(NUMBER_OF_BYTES):
                    read = cipher.read(1)
                    if len(read) == 0:
                        if i == 0:
                            to_append = 0
                        break_sig = 1
                        break  # end of file
                    text_segment[i] = ord(read)
                if to_append:
                    cipher_text.append(text_segment)
                if break_sig:
                    break  # end of file
        iterative_keys = expand_key(key_text)
        corrupted_open_text = deepcopy(open_text)
        result_of_encryption = ecb2(iterative_keys, corrupted_open_text)
        to_decrypt = deepcopy(result_of_encryption)
        result_of_decryption = ecb2_reversed(iterative_keys, to_decrypt)
        redundant_block = [0] * NUMBER_OF_BYTES
        redundant_block[0] = 1
        result_of_decryption_to_write = deepcopy(result_of_decryption)
        # write a decrypted file to check visually if it opens => the process went well
        with open("test_pdf/result.pdf", "wb") as result:
            for i in range(len(result_of_decryption_to_write) - 1):
                for piece in result_of_decryption_to_write[i]:
                    result.write(bytes([piece]))
            if result_of_decryption_to_write[len(result_of_decryption_to_write) - 1] != redundant_block:
                for j in range(len(result_of_decryption_to_write[len(result_of_decryption_to_write) - 1])):
                    if result_of_decryption_to_write[len(result_of_decryption_to_write) - 1][j] == 1:
                        result_of_decryption_to_write[len(result_of_decryption_to_write) - 1][j] = 0
                        break
                for piece in result_of_decryption_to_write[len(result_of_decryption_to_write) - 1]:
                    result.write(bytes([piece]))
        # compare encrypted and decrypted data in memory
        assert result_of_encryption == cipher_text
        assert result_of_decryption == open_text


if __name__ == '__main__':
    unittest.main()
