#!/usr/bin/env python3
import copy


class Polynomial:
    # constructor
    def __init__(self, *x, x0=0, x1=0, x2=0, x3=0, x4=0, x5=0, x6=0, x7=0, x8=0, x9=0):
        self.poly = []  # list of variables of polynomial
        if x:  # if arguments supplied as list or ints
            if isinstance(x[0], list):  # if list
                self.poly = x[0]  # assign list
            else:  # if ints
                for i in x:  # append ints to list
                    self.poly.append(i)
        else:  # if keyword arguments used
            self.poly.append(x0)
            self.poly.append(x1)
            self.poly.append(x2)
            self.poly.append(x3)
            self.poly.append(x4)
            self.poly.append(x5)
            self.poly.append(x6)
            self.poly.append(x7)
            self.poly.append(x8)
            self.poly.append(x9)

        if not any(self.poly[i] for i in range(len(self.poly))):  # if all variables are 0, set list of poly to [0]
            self.poly = [0]
        else:
            # remove redundant zero value variables
            while self.poly[-1] == 0:
                self.poly.pop()

    # print method definition
    def __str__(self):
        if self.poly == [0]:  # if empty
            return "0"
        string = ""  # string to be printed
        # iteration over each variable
        for i, e in reversed(list(enumerate(self.poly))):
            # condition to remove redundant '1' in front of x
            if (e == 1) | (e == -1):  # if value is 1 or -1, set value to ''
                value = ""
            else:  # else value = abs(value)
                value = "%i" % abs(e)
            # condition to determine way of writing x when to different powers
            if i == 0:  # if to power 0
                value = "%i" % abs(e)  # value = abs(value)
            elif i == 1:  # if to power 1
                value = value + "x"  # value = 'value' + 'x'
            else:  # if to power greater than 1
                value = value + "x^%i" % i  # value = 'value' + 'x^power'

            if string == "":  # if string empty - first variable set plus as '' and minus as '-'
                plus = ""
                minus = "-"
            else:  # else if not empty set plus as ' + ' and minus as ' - '
                plus = " + "
                minus = " - "

            if e > 0:  # if value positive, append 'plus' + 'value' to string
                string += plus + value
            elif e < 0:  # if value negative, append 'minus' + 'value' to string
                string += minus + value
        return string

    # equality operator definition
    def __eq__(self, other):
        if len(self.poly) != len(other.poly):  # if not same length
            return False
        if all(False for i in range(len(self.poly)) if self.poly[i] != other.poly[i]):  # else if all variables are not unequal
            return True
        return False

    # addition operator definition
    def __add__(self, other):
        # returns addend_1[i] + addend_2[i], if index 'i' out of range value of addend[i] is 0
        return Polynomial(list(self.poly[i] + other.poly[i] if (i < min(len(self.poly), len(other.poly))) else other.poly[i] if i >= len(self.poly) else self.poly[i] for i in range(max(len(self.poly), len(other.poly)))))

    # power operator definition
    def __pow__(self, power):
        # if power is zero return 1
        if power == 0:
            return 1
        # if power is 1 return operand
        if power == 1:
            return self
        # if power is higher than 1
        res = copy.deepcopy(self.poly)  # result list
        for times in range(power-1):
            n_res = [0] * (len(res) + len(self.poly) - 1)  # new result list allocated
            # polynomial multiplication cycle
            for o1, i1 in enumerate(res):
                for o2, i2 in enumerate(self.poly):
                    n_res[o1 + o2] += i1 * i2
            res = copy.deepcopy(n_res)  # copy new result to result
        return Polynomial(res)

    # derivative method definition
    def derivative(self):
        res = copy.deepcopy(self.poly)  # result list
        for i in range(len(res)):
            res[i] *= i  # (a * x^r)' -> a*r * x^r
        res.pop(0)  # remove first item (shift left), a*r * x^r -> ar * x^r-1
        return Polynomial(res)

    # value of polynomial at value of x method definition
    def at_value(self, val1, val2=None):
        res1 = sum(self.poly[i] * val1 ** i for i in range(len(self.poly)))  # result1 = sum of all variables of operand with x substitued for value1
        if val2 is None:  # if only one value
            return res1
        # else (if two values)
        res2 = sum(self.poly[i] * val2 ** i for i in range(len(self.poly)))  # result2 = as result1 with x substituted for value2
        return res2 - res1  # difference of res2 and res1
