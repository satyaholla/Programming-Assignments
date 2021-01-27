## 6.0001 Pset 1: Part c
## Name: Satya Holla
## Time Spent: 10 minutes
## Collaborators: Teonezcayotl GutieRuiz

""" I am using a backslash (\) in single-line comments that are supposed to be read across multiple lines"""

#############################################
## Get user input for starting_amount below ##
#############################################
starting_amount = float(input("Enter the initial deposit: ")) # get user input for starting amount
#########################################################################
## Initialize other variables you need (if any) for your program below ##
#########################################################################

#Initializations                      Descriptions

house_cost = 750000                 # given cost of house
down_payment = .25 * house_cost     # down payment is 25% of house cost
current_savings = starting_amount   # the current savings starts out at starting amount
no_of_months = 36                   # 3 years = 36 months
r_min = 0                           # r_min and r_max used in bisection search as upper\
r_max = 1                           # \and lower bound of r, and are reset throughout the loop
r = 0.                              # current value of r, set in loop to avg(r_min, r_max)
steps = 0                           # keeps track of steps in search
########################################################################################################
## Determine the lowest return on investment needed to get the down payment for your dream home below ##
########################################################################################################
if down_payment - starting_amount*(1+1/12)**36 > 100:               # if starting amount is too low to\
    r = None                                                        # \reach the down payment, r = None
elif starting_amount < down_payment:                                # start loop if starting amt isn't too high; if it is too high, r = 0
    while abs(current_savings - down_payment) > 100:                # continue loop if current r doesn't output a close enough savings
        steps += 1                                                  # increment steps
        r = (r_min + r_max)/2                                       # since it's a bisection, let r = arithmetic mean of min and max
        current_savings = starting_amount*(1+r/12)**no_of_months    # set value of current savings using given formula
        if current_savings - down_payment > 100:                    # make current r the upper bound for r if it's too high
            r_max = r
        elif down_payment - current_savings > 100:                  # make current r the lower bound for r if it's too low
            r_min = r
##########################################################
## Print out the best savings rate and steps taken here ##
##########################################################
print("Best savings rate:", r)              # output savings rate
print("Steps in bisection search:", steps)  # output number of steps
