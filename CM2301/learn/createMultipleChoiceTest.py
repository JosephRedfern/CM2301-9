###############################################
## Creates multiple choice test              ##
## Uses user to input question and answer    ##
## Saves all information into dictionaries   ##
## For later use out side module             ##
###############################################

module_title = raw_input('Module Title: ')
lecturer_name = raw_input('Lecturer Name: ')
test_title = raw_input('Test Title: ')

#number of questions in the test
number_questions = input('How many questions would you like in the test? ')
#number of multiple choice answers in the test
number_ans = input('Enter a number of possible answers between 2 and 4')


#ERROR:- if number >2 or <4 chosen display error
if number_ans <2 or number_ans > 4:
    print 'Invalid Choice!'
    number_ans = input('Enter a valid number of answers, between 2 and 4')
    #if error happens again, will need to rerun - needs to be implemented via button perhaps?
    if number_ans <2 or number_ans > 4:
        print 'Error, restart'

        

##########################
## Choice of 2 answers  ##
##########################

if number_ans == 2:

    #dictionary saves the questions with their correct and incorrect answers
    dictionary = {'Question' : {'Correct Answer' : 'Incorrect Answer'}}

    #loop to create number of questions required
    for i in range(number_questions):

        #input question
        question = raw_input('Insert question: ' )

        #input correct and incorrect choices
        correctA = raw_input('Insert correct answer: ')
        incorrectA = raw_input('Insert incorrect answer choice: ')

        #add to dictionary
        dictionary[question] = correctA, incorrectA

    print dictionary

    #save the whole test - title etc included
    save_test = {'Test Title' : {'Lecturer Name' :
                               {'Module Title' :{'Question' :
                                               {'Correct Answer' : {'Incorrect Answer'}}}}}}

    save_test[test_title] = module_title, lecturer_name, question, correctA, incorrectA
    print save_test

    

#########################
## Choice of 3 answers ##
#########################


elif number_ans == 3:

    #dictionary saves the questions with their correct and incorrect answers
    dictionary = {'Question' : {'Correct Answer' :
                                {'Incorrect Answer' : 'Incorrect Answer'}}}

    #loop to creat number of questions required
    for i in range(number_questions):

        #input question
        question = raw_input('Insert question: ')

        #input correct and incorrect choices
        correctA = raw_input('Insert correct answer: ')
        incorrectA1 = raw_input('Insert first incorrect answer choice: ')
        incorrectA2 = raw_input('Insert second incorrect answer choice: ')

        #add to dictionary
        dictionary[question] = correctA, incorrectA1, incorrectA2

    # print it all out to check
    print dictionary

    #save the whole test - title etc included
    save_test = {'Test Title' : {'Lecturer Name' :
                               {'Module Title' :{'Question' :
                                               {'Correct Answer' : {'Incorrect Answer' :'Incorrect Answer'}}}}}}

    save_test[test_title] = module_title, lecturer_name, question,correctA, incorrectA1, incorrectA2
    print save_test




#########################
## Choice of 4 answers ##
#########################

elif number_ans == 4:

    #dictionary saves the questions with their correct and incorrect answers
    dictionary = {'Question' : {'Correct Answer' :
                                {'Incorrect Answer' : {'Incorrect Answer' : 'Incorrect Answer'}}}}

    #loop to creat number of questions required
    for i in range(number_questions):

        #input question
        question = raw_input('Insert question: ')

        #input correct and incorrect choices
        correctA = raw_input('Insert correct answer: ')
        incorrectA1 = raw_input('Insert first incorrect answer choice: ')
        incorrectA2 = raw_input('Insert second incorrect answer choice: ')
        incorrectA3 = raw_input('Insert third incorrect answer choice: ')

        #add to dictionary
        dictionary[question] = correctA, incorrectA1, incorrectA2, incorrectA3

    # print it all out to check
    print dictionary

    #save the whole test - title etc included
    save_test = {'Test Title' : {'Lecturer Name' :
                               {'Module Title' :{'Question' :
                                               {'Correct Answer' : {'Incorrect Answer' :
                                                                    {'Incorrect Answer' : 'Incorrect Answer'}}}}}}}

    save_test[test_title] = module_title, lecturer_name, question,correctA, incorrectA1, incorrectA2, incorrectA3
    print save_test



###############################
## Creation of test complete ##
###############################
 
   
