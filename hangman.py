"""
Create a simple hangman game
"""
import random

# create word dictionary
three_letters = ['tie', 'gun', 'mat']
four_letters = ['fish', 'sack', 'jump', 'wind']
five_letters = ['phone', 'range', 'grill']
six_letters = ['turtle', 'bottle', 'tablet']
seven_letters = ['monitor', 'prepare', 'octopus']

word_list = three_letters + four_letters + five_letters + \
            six_letters + seven_letters

# randomly select one word
# random.seed(9)
wordchoice = random.choice(word_list)
# print(wordchoice)
wordlen = len(wordchoice)

correct_guess = []
wrong_guess = []
tried_guess = []

print('** Game Start **')
print('It is a %d letters word: %s' % (wordlen, '_ '*wordlen))
while True:
    guess = input('\nInput a letter:')

    # validate user input is alphabet and single letter
    guess = guess.lower()
    if not guess.isalpha():
        print('Input an alphabet!')
        continue
    elif len(guess) > 1:
        print('Input a single letter!')
        continue

    # check if user guessed this letter before
    if tried_guess.__contains__(guess):
        print('You guessed that before')
        continue
    else:
        tried_guess.append(guess)

    # Check if letter is correct
    if guess in wordchoice:
        correct_guess.append(guess)
        letter_pos = [i for i,letter in enumerate(wordchoice) if letter in correct_guess]
        build_answer = [letter+' ' if i in letter_pos else '_ ' for i,letter in enumerate(wordchoice)]
        print('Your word:', ''.join(build_answer))
        if len(correct_guess) == len(set(wordchoice)):
            print('You guess all correctly! Congratulation!')

    else:
        wrong_guess.append(guess)
        print('Nope!! You have',5 - len(wrong_guess), 'tries left')
        if (5 - len(wrong_guess)) == 0:
            print('You run out of tries!')
            break

print('** Game End **')