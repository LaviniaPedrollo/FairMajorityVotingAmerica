import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import math
import matplotlib.pyplot as plt
from pandas import *
# Build the Connecticut's table
seats=5
array_votes_republicans = np.reshape(np.array([73273,   165558,  68810, 149891, 165440]),(1,seats))
array_votes_democrats =  np.reshape(np.array([197964,  139987, 199652,  136481,  105505]),(1,seats))
table_votes_all = np.concatenate((array_votes_republicans, array_votes_democrats))
print("---------------------------------------\n In Connecticut 2004 :")
print(table_votes_all)
print("---------------------------------------\n")

total_votes_republicans= 73273 + 165558 + 68810  + 149891 + 165440
total_votes_democrats = 197964 + 139987 + 199652 + 136481 + 105505
total_votes = total_votes_republicans + total_votes_democrats

def function1(total_votes_republicans,total_votes_democrats,seats_r,seats_d):

    # Find multiplier to be applied to either the row of democrats or the row of republicans such that the elctions
    # are fair. Example 1 of Connecticut Elections is followed.
    mult = round(0.0001,4); # I start with a 0 multisor and I keep Increasing until mult == 2;
    districts = seats # I consider a number of seats equal to the number of districs (e.g. one seat per district)
    for mult in np.arange( 0.0000,2.0000, 0.0001 ):
        mult = round(mult, 4) #to have a perfect incrementation of 0.0001 each time

        array_votes_republicans_rescaled = array_votes_republicans
        array_votes_democrats_rescaled = array_votes_democrats * mult
        # if r: # if Republicans should win, rescale the democrats
        #     array_votes_republicans_rescaled = array_votes_republicans
        #     array_votes_democrats_rescaled = array_votes_democrats * mult
        # else: # if Republicans should win, rescale the republicans
        #     array_votes_republicans_rescaled = array_votes_republicans * mult
        #     array_votes_democrats_rescaled = array_votes_democrats
        # Get a similar table of that of the 2004 Connecticut elections
        table_votes_rescaled = np.concatenate((array_votes_republicans_rescaled, array_votes_democrats_rescaled))
        #print(table_votes_rescaled)

        # From now on, the code checks that in the rescaled new table it holds that The number of district-winners is the
        # same of the number of the seats destined to them (selected in the code snippet before). So for example, if 2
        # seats are destined to the democrats and 4 to the republicans, there should be 2 democratic district-winners and
        # 3 republican district-winners.

        seats_r_guess = 0;
        seats_d_guess = 0;
        for i in range(districts):
            r = table_votes_rescaled[0][i]
            d = table_votes_rescaled[1][i]
            if r > d:
                seats_r_guess +=1;
            else:
                seats_d_guess +=1;

        if  (int(seats_r_guess) == int(seats_r) and int(seats_d_guess) == int(seats_d)):

                print("For state Connecticut the proposed solution with method 2 is: ")
                print("mult is:", mult)
                #table_votes_rescaled = np.round(table_votes_rescaled)
                print("I obtain: \n", DataFrame(table_votes_rescaled.astype(int)))
                return table_votes_rescaled, mult

    if mult >= 1.9990:
        print("No solution was found for Connecticut")
        return











# CHECK IF ELECTIONS ARE FAIR ---------------------------------------------------------------------------- start - #
districts = seats  # assume one seat per district
seats_r_in_district_i = 0;  # count how many seats are won by the republicans
seats_d_in_district_i = 0;  # count how many seats are won by the democrats

for i in range(districts):  # iterate over districts
    r = table_votes_all[0][i]  # get the votes for the republican party per district
    d = table_votes_all[1][i]  # get the votes for the democratic party per district
    if r > d:  # update the count of district-winners
        seats_r_in_district_i += 1;  # district i was won by the republicans
    else:
        seats_d_in_district_i += 1;  # district i was won by the democrats
# THE RESULTS ARE CONSIDERED FAIRS IF IT HOLDS TRUE THAT, WHEN THE TOTAL VOTES FOR THE REPUBLICANS IS LARGER (or
# smaller) THAN THE NUMBER OF TOTAL VOTES FOR THE DEMOCRATS, ALSO THE NUMBER OF SEATS WON BY THE REPUBLICANS IS
# LARGER (or smaller) THAN THE NUMBER OF SEATS WON BY THE DEMOCRATS. THIS MEANS THAT THE NUMBER OF REPUBLICAN
# DISTRICT-WINNERS MUST BE LARGER (or smaller) THAN THE NUMBER OF DEMOCRATS DISTRICT-WINNERS.
if ((total_votes_republicans > total_votes_democrats and seats_r_in_district_i > seats_d_in_district_i) or
        (total_votes_republicans < total_votes_democrats and seats_r_in_district_i < seats_d_in_district_i)):
    a = 1
    print("For state Connecticut the election results are fair as they are:")
else:
    print("For state Connecticut the election results are NOT fair.")

    # SEATS APPORTIONMENT ------------------------------------------------------------------------------------ start - #
    # I assume that there is one seat given to each district: #seats = #districts
    districts = seats
    # 1) Get the total number of votes (Rep + Dem)
    total_votes = total_votes_republicans + total_votes_democrats
    # 2) Find the standard multisor SD = Total number of votes (Rep + Dem) / number of seats
    SD = total_votes / seats
    # 3) Calculate quotient as: total votes of party i / SD
    quotient_r = total_votes_republicans / SD
    quotient_d = total_votes_democrats / SD
    # 4) Calculate the seats apportioned by rounding (default is to 0 decimal places)
    seats_r = round(quotient_r)  # number of seats destined to the republicans
    seats_d = round(quotient_d)  # number of seats destined to the democrats
    assert (seats_r + seats_d == seats)  # assert that the calculation is correct
    # The party with the biggest number of total votes wins according to FMV.
    if total_votes_republicans > total_votes_democrats:
        r = 1;
        print("Republicans should win.")
    else:
        r = 0;
        print("Democrats should win.")

    # Avoid cases like: 4 seats for republicans and 4 seats for democrats
    if seats_r == seats_d:
        if r ==1:
            seats_r+=1
            seats_d-=1
        else:
            seats_r -= 1
            seats_d += 1

    print("The seats are apportioned as follows: ")
    print(" --> ", int(seats_r), " seats for republicans.")
    print(" --> ", int(seats_d), " seats for democrats.")
    print("For a total of ", districts, " districts.")
    #SEATS APPORTIONMENT - ------------------------------------------------------------------------------------- end -  #

    # METHOD 1: SIMPLIFIED APPROACH -------------------------------------------------------------------------- start - #
    table_votes_percentages = np.concatenate(
        (array_votes_republicans, array_votes_democrats))  # initialize a new table
    table_votes_percentages = table_votes_percentages.astype(float)
    # table_votes_percentages will contain the two party percentages per districts.
    for i in range(districts):  # iterate over districts
        r = table_votes_all[0][i]  # get the votes for the republican party per district
        d = table_votes_all[1][i]  # get the votes for the democratic party per district

        r_perc = round(r * 100.0 / (r + d), 2)  # percentages of votes to republicans within a district i
        d_perc = round(d * 100.0 / (r + d), 2)  # percentages of votes to democrats within a district i
        assert (r_perc + d_perc == 100.0)  # the sum of the two percentages must be 100
        # Within district i...
        table_votes_percentages[0][
            i] = r_perc  # ... update the table with the percentages of votes to republicans...
        table_votes_percentages[1][
            i] = d_perc  # ... and update the table with the percentages of votes to republicans.

    print("With method 1, I obtain: \n", DataFrame(table_votes_percentages))  # print method 1
    # METHOD 1: SIMPLIFIED APPROACH ---------------------------------------------------------------------------- end - #

    # METHOD 2 ----------------------------------------------------------------------------------------------- start - #
    function1(total_votes_republicans, total_votes_democrats, seats_r, seats_d)
    # METHOD 2 ----------------------------------------------------------------------------------------------- end - #
# CHECK IF ELECTIONS ARE FAIR ---------------------------------------------------------------------------- END - #