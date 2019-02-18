#!/usr/bin/env python
# -*- coding: utf-8 -*-
############################################################
# CMPSC 442: Homework 1
############################################################

student_name = "Luwei Lei"

############################################################
# Section 1: Python Concepts
############################################################

python_concepts_question_1 = """
Python is strongly typed means the compiler could keep track of the
types of all the values. The type will not suddenly changed unless
an explicit conversion is called. Python could also be dynamically
typed at the same time, which means a variable is simply a value
bound to a name，so the type of a variable could be changed later on.
"""

python_concepts_question_2 = """
There is a TypeError: "unhashable type: 'list'" while complie this line.
This is due to the list is mutable so it doesn't has a __hash__ function in source code.
The solution to this error is just simply change list type to tuple :
points_to_names = {(0, 0): "home", (1, 2): "school", (-1, 1): "market"}
"""

python_concepts_question_3 = """
The concatenate2 is better since it doesn't need to hold an empty
string in the memory, and it doesn't need to go through a loop.
"""

############################################################
# Section 2: Working with Lists
############################################################

def extract_and_apply(l, p, f):
    return [f(x) for x in l if p(x)]

def concatenate(seqs):
    return [y for x in seqs for y in x ]

def transpose(matrix):
    return [[matrix[j][i] for j in range(0, len(matrix))] for i in range(0, len(matrix[0]))]

############################################################
# Section 3: Sequence Slicing
############################################################

def copy(seq):
    return seq[:]

def all_but_last(seq):
    return seq[:-1]

def every_other(seq):
    return seq[::2]

############################################################
# Section 4: Combinatorial Algorithms
############################################################

def prefixes(seq):
    for i in range(0,len(seq)+1):
        yield seq[:i]

def suffixes(seq):
    for i in range(0,len(seq)+1):
        yield seq[i:]

def slices(seq):
    a = 1
    for i in range(len(seq)-1):
        for j in range(a, (len(seq)+1)):
            yield seq[i:j]
        a = a+1
    yield seq[-1]

############################################################
# Section 5: Text Processing
############################################################

def normalize(text):
    text =  text.lower().split()
    return (" ").join(text)

def no_vowels(text):
    vowels = ('a','e','i','o','u','A','E','I','O','U')
    for i in text:
        if i in vowels:
            text = text.replace(i, '')
    return text

def digits_to_words(text):
    words = {'1':'one', '2':'two','3':'three','4':'four','5':'five','6':'six','7':'seven','8':'eight','9':'nine', '0':'zero'}
    result = [words[i] for i in text if i in words.keys()]
    return " ".join(result)

def to_mixed_case(text):
    text = text.replace("_", " ").lower().split()
    for i in range(1, len(text)):
        text[i] = text[i].capitalize()
    return "".join(text)

############################################################
# Section 6: Polynomials
############################################################

class Polynomial(object):

    def __init__(self, polynomial):
        self.polynomial = tuple(polynomial)

    def get_polynomial(self):
        return self.polynomial

    def __neg__(self):
        newPloynomial = [(-i[0], i[1]) for i in self.polynomial]
        return Polynomial(newPloynomial)

    def __add__(self, other):
        newPloynomial = []
        newPloynomial.extend(self.polynomial)
        newPloynomial.extend(other.polynomial)
        return Polynomial(newPloynomial)

    def __sub__(self, other):
        newPloynomial = []
        newPloynomial.extend(self.polynomial)
        secPloynomial = [(-i[0], i[1]) for i in other.polynomial]
        newPloynomial.extend(secPloynomial)
        return Polynomial(newPloynomial)

    def __mul__(self, other):
        newPloynomial = []
        for i in self.polynomial:
            for j in other.polynomial:
                a = (i[0]*j[0], i[1] +j[1])
                newPloynomial.append(a)
        return Polynomial(newPloynomial)

    def __call__(self, x):
        result = 0
        for i in self.polynomial:
            result = result + i[0] * (x ** i[1])
        return result

    def simplify(self):
        dictPloynomial = {}
        for (coef, power) in self.polynomial:
            if power in dictPloynomial:
                dictPloynomial[power].append(coef)
            else:
                dictPloynomial[power] = [coef]

        dictPloynomial = {power: sum(dictPloynomial[power]) for power in sorted(dictPloynomial)}

        dictPloynomial = {power: coef for power, coef in dictPloynomial.items()if coef != 0}
        if len(dictPloynomial) == 0:
            dictPloynomial = {0:0}
        self.polynomial = tuple(reversed([(v, k) for k, v in dictPloynomial.iteritems()]))


    def __str__(self):
        result = []
        for i in self.polynomial:
            if (i[0] >= 0):
                result.append("+")
                if (i[0] == 1):
                    if (i[1] == 1):
                        result.append("x")
                    elif (i[1] == 0):
                        result.append(str(i[0]))
                    else:
                        result.append("x^"+str(i[1]))
                elif (i[1] == 0):
                    result.append(str(i[0]))
                elif (i[1] == 1):
                    result.append(str(i[0]) + "x")
                else:
                    result.append(str(i[0]) + "x^"+str(i[1]))
            elif (i[0] < 0 ):
                result.append("-")
                if (i[0] == -1):
                    if (i[1] == 1):
                        result.append("x")
                    elif (i[1] == 0):
                        result.append(str(abs(i[0])))
                    else:
                        result.append("x^"+str(abs(i[1])))
                elif (i[1] == 0):
                    result.append(str(abs(i[0])))
                elif (i[1] == 1):
                    result.append(str(abs(i[0])) + "x")
                else:
                    result.append(str(abs(i[0])) + "x^"+str(i[1]))
        if result[0] == "+":
            result = result[1:]
        if result[0] == "-":
            result[1] = result[0] + result[1]
            result = result[1:]
        return " ".join(result)

############################################################
# Section 7: Feedback
############################################################

feedback_question_1 = """
I spent almost 6 hours on this assignment
"""

feedback_question_2 = """
The last question, which is to write a Polynomials class.
I do not have much experience on working with class.
So it took some time to study the class structure.
"""

feedback_question_3 = """
I think the homework is pretty fair.
I practiced something I already know like question 3-5.
And I also learned something that are kind of new to me like question 2 and 6.
"""
