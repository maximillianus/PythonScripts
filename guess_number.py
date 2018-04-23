import random

user_input = 'Y'
randnumber = random.randint(1,100)

while user_input is not 'N':
    # scan user input
    user_input = input('\nGuess a number:')

    print('User input is:', user_input)

    # validate user input
    if user_input.isdigit() == False:
        print('it is not a digit')
        continue

    user_input = int(user_input)
    print('User input class:', type(user_input))
    if user_input < randnumber:
        print('Your guess is too low')
    elif user_input > randnumber:
        print('Your guess is too high')
    else:
        print('Your guess is correct!')
        break


# program ends
print('Bye bye!')