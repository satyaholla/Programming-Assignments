def part_b(salary, savings_percent, total_cost, raise_percentage):
	#########################################################################
	""" Set down payment to 0.15 (given in problem), amount saved
	to 0 (given), and the interest rate to 5% (or 0.05), which is
	also given, and you start off at 0 months. """
	percent_down_payment = 0.15
	amount_saved = 0
	r = 0.05
	months = 0
	
	###############################################################################################
	## Determine how many months it would take to get the down payment for your dream home below ##
	###############################################################################################
	""" the loop iterates for each month, and after each iteration, the value of amount saved
	increases by the appropriate amount. This continues until amount saved > cost of down payment.
	Here, there is the added salary raise section, which is given in the if statement """
	while amount_saved < total_cost*percent_down_payment: #cost of down payment is the total cost times the down payment percentage
	    months = months + 1 #iterates the number of months (each loop represents the end of a month)
	    amount_saved *= 1 + r/12 #investment return: the amount saved increases by amount_saved*r/12, since r is ANNUAL
	    amount_saved += salary*savings_percent/12 #how much you earn from the salary
	    if months % 6 == 0: #every 6 months,
	        salary *= 1 + raise_percentage #salary is compounded in the same was as amount_saved
	
	#######################################################
	## Print out the number of months it would take here ##
	#######################################################
	print ("Number of months:", months) #print output
	return months