# extra functions that you can use

# makes sure two files have the same links
def test_equivalence(filename1, filename2):
    file_in = open(filename1, "r")
    links1 = file_in.read().split("\n")
    file_in.close()

    file_in = open(filename2, "r")
    links2 = file_in.read().split("\n")
    file_in.close()

    if len(links1) <= len(links2):
        for link in links1:
            if link not in links2:
                return False
            print(link + ": " + str(links2.index(link)))
    else:
        for link in links2:
            if link not in links1:
                return False
            print(link + ": " + str(links1.index(link)))
    return True

def sort_data(filename):
    file_in = open(filename, "r")
    links = file_in.read().split("\n")
    file_in.close()

    links.sort()

    file_in = open(filename, "w")
    for x in links:
        file_in.write(x + "\n")
    file_in.close()

sort_data("songs.dat")
sort_data("songs2.dat")
print(test_equivalence("songs2.dat", "songs.dat"))