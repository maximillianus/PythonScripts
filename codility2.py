BIGGEST_N = 2147483647



test1 = 123
test2 = 3544
test3 = 6559
test4 = 1
test6 = 123456789456

def solution(N):
    def_output = 0
    N_LIMIT = 100000000

    # If bigger then specified limit, return -1
    if N > N_LIMIT:
        def_output = -1
        return def_output

    # Convert number into string, split it to list, then sort it descending
    N_list = sorted([int(d) for d in str(N)], reverse=True)

    # Join back number into string from list
    N_joined = ''.join(str(x) for x in N_list)

    # Convert string to int
    N_joined_int = int(N_joined)
    return N_joined_int
    pass


mysolution = solution(test6)
print(mysolution)
#print(''.join(str(x) for x in mynumberlist_sorted) )