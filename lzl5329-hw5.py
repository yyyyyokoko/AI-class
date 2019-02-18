############################################################
# CMPSC442: Homework 5
############################################################

student_name = "Luwei Lei"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import email
import math
import os
import time
############################################################
# Section 1: Spam Filter
############################################################

def load_tokens(email_path):
    fp = open(email_path)
    message = email.message_from_file(fp)
    fp.close()
    list = []
    for i in email.iterators.body_line_iterator(message):
        list.extend(i.split())
    return list

def log_probs(email_paths, smoothing):
    count_all = 0
    words = {}

    for path in email_paths:
        for i in load_tokens(path):
            count_all += 1
            if words.has_key(i):
                words[i] +=1
            else:
                words[i] = 1
    mydict = {}
    a = count_all + smoothing*(len(words.keys())+1)

    for i in words.keys():
        mydict[i] = math.log((words[i] + smoothing) / a)

    mydict["<UNK>"] = math.log(smoothing / a)

    return mydict

class SpamFilter(object):

    def __init__(self, spam_dir, ham_dir, smoothing):
        #merge_list = []
        spam_list = [spam_dir+"/"+i for i in os.listdir(spam_dir)]
        ham_list = [ham_dir+"/"+i for i in os.listdir(ham_dir)]
        #merge_list.extend(spam_list)
        #merge_list.extend(ham_list)

        self.spam_dictionary = log_probs(spam_list,smoothing)
        self.ham_dictionary = log_probs(ham_list,smoothing)
        #self.merge_dictionary = log_probs(merge_list, smoothing)

        self.p_spam = float(len(spam_list)) /float(len(spam_list)+len(ham_list))
        self.p_not_spam = 1 - self.p_spam


    def is_spam(self, email_path):
        spam = 1
        ham = 1
        words = {}

        for i in load_tokens(email_path):
            if words.has_key(i):
                words[i] +=1
            else:
                words[i] = 1

        for i in words.keys():
            if i in self.spam_dictionary:
                spam += self.spam_dictionary[i]*words[i]
            else:
                spam += self.spam_dictionary["<UNK>"]*words[i]

            if i in self.ham_dictionary:
                ham += self.ham_dictionary[i]*words[i]
            else:
                ham += self.ham_dictionary["<UNK>"]*words[i]

        return (math.log(self.p_spam) + spam) > (math.log(self.p_not_spam) + ham)


    def most_indicative_spam(self, n):
        dict = {}
        for i in self.spam_dictionary.keys():
            if i in self.ham_dictionary:
                spam = float(pow(math.e, self.spam_dictionary[i]) * self.p_spam)
                ham = float(pow(math.e, self.ham_dictionary[i]) * self.p_not_spam)
                dict[i] = self.ham_dictionary[i] - float(math.log(spam+ham))

        y = sorted(dict.keys(), key=dict.get)
        return y[:n]

    def most_indicative_ham(self, n):
        dict = {}
        for i in self.ham_dictionary.keys():
            if i in self.spam_dictionary:
                spam = float(pow(math.e, self.spam_dictionary[i]) * self.p_spam)
                ham = float(pow(math.e, self.ham_dictionary[i]) * self.p_not_spam)
                dict[i] = self.spam_dictionary[i] - float(math.log(spam+ham))

        y = sorted(dict.keys(), key=dict.get)
        return y[:n]

#
#start_time = time.time()
#sf = SpamFilter("homework5_data/train/spam","homework5_data/train/ham", 1e-5)
#for i in range(1, 100):
#    print sf.is_spam("homework5_data/train/ham/ham"+str(i))
#print sf.most_indicative_spam(5)
#print sf.most_indicative_ham(5)

#start_time = time.time()
#sf = SpamFilter("homework5_data/train/spam","homework5_data/train/ham", 1e-5)
#print sf.most_indicative_ham(50)
#print time.time() - start_time



############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
It took me about 6 hours.
"""

feedback_question_2 = """
Understanding the formulas took me longer time.
"""

feedback_question_3 = """
All of the questions are very reasonable and interesting.
"""
