
from config import *
import algorithms

LATINS = algorithms.LATIN_LETTERS
KRILLS = algorithms.KRILL_LETTERS
POSTFIXES = ["ning", "ngiz", "ring", "dan", "siz", "cha", "dur", "lar", "lik", "man", "miz", "dir", "san", "mas", "shi", "sha", "rim", "gan", "chi", "din", "dek", "moq", "gʻa", "nga", "day", "gʻi", "yam", "may", "kim", "mok", "dim", "yot", "nim", "ta", "da", "la", "ri", "ka", "ga", "gi", "ni", "li", "si", "mi", "ma", "ki", "qa", "di", "ra", "ku", "ti", "yu", "ro", "na", "va", "ya", "sa", "yo", "i", "a", "u"]

def correctize(text:str) -> str:
    return algorithms.text_correctize(text)

def standartize(text: str) -> str:
    return algorithms.text_standartize(text)

def to_standartize(text: str) -> str:
    return algorithms.word_standartize(text, False)

def from_standartize(text: str) -> str:
    return algorithms.word_standartize(text, True)

def to_syllable(word: str) -> str:
    return algorithms.word_syllable(word)

def to_cyrillic(text:str)->str:
    return algorithms.to_cyrillic(text)

def to_latin(text:str)->str:
    return algorithms.to_latin(text)




    


