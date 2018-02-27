import re

pwd1 = 'a1Ba'
pwd2 = '0bBBb1BBA'
pwd3 = 'aB1a'
pwd4 = 'aBa0aB'
pwd5 = 'a1B2abB'


def solution(yourpass):
    def_output = -1
    strlen = 0

    # Split password by number
    pwd_substring_list = re.split('[0-9]', yourpass)

    # find longest valid substring length
    for substr in pwd_substring_list:
        if re.search('[A-Z]', substr) is not None:
            if len(substr) > strlen:
                strlen = len(substr)
    # def output will be whatever non-zero strlen is
    if strlen != 0:
        def_output = strlen
    return def_output


valid_chk = solution(pwd2)


print(valid_chk)
