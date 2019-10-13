from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os

filename = "encrypted.bin"
default_pathname = "/.playlist-creator"
if not os.path.exists(default_pathname):
    print("Error: key not created yet. Please use key_gen.py first")
    quit(1)
key_location = default_pathname + "/key.bin" 

# read custom username and password from pc

print("We will now ask for your discord username and password. ")
print("We will never share it with anybody. It is only used to sign in with selenium. ")
print("If you are uncomfortable with this, we recommend making a dummy discord account")
username = input("Enter username: ")
password = input("Enter password: ")
data = username + "\n" + password
data = data.encode()

# open key file
file_in = open(key_location, "rb")
key = file_in.read()
file_in.close()

# creater cipher object and encrypt data
cipher = AES.new(key, AES.MODE_CBC)
ciphered_data = cipher.encrypt(pad(data, AES.block_size))

# save to new file
file_out = open(filename, 'wb')
file_out.write(cipher.iv)
file_out.write(ciphered_data)
file_out.close()

print("encryption successful!")