import sys

###
#
#  Flow of Enigma:
#  Key press, goes through plugboard
#  Then to the rotors, from right to left
#  Through the reflector, back through the rotors, left to right
#  Down to a letter, back through the plugboard
#  The letter at the end of the plugboard lights up
#
###
plugboardMenu = """
Plugboard:
1: List all connections
2: Make new connection
3: Break one connection
4: Break all connections
9: Return to main menu
"""

enigmaMenu = """
Enigma:
1: Encrypt/decrypt
9: Return to main menu
"""

mainMenu = """
Welcome to the Enigma simulator
1: Enigma encryption/decryption menu
2: Plugboard
3: Rotors and reflectors
4: Other parts of the Enigma machine is not yet implemented
9: Quit the Enigma simulator
"""

rotorMenu = """
Rotors:
1: Print current selection of rotors and reflectors
2: Choose new rotors
3: Choose reflector
9: Return to main menu
"""

class Enigma:
    def __init__(self, rotor, plugboard):
        self.r = rotor
        self.p = plugboard

    def menu(self):
        while True:
            print(enigmaMenu)
            choice = input(">> ")
            if (choice == "9"):
                break
            elif (choice == "1"):
                cleartext = input("Enter cleartext or ciphertext >> ")
                print("Input: ", cleartext)
                print("Output: ", self.encrypt(cleartext.replace(" ","")))
            else:
                pass

    def encrypt(self, in_text):
        out_text=[]
        for x in range(len(in_text)):
            if x > 0 and x % 5 == 0:
                out_text.append(' ')
            c = p.write(in_text[x])
            self.r.step()
            c = self.r.write(c)
            out_text.append(p.write(c))
        return (''.join(out_text))


class Plugboard:
    def __init__(self):
        self.pairs = []
        #self.pairs = [("a","e"),("t","p")]
    def unplug_all(self):
        self.pairs = []

    def list_connections(self):
        if len(self.pairs) == 0:
            print ("No connections")
        else:
            print (self.pairs)

    def print_tuple(self, char):
        pass

    def plug(self, a, b):
        for pair in self.pairs:
            if a in pair or b in pair:
                print ("This character is already plugged in the pair", pair)
                return
        self.pairs.append((a,b))
        print ("Made new connection of (",a,",",b,")")

    def unplug(self, inp):
        for pair in self.pairs:
            if inp in pair:
                print ("Unplugged", pair)
                self.pairs.remove(pair)

    def write(self, inp):
        for pair in self.pairs:
            if inp in pair:
                i = pair.index(inp)
                return(pair[(i+1)%2])
        return(inp)

    def menu(self):
        while True:
            print(plugboardMenu)
            choice = input(">> ")
            if (choice == "9"):
                break
            elif (choice == "1"):
                self.list_connections()
            elif (choice == "2"):
                print ("What is the first letter to connect?")
                a = input(">> ")
                print ("What is the second letter to connect?")
                b = input("Connect: "+a+" - ")
                self.plug(a,b)
            elif (choice == "3"):
                print ("What letter should be unplugged?")
                inp = input(">> ")
                self.unplug(inp)
            elif (choice == "4"):
                inp = input(">> ")
                print (self.write(inp))
            else:
                pass

class RotorSelection:
    def __init__(self):
        self.rotors = {}
        self.rotors['I'] = Rotor(
            (4,10,12,5,11,6,3,16,21,25,13,19,14,22,24,7,23,20,18,15,0,8,1,17,2,9),["q"])
        self.rotors['II'] = Rotor(
            (0,9,3,10,18,8,17,20,23,1,11,7,22,19,12,2,16,6,25,13,15,24,5,21,14,4),["e"])
        self.rotors['III'] = Rotor(
            (1,3,5,7,9,11,2,15,17,19,23,21,25,13,24,4,8,22,6,0,10,12,20,18,16,14),["v"])
        self.rotors['IV'] = Rotor(
            (4,18,14,21,15,25,9,0,24,16,20,8,17,7,23,11,13,5,19,6,10,3,2,12,22,1),["j"])
        self.rotors['V'] = Rotor(
            (21,25,1,17,6,8,19,24,20,15,18,3,13,7,11,23,0,22,12,9,16,14,5,4,2,10),["z"])
        self.rotors['VI'] = Rotor(
            (9,15,6,21,14,20,12,5,24,16,1,4,13,7,25,17,3,10,0,18,23,11,8,2,19,22),["z","m"])
        self.rotors['VII'] = Rotor(
            (13,25,9,7,6,17,2,23,12,24,18,22,1,14,20,5,0,8,21,11,15,4,10,16,3,19),["z","m"])
        self.rotors['VIII'] = Rotor(
            (5,10,16,7,19,11,23,14,2,1,9,18,15,3,25,17,0,12,4,22,13,8,20,24,6,21),["z","m"])
        self.reflector_B = Reflector("yruhqsldpxngokmiebfzcwvjat")

        self.selection = []
        self.selection.append(self.reflector_B)
        self.selection.append(self.rotors['I'])
        self.selection.append(self.rotors['II'])
        self.selection.append(self.rotors['III'])

    def getRotors(self):
        for x in len(self.selection):
            if x == len(self.selection):
                break
            self.selection[x].next = self.selection[x+1]

        return self.selection[-1]

    def printRotors(self):
        for name in self.rotors:

            print(name)

    def menu(self):
        while True:
            print(rotorMenu)
            choice = input(">> ")
            if (choice == "9"):
                break
            elif (choice == "1"):
                self.printRotors()
            elif (choice == "2"):
                pass
            elif (choice == "3"):
                pass
            else:
                continue

class Rotor:
    def __init__(self, wiring, turnover_notch):
        self.io = ("a","b","c","d","e","f","g","h","i","j","k","l","m","n",
                "o","p","q","r","s","t","u","v","w","x","y","z")
        self.left = wiring
        self.right = (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25)
        self.offset = 0
        self.turnover_notch = turnover_notch
        self.position = 0

    def sub_in(self, c):
        turn_next = False
        c = self.io[(self.left[self.io.index(c)]-self.position)%26]
        return (c)

    def sub_out(self, c):
        c = self.io[self.right[self.left.index((self.io.index(c)+self.position)%26)]]
        return c

    def step(self):
        if self.io[self.position] in self.turnover_notch:
            self.next.step()
        self.position = (self.position+1)%26
        self.left = self.left[1:]+self.left[0:1]

    def write(self, inp):
        A = self.sub_in(inp)
        A = self.next.write(A)
        return self.sub_out(A)

class Reflector:
    def __init__(self, substitution):
        self.alphabet = ("a","b","c","d","e","f","g","h","i","j","k","l","m","n",
                "o","p","q","r","s","t","u","v","w","x","y","z")
        self.substitution = tuple(substitution)

    def reflect(self, inp):
        return (self.substitution[alphabet.index(inp)])

    def write(self, inp):
        return (self.substitution[alphabet.index(inp)])

def create_rotors():
    pass

if __name__ == "__main__":
    p = Plugboard()
    r = RotorSelection()

    alphabet = ("a","b","c","d","e","f","g","h","i","j","k","l","m","n",
            "o","p","q","r","s","t","u","v","w","x","y","z")

    while True:
        print(mainMenu)
        choice = input(">> ")
        if (choice == "9"):
            exit()
        elif (choice.lower() == "h"):
            continue
        elif (choice == "1"):
            e = Enigma(r.getRotors(), p)
            e.menu()
        elif (choice == "2"):
            p.menu()
        elif (choice == "3"):
            r.menu()
        elif (choice == "t"):
            for x in range(30):
                A = "a"
                r_III.step()
                print (x+1, r_III.write("a"))
        else:
            continue
