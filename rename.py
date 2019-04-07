import sys
with open("deck.txt", "r") as a, open("test_deck.txt", "w") as o:
    sys.stdout = o
    for lines in a:
        line = lines.strip().split()
        print(" ".join(lines[0:-1]))


sys.exit(0)

        
