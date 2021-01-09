import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import numpy as np
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)
from pandas import *


def function1(total_votes_republicans,total_votes_democrats,seats_r,seats_d,state_name):

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

                print("For state ", state_name, "the proposed solution with method 2 is: ")
                print("mult is:", mult)
                #table_votes_rescaled = np.round(table_votes_rescaled)
                print("I obtain: \n", DataFrame(table_votes_rescaled.astype(int)))
                return table_votes_rescaled, mult

    if mult >= 1.9990:
        print("No solution was found for ", state_name)
        return

##########################################################################################################################
# Change the data path accordingly. Please download the 1976-2018-house2.csv file from https://www.kaggle.com/tunguz/us-elections-dataset
data_path_of_csv_file = r'C:\Users\Lavinia\Desktop\ETH COURSES\3st semester\Mathematics in politics and law\project\1976-2018-house2.csv'
##########################################################################################################################
# DATA PRE-PROCESSING
df = pd.read_csv(data_path_of_csv_file, encoding= 'unicode_escape') # Read the data from the .csv file
df = df[df.year == 2018] # Select only the data from the 2018 elections
states_list = sorted(list(set(df.state.tolist()))) # Sort the states list alphabetically
columns_list = ['state', 'district', 'party', 'candidatevotes', 'totalvotes']
df = df[columns_list]# Select only relevant information from the big database

for state_name in states_list: # iterate over all the american states
    df_name = "df_2018_" + state_name # give the sub-dataset for the specific state a name
    sub_df = df[df.state == state_name] # sub_df only refers to data of the inmultidual states
    number_of_districts = sub_df["district"].unique() # get the number of districts within the state
    newsubdf = pd.DataFrame() # newsubdf will be the pandas dataframe where data of interest are stored (for each state)
    newsubdf["Party"] = ['Republicans','Democrats'] # create the column containing the party rows (rep. and dem.)
    seats = 0 # initialize the number of seats which will be equal to the number of districts
    array_votes_republicans = [] # store here the votes given to the republicans from each district
    array_votes_democrats = [] # store here the votes given to the democrats from each district
    total_votes_republicans = 0 # counts the total votes given to republicans: sum over first row
    total_votes_democrats = 0 # counts the total votes given to democrats: sum over first row
    for district_number, group in sub_df.groupby('district'): # iterate over districts
        # count the votes given to the republicans and fill the array array_votes_republicans
        if (group.party == "republican").any():
            row_rep = group.loc[sub_df['party'] == "republican"]
            a = row_rep.iloc[0]['candidatevotes']
            total_votes_republicans+=a
            array_votes_republicans.append(a)
        else:
            a = 0 # in some ditricts republicans are not present:
            array_votes_republicans.append(a)
        # count the votes given to the democrats and fill the array array_votes_democrats
        if (group.party == "democrat").any():
            row_dem = group.loc[(group['party'] == "democrat")]
            b = row_dem.iloc[0]['candidatevotes']
            total_votes_democrats+=b
            array_votes_democrats.append(b)
        elif(group.party == "democratic-npl").any(): # in some ditricts democratic-npl is present:
            row_dem = group.loc[(group['party'] == "democratic-npl")] # NPL stands for Nonpartisan League Party
            b = row_dem.iloc[0]['candidatevotes']
            total_votes_democrats += b
            array_votes_democrats.append(b);
        else:
            b=0; # in some ditricts democratics are not present:
            total_votes_democrats += b
            array_votes_democrats.append(b)

        newsubdf["District_"+f'{district_number}'] = [a, b]
        seats+=1

    # Here table_votes_all is obtained and its similar to the Connecticut's example.
    array_votes_republicans = np.reshape(np.asarray(array_votes_republicans),(1,seats))
    array_votes_democrats = np.reshape(np.asarray(array_votes_democrats),(1,seats))
    table_votes_all = np.concatenate((array_votes_republicans, array_votes_democrats))
    # Example result for table_votes_all in Arkansas
    # +-------------+------------+------------+------------+------------+
    # | Party       | District_1 | District_2 | District_3 | District_4 |
    # +-------------+------------+------------+------------+------------+
    # | Republicans |   138757   |   132125   |   148717   |   136740   |
    # +-------------+------------+------------+------------+------------+
    # | Democrats   |   57907    |   116135   |   74952    |   63984    |
    # +-------------+------------+------------+------------+------------+

    print("===========================================================================================================")
    print("In the original 2018 elections, the situation in " + state_name + " was:\n")
    print(DataFrame(newsubdf))
    print("-----------------------------------------------------------------------------------------------------------\n")

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
        print("For state ", state_name, "the election results are fair as they are:")
    else:
        print("For state ", state_name, "the election results are NOT fair.")

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
        function1(total_votes_republicans, total_votes_democrats, seats_r, seats_d, state_name)
        # METHOD 2 ----------------------------------------------------------------------------------------------- end - #
    # CHECK IF ELECTIONS ARE FAIR ---------------------------------------------------------------------------- END - #











