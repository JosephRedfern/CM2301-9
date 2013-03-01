###############################################
## Creates multiple choice test              ##
## Uses user to input question and answer    ##
## Saves all information into dictionaries   ##
## For later use out side module             ##
###############################################

import random

###########################
## Creation of Questions ##
###########################

    
# dictionary saves the questions with their answer choices
dictionary = {}

#user input: number of questions to create
number_questions = input('How many questions would you like to add to the pool? ')
# number_ans --> the number of multiple choices
number_ans = int(4)

# dictionary_count --> the number of questions currently stored
dictionary_count = int()
dictionary_count = dictionary_count + number_questions


#loop to create number of questions required
for i in range(number_questions):

    #input question
    question = raw_input('Insert question: ')

    #input correct and incorrect choices
    correctA = raw_input('Insert correct answer: ')
    incorrectA1 = raw_input('Insert first incorrect answer choice: ')
    incorrectA2 = raw_input('Insert second incorrect answer choice: ')
    incorrectA3 = raw_input('Insert third incorrect answer choice: ')

    #add to dictionary
    self.dictionary[question] = correctA, incorrectA1, incorrectA2, incorrectA3

# print it all out to check
print self.dictionary
print "Questions saved"


####################
##  Generate Test ##
####################

# new dictionary for test storage
new_test = {}

# general test info
module_title = raw_input('Module Title: ')
lecturer_name = raw_input('Lecturer Name: ')
test_title = raw_input('Test Title: ')

# how many questions to select
print "There are already ", dictionary_count, " questions in the database."
input_questions = input('How many questions would you like in the test? ')

# error message
if input_questions > dictionary_count:
    print "Incorrect entry"
    input_questions = input('How many questions would you like in the test? ')

# randomly select questions from dictionary
chosen_questions = random.sample(dictionary.items(), input_questions)
print "random choice ", chosen_questions

#save test into own dictionary
self.new_test[test_title] = module_title, lecturer_name, chosen_questions

print self.new_test

###############################
## Creation of test complete ##
###############################

