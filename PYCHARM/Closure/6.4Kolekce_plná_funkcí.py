import random

def to_uppercase(stri):
    return stri.upper()

def to_lowercase(stri):
    return stri.lower()

def smile(stri):
    stri = stri.replace(' ', '😊')
    return stri

def vToW(stri):
    stri = stri.replace('V', 'W')
    return stri

def append_star(stri):
    return '*' + stri + ' *'

def expand_punct(stri):
    stri = stri.replace('!', '!!!!!')
    stri = stri.replace('?', '???')
    return stri

funky_functions = [to_uppercase, smile, vToW, append_star, expand_punct]
used_functions = []
def funky_format(text):
    for x in range(3):
        random_function = random.choice(funky_functions)
        text = random_function(text)
        used_functions.append(random_function.__name__)
    print(used_functions)
    return text








if __name__ == '__main__':

    print(funky_format("Ahoj Karle! Pudeme dnes do kina?"))

