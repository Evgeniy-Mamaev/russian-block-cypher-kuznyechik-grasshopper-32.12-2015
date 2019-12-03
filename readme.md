There are twelve folders in the test folder. Each test_0..9 folder
represents the test of the Kuznyechik cipher. The test_pdf folder
stands for the test of the block cipher mode ecb (electronic code book).

The former tests assert the computation is correct by comparing 
an encrypted block of length 128 bit (16 bytes) with the model cipher text
in memory. The decrypted block is compared with the original plain text
in memory as well.

The later test compares an encrypted plaintext.pdf file (in Russian) with
the model cipher text in memory. The implementation generates 
from an encrypted text the decrypted result.pdf file for providing one
an opportunity to check the result visually. The result.pdf file opens =>
the process went fine. 
