import random

user_input = 'Y'

while user_input is not 'N':
    # scan user input
    user_input = input('\nRoll a dice? (Y/N)')

    # print('User input is:', user_input)
    if user_input in ['Y', 'y']:
        # roll dice based on user input
        dice_outcome = random.randint(1,6)
        print('Dice outcome is:', dice_outcome)
    else:
        print('You must input Y or N.')

# program ends
print('User input \'N\' => end program.\nBye bye!')