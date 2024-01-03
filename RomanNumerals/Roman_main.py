
import logging
from functools import total_ordering
from math import ceil


@total_ordering
class RomanNumerals:

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

    alph = [(1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'), (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'), (10, 'X'),
            (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')]
    words = ("I", "V", "X", "L", "C", "D", "M")
    alph_w = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    def __init__(self, val : str | int):

        if isinstance(val, int):
            self.dec_val: int = val
            self.value: str = self.to_roman(val)
            return



        if isinstance(val, str):
            self.value: str = val.upper()
            assert (self.isrome(val)), "RomanNumerals get only int and string datas with base roman letters."
            self.dec_val = self.from_roman(val)



    @classmethod
    def isrome(cls, val, cor_gram = False) -> bool:
        if isinstance(val, (RomanNumerals, str)):
            if not all(char in cls.alph_w for char in val):
                return False
            if cor_gram:
                return cls.is_valid_roman_numeral(cls, val)
            return True
        return False

    def is_valid_roman_numeral(self, s: str) -> bool:
        #GPT-3.5 realisation
        if not s:
            return False

        limit = (("V", "L", "D"), ("I", "X", "C", "M"))
        prev_value = self.alph_w[s[0]]
        total = prev_value

        for char in s[1:]:
            current_value = self.alph_w[char]

            if current_value > prev_value:
                total += current_value - 2 * prev_value  # Subtract twice the previous value
            else:
                total += current_value

            prev_value = current_value

        # Check if the calculated total matches the original Roman numeral
        if total != sum(self.alph_w[char] for char in s):
            return False

        if not s:
            return False

        prev_value = self.alph_w[s[0]]
        count_repeat = 1

        for char in s[1:]:
            current_value = self.alph_w[char]

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

    @classmethod
    def to_roman(cls, val: int | str) -> str:
        #try:
        #   val = int(val)
        #except ValueError:
        #    raise cls.Roman_Exception(val)

        if val.isdigit():
            val = int(val)
        else:
            raise cls.Roman_Exception(val)

        answer = ''
        while val > 0:
            for num, let in cls.alph:
                if val >= num:
                    val -= num
                    answer += let
                    break
        if answer == '':
            assert False, "You can't trasform double or negative numbers, only naturals."
        return answer

    @classmethod
    def from_roman(cls, roman_num: str, str_c = True) -> int | str:
        '''Перевод из Римской системы в десятичную.'''
        if not cls.isrome(roman_num):
            raise cls.Roman_Exception("Grammatic Error.")
        answer = 0
        while len(roman_num) > 0:
            for num, let in cls.alph:
                if roman_num.startswith(let):
                    roman_num = roman_num[len(let):]
                    answer += num
                    break
        return str(answer) if str_c else answer

    def __lt__(self, other):
        if isinstance(other, RomanNumerals):
            return self.dec_val < other.dec_val
        else:
            return self.dec_val < ceil(other)

    def __eq__(self, other):
        if isinstance(other, RomanNumerals):
            return self.value == other.value
        elif isinstance(other, int):
            return self.dec_val == other
        else:
            return self.value == other

    def __add__(self, other):
        '''Сложение.'''
        if isinstance(other, RomanNumerals):
            return self.to_roman(self.dec_val + other.dec_val)
        else:
            return self.to_roman(self.dec_val + other)


    def __sub__(self, other):
        '''Вычитание.'''
        if isinstance(other, RomanNumerals):
            return self.to_roman(self.dec_val - other.dec_val)
        else:
            return self.to_roman(self.dec_val - other)


    def __mul__(self, other):
        '''Умножение.'''
        if isinstance(other, RomanNumerals):
            return self.to_roman(self.dec_val * other.dec_val)
        else:
            return self.to_roman(self.dec_val * other)


    def __truediv__(self, other):
        '''Деление'''
        if isinstance(other, RomanNumerals):
            return self.to_roman(round(self.dec_val / other.dec_val))
        else:
            return self.to_roman(self.dec_val / other)

    def __pow__(self, other):
        if isinstance(other, RomanNumerals):
            return self.to_roman(self.dec_val ** other.dec_val)
        else:
            return self.to_roman(self.dec_val ** other)

    def __int__(self):
        return self.dec_val

    def __str__(self):
        return self.value
