import os
import os.path

from Crypto.Random import get_random_bytes
default_pathname =  r"/.playlist-creator"
pathname = input('Please enter a pathname to save to (default: %s): ' % default_pathname)
if not pathname: pathname = default_pathname
if not os.path.exists(pathname):
    print("Creating folder at path: " + pathname)
    try:
        os.mkdir(pathname)
        print("Successfully created directory at path: " + pathname)
    except OSError:
        print("Failed to create directory at: " + pathname)
        quit(1)

key_location = pathname + "/key.bin"
# generate random key
key = get_random_bytes(32)

# save key to file
if os.path.isfile(key_location):
    quit_option = input("Key already exists. Overwrite? (y/n): ")
    if quit_option[0] == "n":
        print("Aborting creation...")
        quit()
file_out = open(key_location, 'wb')
file_out.write(key)
file_out.close()
print("Successfully created key at: " + key_location)
