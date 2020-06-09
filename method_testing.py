import pandas as pd
import numpy as np
from util import column_sum
import itertools

rn = [1,2,3,4,5,6,7,8,9,10]
methods_list = list(itertools.combinations(rn,5))
# 1 is follow trend and 0 is do the opposite

methods_list = [(1,2,3,4,6),(2,4,6,8,10),(1,3,5,7,9),(1,2,5,7,9),(2,4,5,6,10)]

import csv

with open('methods.csv', 'w') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(methods_list)




results = pd.read_csv('result_list.csv')
instruments = pd.read_csv('test_optimum.txt')


instruments_list = instruments['PAIR'].to_list()

method_number = 0
print(instruments_list)
# for methods in methods_list:
#     method_number += 1
#     loss = 0
#     clear = 'yes'

#     try:
#         del dates_ml
#     except:
#         pass

#     dates_ml = pd.read_csv('Date_ML.csv')

for instrument in instruments_list:
    day = []
    i = 0

    results_list = results[instrument].to_list()
    
    clear = 'yes'
    loss = 0
    previous_result = 'None'
    counter = 0
    stage = 0
    
    index = 0
    days = []
    pair = []
    pair = []

    #tracing dicts
    counter_dict = {}
    loss_dict ={}
    stage_dict = {}
    clear_dict = {}
    for methods in methods_list:
        loss_dict[methods] = 0
        counter_dict[methods] = 0
        stage_dict[methods] = 0
        clear_dict[methods] = 0
    
    for result in results_list:
        for methods in methods_list:
            
            i += 1
            index += 1
            if stage_dict[methods] == 5:
                stage_dict[methods] = 0
            
            if counter_dict[methods] >= 5:
                loss_dict[methods] += 1
                counter = 0
            
          

                try:
                    loss_dict[methods] += 1
                except:
                    loss_dict[methods] = 1
                clear_dict[methods] = 'no'

            
            if result == 'W':
                if methods[stage_dict[methods]] % 2 == 1:
                    clear_dict[methods] = 'yes'
            if result == 'L':
                if methods[stage_dict[methods]] % 2 == 0:
                    clear_dict[methods] = 'yes'

            if clear_dict[methods] == 'yes':
            # testing going with trend occurence
                if methods[stage_dict[methods]] % 2 == 1:
                    if result == 'W':
                        counter_dict[methods] = 0
                    if result == 'L':
                        counter_dict[methods] += 1
                        stage_dict[methods] += 1
                    if result == 'D':
                        if counter_dict[methods] == 0:
                            counter_dict[methods] += 1
                            stage_dict[methods] += 1
                        elif counter_dict[methods] < 2.5:
                            counter_dict[methods] += 0.25
                            stage_dict[methods] +=1
                        
                    
                # testing going against trend occurence
                else:
                    if result == 'W':
                        counter_dict[methods] += 1
                        stage_dict[methods] += 1
                    if result == 'L':
                        counter_dict[methods] = 0
                    if result == 'D':
                        if counter_dict[methods] == 0:
                            counter_dict[methods] += 1
                            stage_dict[methods] += 1
                        elif counter_dict[methods] < 2.5:
                            counter_dict[methods] += 0.25
                            stage_dict[methods] +=1
        
    
    # df = pd.DataFrame({'Dates': days, instrument : pair})
    # df[instrument] = 1 
    # print(df.head())

    # dates_ml = pd.merge(dates_ml,df[['Dates',instrument]], on = 'Dates', how = 'left')

mystring = " ".join(map(str,methods))



try:
    if loss < lowest_loss:
        lowest_loss = loss
        best_combo = mystring
except:
    lowest_loss = loss
    best_combo = mystring
    




# dates_ml.to_csv('Results/method_losses' + str(methods) + '.csv')









                        
                    









