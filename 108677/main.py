from datetime import datetime, timedelta
# defining inital bank deposit
initial_bank_deposit = {1:10, 5:10, 10:10, 50:10, 100:10}

# defining a dictionary whick keys are the  usernames and the values are a list of the amout of money before last interaction and after last interaction
# and the time of the last interaction
usernames = {}

# defining a list to store all inputs [[the order of that input, the input], ...]
inputs = []



# defining a function to convert date type to a pythonic format
def change_time(s):
    s_change = datetime.strptime(s,"%Y/%m/%d-%H:%M:%S")
    return s_change
    

n = int(input())

# difining a list to store the answers of the commands
answers = [0] * n

# read all inputs and store them in a list
for i in range(n):
    case = input().split()
    case[-1] = change_time(case[-1])
    inputs += [[i] + case]

# sorting the commands in ascending order according to the dates
sorted_inputs = sorted(inputs, key= lambda x: x[-1])

for input in sorted_inputs:
    # defining the place of the answer of the request in the answer list
    idx = input[0]
    # if the request was registering
    if input[1] == "REGISTER":
        if input[2] in usernames:
            answers[idx] = "Duplicate User!"
        else:
            usernames[input[2]] = [[0, 100], input[3]]
            answers[idx] = "Registered Successfully"

    # if the request was deposit
    elif input[1] == "DEPOSIT":
        if input[2] in usernames:
            # updating the fund before and after the deposit date
            usernames[input[2]][0][0] = usernames[input[2]][0][1]
            usernames[input[2]][0][1] += int(input[3])
            usernames[input[2]][1] = input[4]
            answers[idx] = usernames[input[2]][0][1]

        else:
            answers[idx] = "No Such User Found!"

    # if the request was withdraw
    elif input[1] == "WITHDRAW":
        if input[2] not in usernames:
            answers[idx] = "No Such User Found!"
        else:
            # checking if the date of the withdraw is before of after the last interaction
            if input[4] < usernames[input[2]][1]:
                money_case = usernames[input[2]][0][0]
            else:
                money_case = usernames[input[2]][0][1]

            if int(input[3]) > 200:
                answers[idx] = "Maximum Amount Exceeded!"

            elif money_case < int(input[3]):
                answers[idx] = "Not Enough Fund!"

            else:
                # check if we can pay the money with current coins in the bank
                remaining_amount = int(input[3])
                first_situation = initial_bank_deposit.copy()
                for coin_value in sorted(initial_bank_deposit.keys(), reverse=True):
                    if remaining_amount >= coin_value:
                        num_coins = min(remaining_amount // coin_value, initial_bank_deposit[coin_value])
                        remaining_amount -= num_coins * coin_value
                        initial_bank_deposit[coin_value] -= num_coins
                if remaining_amount != 0:
                    answers[idx] = 'Not Enough Banknotes!'
                    initial_bank_deposit = first_situation
                    
                else:
                    if input[4] < usernames[input[2]][1]:
                        usernames[input[2]][0][0] -= int(input[3])
                        usernames[input[2]][0][1] -= int(input[3])
                        usernames[input[2]][1] = input[4]
                    else:
                        usernames[input[2]][0][0] = usernames[input[2]][0][1]
                        usernames[input[2]][0][1] -= int(input[3])
                        usernames[input[2]][1] = input[4]

                    answers[idx] = money_case - int(input[3])
        
    
    elif input[1] == "TRANSFER":
        if (input[2] not in usernames) or (input[3] not in usernames):
            answers[idx] = "No Such User Found!"
        else:
            if input[5] < usernames[input[2]][1]:
                money_case = usernames[input[2]][0][0]
            else:
                money_case = usernames[input[2]][0][1]
                
            if int(input[4]) > 3000:
                answers[idx] = "Maximum Amount Exceeded!"

            elif money_case < int(input[4]):
                answers[idx] = "Not Enough Fund!"

            else:
                if input[5] < usernames[input[2]][1]:
                    usernames[input[2]][0][0] -= int(input[4])
                    usernames[input[2]][0][1] -= int(input[4])
                    usernames[input[2]][1] = input[5]
                else:
                    usernames[input[2]][0][0] = usernames[input[2]][0][1]
                    usernames[input[2]][0][1] -= int(input[4])
                    usernames[input[2]][1] = input[5]

                # transfering money to the destination deposit
                timestamp = input[5] + timedelta(hours = 1)
                usernames[input[3]][0][0] = usernames[input[3]][0][1]
                usernames[input[3]][0][1] += int(input[4])
                usernames[input[3]][1] = timestamp

                answers[idx] = money_case - int(input[4])


    elif input[1] == "GET_BALANCE":
        if input[2] not in usernames:
            answers[idx] = "No Such User Found!"

        else:
            if input[3] < usernames[input[2]][1]:
                money_case = usernames[input[2]][0][0]
            else:
                money_case = usernames[input[2]][0][1]

            if money_case < 10:
                answers[idx] = "Not Enough Fund!"

            else:
                if input[3] < usernames[input[2]][1]:
                    usernames[input[2]][0][0] -= 10
                    usernames[input[2]][0][1] -= 10
                    usernames[input[2]][1] = input[3]
                else:
                    usernames[input[2]][0][0] = usernames[input[2]][0][1]
                    usernames[input[2]][0][1] -= 10
                    usernames[input[2]][1] = input[3]
                answers[idx] = money_case - 10

        
    elif input[1] == "ADD_BANKNOTE":
        initial_bank_deposit[int(input[2])] += int(input[3])
        answers[idx] = sum(key * value for key, value in initial_bank_deposit.items())
        
print(*answers, sep = "\n")



