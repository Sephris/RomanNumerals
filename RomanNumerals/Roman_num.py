from RomanNumerals.Roman_main import RomanNumerals

class Roman_Exception(Exception):
        def __init__(self, *args):
            if args:
                self.message = args[0]
            else:
                self.message = None

        def __str__(self):
            if self.message:
                return "Roman_TransformationError, The '{0}' has wrong format. ".format(self.message)
            else:
                return 'Roman_TransformationError'
"""Римские числа в пределах. Эффективные вычисления в пределах до 4000. Поддержка более больших значений не ведётся."""



class Structurs:
    alph = [(1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'), (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'), (10, 'X'),
            (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')]
    words = ("I", "V", "X", "L", "C", "D", "M")
    alph_w = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}



def isrome(val, cor_gram = False) -> bool:
    if isinstance(val, (RomanNumerals, str)):
        if not all(char in Structurs.alph_w for char in val):
            return False
        if cor_gram:
            return is_valid_roman_numeral(val)
        return True
    return False

def is_valid_roman_numeral(s: str) -> bool:
    #GPT-3.5 realisation
    if not s:
        return False

    limit = (("V", "L", "D"), ("I", "X", "C", "M"))
    prev_value = Structurs.alph_w[s[0]]
    total = prev_value

    for char in s[1:]:
        current_value = Structurs.alph_w[char]

        if current_value > prev_value:
            total += current_value - 2 * prev_value  # Subtract twice the previous value
        else:
            total += current_value

        prev_value = current_value

    # Check if the calculated total matches the original Roman numeral
    if total != sum(Structurs.alph_w[char] for char in s):
        return False

    if not s:
        return False

    prev_value = Structurs.alph_w[s[0]]
    count_repeat = 1

    for char in s[1:]:
        current_value = Structurs.alph_w[char]

        if current_value == prev_value:
            count_repeat += 1
            if count_repeat > 3 or char in ['V', 'L', 'D']:
                return False
        else:
            count_repeat = 1

        if current_value > prev_value:
            if count_repeat > 1 or char in ['V', 'L', 'D']:
                return False
            if char in ['I', 'X', 'C'] and current_value > 10 * prev_value:
                return False  # Недопустимо вычитать числа более чем в 10 раз больше предыдущего
        else:
            if prev_value > 10 * current_value:
                return False  # Недопустимо вычитать числа более чем в 10 раз больше следующего

        prev_value = current_value

    return True

def to_roman(val: int | str) -> str:
    #try:
    #   val = int(val)
    #except ValueError:
    #    raise Structurs.Roman_Exception(val)

    if val.isdigit():
        val = int(val)
    else:
        raise Roman_Exception(val)

    answer = ''
    while val > 0:
        for num, let in Structurs.alph:
            if val >= num:
                val -= num
                answer += let
                break
    if answer == '':
        raise RomanNumerals.Roman_Exception(val, "You can't trasform double or negative numbers, only naturals.")
    return answer

def from_roman(roman_num: str, str_c = True) -> int | str:
    '''Перевод из Римской системы в десятичную.'''
    if not isrome(roman_num):
        raise Roman_Exception("Grammatic Error.")
    answer = 0
    while len(roman_num) > 0:
        for num, let in Structurs.alph:
            if roman_num.startswith(let):
                roman_num = roman_num[len(let):]
                answer += num
                break
    return str(answer) if str_c else answer
