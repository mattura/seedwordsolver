# Seed Word Solver v1.0 
Attempts to discover the correct seed word when given a series of 12 - 24 words.
One word given may be invalid or missing. All possible candidates will be shown.

This code runs offline (*see requirements first)

NOTE: There is an extensively updated version of this script, with HEAPS of new features, faster, better, etc. 
The updated version is available on request only (raise an issue to get my attention!)

# Use this code:
* If you have 11 out of 12, or 23 out of 24 seed words and need to find the missing one
* AND you do not have the patience to type 24 words, up to 2048 times into your hardware wallet
* AND you have reviewed this code and trust it (no liability licence)

# Requirements:
* The 'mnemonic' library from Trezor (https://github.com/trezor/python-mnemonic):

    ```
    pip install mnemonic
    ```
* A BIP39 seed word list downloaded from: 
https://github.com/bitcoin/bips/blob/master/bip-0039/bip-0039-wordlists.md
(if this is not "english.txt", edit the line ```bipfile="*****"``` to reflect the filename)

# Run:
1) Load seed words from text file (separated by any whitespace):
```
python seedwordsolver.py seedwords.txt
```
2) Type or paste seed words directly into the program (keep the words in RAM and stdout):
```
python seedwordsolver.py
```

The resulting sets of valid possible seed words are displayed in the console

# Features:
* Checks BIP39 wordlist matches bitcoin BIP39 MD5 hashes 
* Takes input from file or within the program
* Highlights words not in BIP wordlist
* Provides seed and HD master key for results
* Might just get you back your lost BTC!
* Pretty console colours!

# Suggestions? Donations?
Raise an issue!
