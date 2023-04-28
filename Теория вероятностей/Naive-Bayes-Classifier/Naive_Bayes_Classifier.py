import math
import re 
import os


class Msg:
    def __init__(self, data_path):

        self.data_path = data_path #Path to the spam/non-spam directory
        self.cnt = 0 #The number of emails in the directory
        self.prob = 0 #Probability of email being classified as spam/non-spam
        self.dct = {} #All words found in spam/non-spam emails and their number
        self.sum_of_probs = 0 #The sum of the probabilities that the words of the email are spam/non-spam

    def get_word_cnt(self, word): #Number of spam/non-spam emails with the word 'word'

        if self.dct.get(word) != None:
            return self.dct.get(word)

        return 0

    def find_prob(self, word): #Finding the probability that a word is from a spam/non-spam email using Laplace smoothing
        self.sum_of_probs += math.log10(self.get_word_cnt(word) + 1 / self.cnt + 2)
    

spam = Msg('./Spam')
non_spam = Msg('./No spam')


def handle_Emails(path, dct, cntFiles = 0): #Handling a directory of spam/non-spam emails

    files = os.listdir(path)

    for i in range(0, len(files)):

        file = path + '\\' + files[i]

        if os.path.isfile(file):
            
            cntFiles += 1

            with open(file, 'r') as inp:

                try:
                    text = set(re.sub(r'[^\w\s]', ' ', inp.read()).lower().split()) #Getting a set of words of a email
                        
                    for word in text: #Adding email words to the dictionary

                        cnt = 1

                        if dct.get(word) != None:
                            cnt = dct.get(word) + 1

                        dct.update({word: cnt})

                except:
                    continue
                
        else:
            cntFiles = handle_Emails(file, dct, cntFiles)

    return cntFiles

    
spam.cnt = handle_Emails(spam.data_path, spam.dct)
non_spam.cnt = handle_Emails(non_spam.data_path, non_spam.dct)

spam.prob = spam.cnt / (non_spam.cnt + spam.cnt)
non_spam.prob = non_spam.cnt / (non_spam.cnt + spam.cnt)

print('Enter "end" to finish')
while (1):

    newMsg = input('Enter the path to the message to be classified: ')

    if newMsg.lower() == 'end':
        break

    try:
        with open(newMsg, 'r') as inp:

            try:
                text = set(re.sub(r'[^\w\s]', ' ', inp.read()).lower().split())

                for word in text:          
                    spam.find_prob(word)
                    non_spam.find_prob(word)

                print('It is most likely that this letter is ', end = '')
        
                if math.log10(spam.prob) + spam.sum_of_probs > math.log10(non_spam.prob) +  non_spam.sum_of_probs:
                    print('spam\n')
                else:
                    print('no spam\n')
                
                spam.sum_of_probs = 0
                non_spam.sum_of_probs = 0

            except:
                print('Unable to process email\n')

    except:
        print('Unable to open email\n')