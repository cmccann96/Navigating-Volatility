
import requests
import json
import math

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import re

import sys

from util import column_sum
import datetime





download_path = r'C:\Users\Conne\Downloads'
optimum_pip = pd.read_csv('test_optimum.txt', sep = ",")



number_of_misses = 0

INST_NAME = optimum_pip['PAIR'].tolist()
PIP = optimum_pip['PIP'].tolist()

# factor_list =  [0.75,0.8,0.85,0.9,0.95,1,1.05,1.10,1.15,1.2,1.25]
# factor_list = [1]
factor_list = [1]
# n_list = list(range(1,50,5))
# m_list = list(range(25,100,5))

n_list = [50,41,36,26,2]
m_list = [100,90,80,75,70]
pip_test_list = [17,19,21,23,25,27,29,31,33,35,37,39,41]
monday_wins = 0
monday_losses = 0
chosen_day = 'Monday'

try:
    del dates_ml
except:
    pass


dates_ml = pd.read_csv('Date_ML.csv')

for instrument_name,pip in zip(INST_NAME, PIP):
    print(instrument_name)
# for pip_test in pip_test_list:
    loss_counter = 0
    # pip = pip_test
    # pip = 20
# print(instrument_name)
# tags = pd.read_csv(os.path.join(download_path, instrument_name + '_Candlestick_1_Hour_BID_10.01.2017-17.12.2019' + '.csv'))
    tags = pd.read_csv('historical_data/' + instrument_name + '_withsp500_historical.csv')
    

    

    days = []
    draws = []
    pair = []
    pair_draw = []
    movement_amounts = []
    longs = []
    pair_longs = []
    shorts = []
    pair_shorts = []
    wins = []
    wins_pairs = []
    close_pricing_list_1 = []
    close_pricing_list_2 = []

    if 'JPY' in instrument_name:
        pip = pip/100
        spread = 0.006
        # pip_list = list(np.linspace(0.1,0.4,30))
    
    else:
        pip = pip/10000
        # pip_list = list(np.linspace(0.001,0.004,30))
        spread = 0.00004

    # rename each variable is tags
    tags = tags.rename(columns = lambda x : 'tag_' + str(x))
    # print(tags.head())
    # tags.columns = ['test','open', 'high', 'low', 'close','voluem']
    tags.columns = ['bab','bad','test','open', 'high', 'low', 'close','voluem','Fianl Date','rdm','rdm_2','rdm_3','oanda_open','Open_sp','High_sp','Low_sp',
    'Close_sp','Volume_sp']
    del tags['bad']
    tags['DATE'] = tags['test'].astype(str).str[:5]
    tags['TIME'] = tags['test'].astype(str).str[11:13:1]

    # tags['TIME'] = tags.TIME.astype(float)
    # tags['DATE'] = pd.to_datetime(tags['DATE'])
    # tags['test'] = pd.to_datetime(tags['DATE'])
    # view the tags dataframe

    tags_index = []
    tags_index_start = []

    for i in range(0, len(tags)):

        if tags['TIME'].iloc[i] == '09':
            break
        else:
            tags_index_start.append(i)

    for i in range(0,len(tags)):
        if tags['DATE'].iloc[i] == '13.12':
            if tags['TIME'].iloc[i] == '09':
                for j in range(i,len(tags)):                
                    tags_index.append(j)
                    if tags['DATE'].iloc[j] == '03.01':                    
                        if tags['TIME'].iloc[j] == '08':
                            break






    # for index in sorted(tags_index, reverse=True):
    # tags.drop(tags.index(1),inplace =True)
    tags = tags.drop(tags_index_start)
    tags = tags.drop(tags_index)


    # tags.to_csv('tag_test.csv')

    #must change these for full year test
    first = list(range(0,17000,24))
    second = list(range(48,28800,24))



    day_iterator = list(range(26,47))
    postition_activator = list(range(24,47))

    df = pd.DataFrame(index = ['pip','loss','freq'], columns = ['pip','loss','freq'])
    dates_recorder = pd.DataFrame(index = ['Dates',instrument_name], columns = ['Dates',instrument_name])

    # for pip in pip_list:
    
    counter = 0
    loss = 0
    freq = 0
    total = 0



    ##############################3  PERFORMING THE TESTING #################################################3

    for i,j in zip(first,second):
        day = tags[i:j]
        max_movement = [0]

        action = day['oanda_open'].iloc[24] - day['oanda_open'].iloc[0] 
        sp_action = day['Open_sp'].iloc[24] - day['Open_sp'].iloc[0] 
        total +=1
        
        if math.isnan(action):
            action = day['open'].iloc[24] - day['open'].iloc[0]
        
        checker = 'no'


        if (datetime.datetime.strptime(day['test'].str[:10].iloc[24], '%d.%m.%Y').strftime('%A')) == 'Monday':
            continue


        # # CALCULATING THE MA
        # # n= 5            
        # # m = 10
        # if len(close_pricing_list_1) < n:
        #     close_pricing_list_1.append(day['oanda_open'].iloc[24])
            
        # else:
        #     del close_pricing_list_1[0]
        #     close_pricing_list_1.append(day['oanda_open'].iloc[24])

        # if len(close_pricing_list_2)  < m:
        #     close_pricing_list_2.append(day['oanda_open'].iloc[24])
        #     continue
        # else:
        #     del close_pricing_list_2[0]
        #     close_pricing_list_2.append(day['oanda_open'].iloc[24])



        # k_n = 2/(1+n)
        # k_m = 2/(1+m)
        # try:
        #     old_moving_average_1 = moving_average_1
        # except:
        #     pass
        # try:
        #     old_moving_average_2 = moving_average_2
        # except:
        #     pass
        
        # #standard MA
        # moving_average_1  = (sum(close_pricing_list_1))/n
        # moving_average_2  = (sum(close_pricing_list_2))/m


        # try:
            
        #     moving_average_1 = ((day['oanda_open'].iloc[24])*k_n) + (old_moving_average_1 * (1-k_n))
        #     # if math.isnan(moving_average_1):
        #     #     moving_average_1  = (sum(close_pricing_list_1))/n
            
        # except:
        #     moving_average_1  = (sum(close_pricing_list_1))/n

            

        # try:
        #     moving_average_2 = ((day['oanda_open'].iloc[24])*k_m) + (old_moving_average_2 * (1-k_m))
        #     # if math.isnan(moving_average_2):
        #     #     print('reconfig')
        #     #     moving_average_2  = (sum(close_pricing_list_1))/m
            
        # except:
        #     moving_average_2  = (sum(close_pricing_list_2))/m
        
        freq += 1
        
    
        ######iterating over days now

        for k in day_iterator:
            high = abs(day['high'].iloc[k] - day['oanda_open'].iloc[24]) 
            low = abs(day['low'].iloc[k] - day['oanda_open'].iloc[24])

            if high > max_movement[0]:
                max_movement = [high]
            if low > max_movement[0]:
                max_movement = [low]
        
        if len(movement_amounts) < 6:
            movement_amounts.append(max_movement[0])
        else:
            del movement_amounts[0]
            movement_amounts.append(max_movement[0])
        
        average_day_mover = sum(movement_amounts) / len(movement_amounts)
        
        # proportion = 0.6
        # take_profit = proportion * average_day_mover
        # stop_loss = proportion * average_day_mover

        take_profit = pip
        stop_loss = pip
        
        for k in day_iterator:
            

            current_open = day['open'].iloc[k]

            day_open = day['oanda_open'].iloc[24]
            if math.isnan(day_open):
                day_open = day['open'].iloc[24] 
            high = day['high'].iloc[k] - day_open
            low = day['low'].iloc[k] - day_open
            current_low = day['low'].iloc[k]
            current_high = day['high'].iloc[k]

            
            
            if counter >= 5:
                loss_counter += 1
                
                loss = 1
                counter = 0
                days.append(tags['test'].str[:10].iloc[i])
                pair.append(instrument_name)
                
                
                
                
            if k == 45 and counter == 0:
                counter += 1
                number_of_misses += 1
                break

            if k ==45 and counter == 1:
                counter += 0.5
                break

                
            # if k == 45 and counter > 1:
            #     counter += 0.2
            #if the order has been activated just go through standard checking now
            if checker == 'yes':
                if sp_action > 0:
                
                    if action < 0:
                    
                    #stop loss tester
                        if high > ((stop_loss))-spread:
                            counter += 1
                            
                            if (datetime.datetime.strptime(day['test'].str[:10].iloc[24], '%d.%m.%Y').strftime('%A')) == chosen_day:
                                monday_losses += 1
                            
                            break

                        #take profit testor
                        if low < take_profit *(-1) - spread:
                            counter = 0
                            
                            if (datetime.datetime.strptime(day['test'].str[:10].iloc[24], '%d.%m.%Y').strftime('%A')) == chosen_day:
                                monday_wins += 1
                            break

                    
                    if action > 0:
                    

                        #take profit tester
                        if high > (take_profit) + spread:
                            counter = 0
                            
                            if (datetime.datetime.strptime(day['test'].str[:10].iloc[24], '%d.%m.%Y').strftime('%A')) == chosen_day:
                                monday_wins += 1
                            break

                        #stop loss tester
                        if low < ((stop_loss *(-1))) + spread:
                            counter += 1
                            
                            if (datetime.datetime.strptime(day['test'].str[:10].iloc[24], '%d.%m.%Y').strftime('%A')) == chosen_day:
                                monday_losses += 1
                            break

                else:

                    if action > 0:
                
                    #stop loss tester
                        if high > ((stop_loss))-spread:
                            counter += 1
                            
                            
                            break

                        #take profit testor
                        if low < take_profit *(-1) - spread:
                            counter = 0
                            
                            
                            break

                    
                    if action < 0:
                        

                        #take profit tester
                        if high > (take_profit) + spread:
                            counter = 0
                            
                            
                            break

                        #stop loss tester
                        if low < ((stop_loss *(-1))) + spread:
                            counter += 1
                            
                                
                            break
                        
                
                

            #Testing to see if the order has been activated

            else:
                if current_open > day_open:
                    if current_low < day_open:
                        checker = 'yes'

                            
                if current_open < day_open:
                    if current_high > day_open:
                        checker = 'yes'


        # print("the pip here is:  " + str(pip_test) + "with a loss of:  " + str(loss_counter))    
        

    # df = pd.DataFrame({'Dates': days, instrument_name : pair})
    # df[instrument_name] = 'L'

    df = pd.DataFrame({'Dates': days, instrument_name : pair})
    df[instrument_name] = 1
            

    dates_ml = pd.merge(dates_ml,df[['Dates',instrument_name]], on = 'Dates', how = 'left')

    # for date in draws:
    #     dates_ml.loc[dates_ml['Dates'] == date, instrument_name] = 'D'

    # for date in wins:
    #     dates_ml.loc[dates_ml['Dates'] == date, instrument_name] = 'W'

# dates_ml.dropna(subset = ['AUDNZD'], inplace = True)

# print(dates_ml.head())
dates_ml.to_csv('Results/Sp500_testing.csv')

print("the total losses for this strat is:  " + str(column_sum(dates_ml)))
print("the number of inital misses is: " + str(number_of_misses))
print("number of monday losses is :   " + str(monday_losses))
print("number of monday wins is :   " + str(monday_wins))
# print(number_of_misses)
# print(total)
    

