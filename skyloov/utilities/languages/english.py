import random
import string


def replace_non_english_characters(word):
    char_set = string.printable
    return ''.join([x if x in char_set else str(random.randint(0, 10)) for x in word])
