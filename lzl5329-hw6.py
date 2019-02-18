############################################################
# CMPSC 442: Homework 6
############################################################

student_name = "Luwei Lei"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import string
import random
import math

############################################################
# Section 1: Markov Models
############################################################

def tokenize(text):
    for i in text:
        if i in string.punctuation:
            text = text.replace(i, " "+i+" ")
    return text.split()

def ngrams(n, tokens):
    tokens =  ['<START>']*(n-1)+tokens+['<END>']
    list = []
    for i in range(n-1, len(tokens)):
        a = (tuple(tokens[i-n+1:i]), tokens[i])
        list.append(a)
    return list

class NgramModel(object):
    def __init__(self, n):
        self.n = n
        self.context_dic ={}
        self.context_token = {}

    def update(self, sentence):
        for i in ngrams(self.n, tokenize(sentence)):
            if self.context_dic.has_key(i[0]):
                self.context_dic[i[0]] +=1
            else:
                self.context_dic[i[0]] = 1

            if self.context_token.has_key(i):
                self.context_token[i] +=1
            else:
                self.context_token[i] = 1

        #return self.context_dic, self.context_token

    def prob(self, context, token):
        input = (context, token)
        try:
            return float(self.context_token[input]) / float(self.context_dic[context])
        except(KeyError):
            return 0.0

    def random_token(self, context):
        r = random.random()

        ngram_token = self.context_token.keys()
        T = []
        for i, j in ngram_token:
             if i == context:
                 T.append(j)
        T = sorted(sorted(T), key=str.upper)

        sum1 = 0
        sum2 = 0
        for token in T:
            sum2 += self.prob(context, token)
            if sum1 <= r < sum2:
                return token
            sum1 = sum2

    def random_text(self, token_count):
        if self.n == 1:
            result = [self.random_token(()) for i in range(token_count)]
            return " ".join(result)
        else:
            initial = ("<START>",) * (self.n -1)
            context = initial
            list =[]
            for i in range(token_count):
                token = self.random_token(context)
                if token == "<END>":
                    context = initial
                else:
                    context = context[1:] + (token,)
                list.append(token)
            return " ".join(list)

    def perplexity(self, sentence):
        prob = 0
        for i, j in ngrams(self.n, tokenize(sentence)):
            prob += math.log(float(1)/self.prob(i, j))
        return (math.exp(prob)) ** (float(1)/(len(tokenize(sentence))+1))

def create_ngram_model(n, path):
    model = NgramModel(n)
    with open(path) as f:
        content = f.read().splitlines()
    for i in content:
        model.update(i)
    return model


random.seed(1)
m = create_ngram_model(1, "frankenstein.txt")
print m.random_text(15)
m = create_ngram_model(2, "frankenstein.txt")
print m.random_text(15)
m = create_ngram_model(3, "frankenstein.txt")
print m.random_text(15)
m = create_ngram_model(4, "frankenstein.txt")
print m.random_text(15)


m = NgramModel(1)
m.update("a b c d")
m.update("a b a b")
random.seed(1)
print [m.random_token(()) for i in range(25)]
print m.random_text(15)
print m.perplexity("a b")

############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
I spent 4 hours on this assignment.
"""

feedback_question_2 = """
The stats and math part is a little bit challenging.
"""

feedback_question_3 = """
I hope we would have more example testing cases.
"""
