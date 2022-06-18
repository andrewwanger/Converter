import binascii
import sys
import os.path
import socket

#read file and convert binary to hex
def main(filename):
    if sys.argv[1] == "--h":
        print("Help: input formats should be as follows: python3 converter.py [name of .bin wanted to be translated] [0 (little endian) / 1 (big endian)]")
        quit()
    if len(sys.argv) < 3:
        print("Please fill in missing parameters. Help can be found with the command: 'python3 converter.py --h'")
        quit()
    with open(filename, 'rb') as f:
       # Slurp the whole file and efficiently convert it to hex all at once
        hexdata = binascii.hexlify(f.read())
    stringhex = hexdata.decode('UTF-8')
    if sys.argv[2] == "0" or sys.argv[2] == "1":
        finalwrite = format(stringhex, sys.argv[2])
        if os.path.exists(filename[:-4] + ".txt"):
            overwrite = open(filename[:-4] + ".txt", "w")
            overwrite.write(finalwrite)
        else:
            newf = open(filename[:-4] + ".txt", "x")
            newf.write(finalwrite)
    else:
        print("Command not valid")

def format(hexstring, endian):
    address = 0
    initsize = len(hexstring)
    towrite = ""
    while address < initsize//2:
        curr = hexstring[:8]
        databyte =  "0x" + curr
        if endian == "0":
            intcurr = int(curr, base = 16)
            lilend = socket.ntohl(intcurr)
            curr = hex(lilend)
            databyte = padhexa(curr)
        hexstring = hexstring[8:]
        hexadd = padhexa(hex(address))
        address += 4
        towrite += hexadd + "\t" + databyte + "\n"
    return towrite

def padhexa(s):
    return '0x' + s[2:].zfill(8)

main(sys.argv[1])
