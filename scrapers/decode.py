# decode.py is in here and not in ../crypto because I'm lazy
# if you fix this please put a pull request

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import os.path

# prefix if user is in the scrapers directory running the python script
prefix = ""
if not os.path.exists("crypto"):
    if os.path.exists("../crypto"):
        prefix = "../"
    else:
        print("Error: please run the python script while inside your playlist-creator folder")
        quit(1)
filename = prefix + "crypto/encrypted.bin"
key_location = input("decode.py: Enter the key location (press enter for default: /.playlist-creator/key.bin): ")
if not key_location: key_location = r"/.playlist-creator/key.bin"

# open key file
file_in = open(key_location, "rb")
key = file_in.read()
file_in.close()

# read the data from the file
file_in = open(filename, "rb")
iv = file_in.read(16)
ciphered_data = file_in.read()
file_in.close()

cipher = AES.new(key, AES.MODE_CBC, iv=iv)
data = unpad(cipher.decrypt(ciphered_data), AES.block_size)
data = str(data, "utf-8").split('\n')

print("decryption successful!")