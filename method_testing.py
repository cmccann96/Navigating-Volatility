import pandas as pd
import numpy as np
from util import column_sum
import itertools

rn = [1,2,3,4,5,6,7,8,9,10]
methods_list = list(itertools.combinations(rn,5))
# 1 is follow trend and 0 is do the opposite

import csv

with open('methods.csv', 'w') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(methods_list)


results = pd.read_csv('result_list.csv')
instruments = pd.read_csv('test_optimum.txt')
dates_ml = pd.read_csv('Date_ML.csv')

instruments_list = instruments['PAIR'].to_list()

method_number = 0
print(instruments_list)
for methods in methods_list:
    method_number += 1
    loss = 0
    clear = 'yes'
    for instrument in instruments_list:
        
        results_list = results[instrument].to_list()
        
        previous_result = 'None'
        counter = 0
        stage = 0
        
        index = 0
        days = []
        pair = []

        for result in results_list:
            index += 1
            if stage == 5:
                stage = 0
            
            if counter >= 5:
                loss += 1
                counter = 0
            
        
                clear = 'no'

            
            if result == 'W':
                if methods[stage] % 2 == 1:
                    clear = 'yes'
            if result == 'L':
                if methods[stage] % 2 == 0:
                    clear = 'yes'

            if clear == 'yes':
            # testing going with trend occurence
                if methods[stage] % 2 == 1:
                    if result == 'W':
                        counter = 0
                    if result == 'L':
                        counter += 1
                        stage += 1
                    if result == 'D':
                        if counter == 0:
                            counter += 1
                            stage += 1
                        elif counter < 2.5:
                            counter += 0.25
                            stage +=1
                        
                    
                # testing going against trend occurence
                else:
                    if result == 'W':
                        counter += 1
                        stage += 1
                    if result == 'L':
                        counter = 0
                    if result == 'D':
                        if counter == 0:
                            counter += 1
                            stage += 1
                        elif counter < 2.5:
                            counter += 0.25
                            stage +=1

    mystring = " ".join(map(str,methods))


   
    try:
        if loss < lowest_loss:
            lowest_loss = loss
            best_combo = mystring
    except:
        lowest_loss = loss
        best_combo = mystring
        
print(lowest_loss)
print(best_combo)









                        
                    









