from enum import Enum

W = Enum('W',"ES IST FÜNF_A ZEHN_A ZWANZIG DREI_A VIERTEL VOR NACH HALB \
ELF FÜNF_B EIN EINS ZWEI DREI_B VIER SECHS ACHT SIEBEN ZWÖLF ZEHN_B NEUN UHR".split(" "))

# Extra Worte, zusätzlich zur Uhrzeit
XW = Enum("XW","B BE SO DOM HEL RA F")

TagKat = Enum("TagKat", "Normal Feiertag FamGeburtstag BekGeburtstag")
