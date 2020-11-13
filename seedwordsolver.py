'''
=== Seed Word Solver v1.0 === https://github.com/mattura/seedwordsolver/ ===
Attempts to discover the correct seed word when given a series of 12 - 24 words.
One word given may be invalid or missing. All possible candidates will be shown.

This code runs offline.

The 'mnemonic' library is from Trezor (https://github.com/trezor/python-mnemonic)
Functions from this code are used to:
 1) convert the seed words to the seed (hex),
 2) check the seed is valid (checksum),
 3) convert the seed to the hierarchical deterministic (HD) master private key (xprv...)
 4) generate random seed words (if specified below)
*********************************************************************************
* To run this code you must first install the mnemonic library by executing:    *
*     pip install mnemonic                                                      *
*                                                                               *
* Ensure you have a BIP39 seed word list downloaded from:                       *
* https://github.com/bitcoin/bips/blob/master/bip-0039/bip-0039-wordlists.md    *
* And specify the file name below in 'bipfile'  (eg "english.txt")              *
*                                                                               *
* Then run:                                                                     *
*     python seedwordsolver.py [seedwords.txt]                                  *
*********************************************************************************
'''
from mnemonic import Mnemonic
import sys, re, random, time, hashlib
# Seed word list (as specified in BIP39), eg. download the english seed word list here:
# https://raw.githubusercontent.com/bitcoin/bips/master/bip-0039/english.txt
bipfile="english.txt"

#Create mnemonic object (use the same language as the above word list):
m = Mnemonic("english")  #TODO: for other languages, import unicodedata and use .normalize()

#   Set the following value to True to generate random valid seed words,
#   instead of loading seed words from a file or user input
generate_random_seedwords = False   #Set to True to generate valid seed words
checkMD5 = True     #Verify MD5 matches official BIP source of wordlist
wps = 0    #Number of words per second to test! Set to 0 for fastest possible results. Or try 100!

#Pretty terminal colours:
tRED = '\033[91m'
tGRN = '\033[92m'
tYLW = '\033[93m'
tNRM = '\033[0m'

#Load BIP39 word list and check hash:
validmd5s = ["0c5517ab8edb22ea7a61e44b28e96da7","00d0909e346b52006d1e9ef680b5a5fc",
"38fd5e100d4604c2a844bb9bb9305975","f23506956964fa69c98fa3fb5c8823b5", #English
"f5905fd22fd0deb0be40f356204ba3fb","fbe635509a2859b7b6de2c0f16f15ed8",
"c71fca9fd3fe9f85514cb38a58859de2","ec271d4926b82ef5c02aefa7dd2daaf4",
"5171ee312f7709bec7660bc9ac07351a"]
md5 = hashlib.md5()
try:
    with open(bipfile, 'rb') as f:
        while True:
            data = f.read(65536)
            if not data:
                break
            md5.update(data)
    if md5.hexdigest() not in validmd5s and checkMD5:
        exit("{r}WARNING: '{f}' MD5 hash does not match official BIP39 word list!{0}\n\
        Download the correct list from:\n\t{y}https://github.com/bitcoin/bips/tree/master/bip-0039{0}\n\
        Or to ignore this warning, change {y}checkMD5{0} to {y}False{0}".format(tNRM,r=tRED,y=tYLW,f=bipfile))
except IOError as e:
    exit("{r}Error{0}: BIP39 wordlist '{f}' not found. Please locate or download from:\n\t\
    {y}https://github.com/bitcoin/bips/tree/master/bip-0039{0}".format(tNRM,y=tYLW,r=tRED,f=bipfile))

#Read the words:
with open(bipfile) as f:
    ctx = f.readlines()
biplist = [x.strip() for x in ctx]
r_samp = random.randint(10,len(biplist)-10)
print("BIP List loaded {} words. Sample: [...{}...]".format(len(biplist),", ".join(biplist[r_samp:r_samp+8])))

if generate_random_seedwords:
    w = m.generate(strength=256) #Generate random words, 24 length:
    words = w.split(" ")
    print("{}Random words generated:{}".format(tYLW,tNRM))
else:
    if len(sys.argv)>1:     #If filename is specified, try to load seed words:
        seedfile = sys.argv[1]
        with open(seedfile) as f:
            input_words = f.read().strip()
    else:                   #Otherwise, take words from console input:
        print("To load seed words from file, use:\n\t{}python {} seedwords.txt{}\nOtherwise, type/paste the words here ({}Ctrl+D{} to finish):".format(tGRN,sys.argv[0],tNRM,tYLW,tNRM))
        u_input=sys.stdin.readlines()
        input_words = " ".join(u_input).strip()
        if input_words=="":
            exit()
    words = re.split('\s+', input_words)    #Split the words by any whitespace
    if len(words)<12:
        exit("{}Word list too small!{} Please try at least 12 words".format(tRED,tNRM))
    w = " ".join(words)
    print("Seed words loaded:".format(tGRN,tNRM))

#Keep track of invalid words (not in BIP39 list):
invalids = []
while len(words)//3 != len(words)/3:
    words = words + ["-"]
for i,wd in enumerate(words):
    if wd not in biplist:
        print("{}{:>3}) {}{}".format(tYLW,i+1,wd,tNRM))
        invalids = invalids + [i]
    else:
        print("{:>3}) {}".format(i+1,wd))

#Check the seed phrase:
if m.check(w):
    print("{}Valid Seed Words (checksum pass){}".format(tGRN,tNRM))
    seed = m.to_seed(w)
    print("Seed: {}".format(seed.hex()))
    print("Master Key (null password): {}".format(m.to_hd_master_key(seed)))
else:
    print("{}Invalid Seed Words (checksum fail){}".format(tRED,tNRM))

#Currently, this script can only find one unknown word:
if len(invalids)>1:
    exit("Too many unknowns! Please ensure only 1 seed word is missing or invalid.")

#Get user input for which word to switch out:
try:
    if len(invalids)>0:
        inp = input("Word number to test (default={}):".format(invalids[0]+1))
        index = int(inp)-1
    else:
        inp = input("Word number to test:")
        index=int(inp)-1
    if index<0 or index>len(words):
        exit("Index must be between 1 and {}, quitting.".format(len(words)))
except Exception as e:
    if inp=="" and len(invalids)>0:
        index=invalids[0]
    else:
        exit("Invalid/null input, quitting.".format(e))

#User chose a word other than the existing invalid one
if (len(invalids)==1 and invalids[0]!=index):
    exit("Too many unknowns! Please ensure only 1 seed word is missing or invalid.")

#Perform the replacement and show the results:
print("Replacing '{}{}{}'...".format(tYLW,words[index],tNRM))
count= 0
for candidate in biplist:
    words[index] = candidate
    w=" ".join(words)
    if m.check(w):
        count = count + 1
        seed = m.to_seed(w, passphrase="")
        print("Valid BIP39 Words:   \n{}{:>3}{})  {}".format(tYLW,count,tNRM,w.replace(candidate,"{}{}{}".format(tGRN,candidate,tNRM))))
        print("Seed: {}".format(seed.hex()))
#        print("Entropy: {}".format(m.to_entropy(w).hex()))
        print("HD Master Key: {}".format(m.to_hd_master_key(seed)))
        if wps>0:
            time.sleep(5/wps)
    else:
        print(" '{}' invalid      ".format(candidate), end="\r")
        if wps>0:
            time.sleep(1/wps)
