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
for methods in methods_list:
    method_number += 1
    loss = 0
    clear = 'yes'

    try:
        del dates_ml
    except:
        pass

    dates_ml = pd.read_csv('Date_ML.csv')
    
    for instrument in instruments_list:
        day = []
        i = 0

        results_list = results[instrument].to_list()
        
        previous_result = 'None'
        counter = 0
        stage = 0
        
        index = 0
        days = []
        pair = []
        pair = []

        for result in results_list:
            i += 1
            index += 1
            if stage == 5:
                stage = 0
            
            if counter >= 5:
                loss += 1
                counter = 0
            
                days.append(results['Dates'].str[:10].iloc[i])
                pair.append(instrument)
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
        
        
        df = pd.DataFrame({'Dates': days, instrument : pair})
        df[instrument] = 1 
        

        dates_ml = pd.merge(dates_ml,df[['Dates',instrument]], on = 'Dates', how = 'left')

    mystring = " ".join(map(str,methods))


   
    try:
        if loss < lowest_loss:
            lowest_loss = loss
            best_combo = mystring
    except:
        lowest_loss = loss
        best_combo = mystring
        
        


    
                
    print(methods)
    print(loss)
    
    dates_ml.to_csv('Results/method_losses' + str(methods) + '.csv')









                        
                    









