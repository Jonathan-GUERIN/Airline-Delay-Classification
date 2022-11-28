import numpy as np
import pandas as pd


raw_data2018 = pd.read_csv('C:/Users/jonathan/Documents/Telecom 2A/SD201/Projet/Combined_Flights_2018.csv')
print("2018")
raw_data2019 = pd.read_csv('C:/Users/jonathan/Documents/Telecom 2A/SD201/Projet/Combined_Flights_2019.csv')
print("2019")
raw_data2020 = pd.read_csv('C:/Users/jonathan/Documents/Telecom 2A/SD201/Projet/Combined_Flights_2020.csv')
print("2020")
raw_data2021 = pd.read_csv('C:/Users/jonathan/Documents/Telecom 2A/SD201/Projet/Combined_Flights_2021.csv')
print("2021")
raw_data2022 = pd.read_csv('C:/Users/jonathan/Documents/Telecom 2A/SD201/Projet/Combined_Flights_2022.csv')
print("2022")


raw_data = pd.DataFrame()

raw_data = raw_data2018
raw_data = raw_data.append(raw_data2019)
print("2019")
raw_data = raw_data.append(raw_data2020)
print("2020")
raw_data = raw_data.append(raw_data2021)
print("2021")
raw_data = raw_data.append(raw_data2022)
print("2022")


data = pd.DataFrame()


data['Date'] = raw_data['FlightDate']       #ajouter le numero de vol ?
data['Airline'] = raw_data['Airline']
data['Origin'] = raw_data['Origin']
data['Destination'] = raw_data['Dest']
data['Cancelled'] = raw_data['Cancelled']
data['CRSDepTime'] = raw_data['CRSDepTime']
data['DepTime'] = raw_data['DepTime']
data['DepDelay'] = raw_data['DepDelayMinutes']      #Si on prend la colonne DepDelay on a des delays négatifs ce qui nous intéresse pas
data['ArrTime'] = raw_data['ArrTime']
data['ArrDelay'] = raw_data['ArrDelayMinutes']  
data['AirTime'] = raw_data['AirTime'] 

data['CRSElapsedTime'] = raw_data['CRSElapsedTime']
data['ActualElapsedTime'] = raw_data['ActualElapsedTime'] 

data['Distance'] = raw_data['Distance'] 
data['DayOfWeek'] = raw_data['DayOfWeek'] 
data['Operating_Airline'] = raw_data['Operating_Airline'] 
data['Tail_Number'] = raw_data['Tail_Number'] 
data['FlightNumber'] = raw_data['Flight_Number_Operating_Airline']
data['OriginAirportID'] = raw_data['Operating_Airline'] 
data['OriginCityName'] = raw_data['OriginCityName'] 
data['OriginStateName'] = raw_data['OriginStateName'] 
data['DestAirportID'] = raw_data['DestAirportID'] 
data['DestCityName'] = raw_data['DestCityName'] 
data['DestStateName'] = raw_data['DestStateName'] 
data['DepDel15'] = raw_data['DepDel15'] 
data['DepartureDelayGroups'] = raw_data['DepartureDelayGroups'] 
data['DepTimeBlk'] = raw_data['DepTimeBlk'] 
data['CRSArrTime'] = raw_data['CRSArrTime'] 
data['ArrDel15'] = raw_data['ArrDel15'] 
data['ArrivalDelayGroups'] = raw_data['ArrivalDelayGroups'] 
data['ArrTimeBlk'] = raw_data['ArrTimeBlk'] 
data['DistanceGroup'] = raw_data['DistanceGroup'] 



print("Indexes")

airlines = ['Endeavor Air Inc.', 'Delta Air Lines Inc.', 'Southwest Airlines Co.', 'Alaska Airlines Inc.', 'Hawaiian Airlines Inc.', 'SkyWest Airlines Inc.', 'Comair Inc.', 'Spirit Air Lines']

indexToDrop = data[(~data['Airline'].isin(airlines))].index

print("Indexes Finished")

cleaned_data = data[~data.index.isin(indexToDrop)].copy()  
print("cleaned")
cleaned_data.reset_index(inplace=True)     #reset les index pour qu'ils correspondent

data = cleaned_data
#Coder les classes de 5 minutes
print("Creating 5 minutes class")
def seach_depClass(row):
    if data['DepDelay'] == 0:
        val = 0
    elif data['DepDelay'] < 0:
        val = 0
    elif data['DepDelay'] > 0 and data['DepDelay'] < 5:
        val = 1
    elif data['DepDelay'] > 5 and data['DepDelay'] < 10:
        val = 2
    elif data['DepDelay'] > 10 and data['DepDelay'] < 15:
        val = 3
    elif data['DepDelay'] > 15 and data['DepDelay'] < 20:
        val = 4
    elif data['DepDelay'] > 20:
        val = 5
    return val

#data['DepDelayClass'] = data.apply(f, axis=1)
"""
data['DepDelayClass'] = np.where(
    data['DepDelay'] == 0 , 0, np.where(
    data['DepDelay'] < 0, 0, np.where(
    data['DepDelay'] > 0 & data['DepDelay'] < 5, 1, np.where(
    data['DepDelay'] >= 5 & data['DepDelay'] < 10, 2, np.where(
    data['DepDelay'] >= 10 & data['DepDelay'] < 15, 3, np.where(
    data['DepDelay'] >= 15 & data['DepDelay'] < 20, 4, 5))))))
"""
print("If problem occurs here, refer to line 112: creation 5 minutes class np.select isn't valid")
column = 'DepDelay'
conditions = [data['DepDelay'] == 0,
              data['DepDelay'] < 0,
              (data['DepDelay'] > 0) & (data['DepDelay'] < 5),
              (data['DepDelay'] >= 5) & (data['DepDelay'] < 10),
              (data['DepDelay'] >= 10) & (data['DepDelay'] < 15),
              (data['DepDelay'] >= 15) & (data['DepDelay'] < 20),
              (data['DepDelay'] >= 20)]
choices     = [0,0,1,2,3,4,5]
    
data["DepDelayClass"] = np.select(conditions, choices, default=np.nan)

#rslt_df = dataframe[(dataframe['Age'] == 21) & dataframe['Stream'].isin(options)]

#Replace NaN by -1
print("Replacing NaN by -1, line 128")
data.fillna(-1)

#Coder le data balance
#Count Cancelled
#1er data balance sur si annulé ou pas
print("Making balance_cancelled")
number_cancelled = data[(data['Cancelled'] == True)].count()
number_maintained = data[(data['Cancelled'] == False)].count()

small = min(number_cancelled,number_maintained)
if small > 50000:
    fraction = 50000/small
    
    data_cancelled = data[(data['Cancelled'] == True)]
    data_maintained = data[(data['Cancelled'] == False)]
    
    cancelled_proportion = 50000/number_cancelled
    maintained_proportion = 50000/number_maintained
    data_cancelled = data_cancelled.sample(frac=cancelled_proportion).reset_index(drop=True)
    data_maintained = data_maintained.sample(frac=data_maintained).reset_index(drop=True)
    
    balance_cancelled = pd.DataFrame()
    balance_cancelled = data_cancelled
    balance_cancelled = balance_cancelled.append(data_maintained)
    np.random.seed(1)
    balance_cancelled = balance_cancelled.sample(frac=1).reset_index(drop=True)
else:
    data_cancelled = data[(data['Cancelled'] == True)]
    data_maintained = data[(data['Cancelled'] == False)]
    
    if number_cancelled < number_maintained:
        proportion = number_cancelled/number_maintained
        data_cancelled = data_cancelled.sample(frac=1).reset_index(drop=True)
        data_maintained = data_maintained.sample(frac=proportion).reset_index(drop=True)
    else:
        proportion = number_maintained/number_cancelled
        data_cancelled = data_cancelled.sample(frac=proportion).reset_index(drop=True)
        data_maintained = data_maintained.sample(frac=1).reset_index(drop=True)
    
    balance_cancelled = pd.DataFrame()
    balance_cancelled = data_cancelled
    balance_cancelled = balance_cancelled.append(data_maintained)
    np.random.seed(1)
    balance_cancelled = balance_cancelled.sample(frac=1).reset_index(drop=True)
    
print("Finished balance_cancelled, begin registering balance_cancelled")
balance_cancelled.drop(columns=['level_0', 'index'], inplace=True)
balance_cancelled.to_csv('balance_cancelled.csv')



#2eme data balance sur les classes de retard
print("Making balance_DepDelayClass")
number_class0 = data[(data['DepDelayClass'] == 0)].count()
number_class1 = data[(data['DepDelayClass'] == 1)].count()
number_class2 = data[(data['DepDelayClass'] == 2)].count()
number_class3 = data[(data['DepDelayClass'] == 3)].count()
number_class4 = data[(data['DepDelayClass'] == 4)].count()
number_class5 = data[(data['DepDelayClass'] == 5)].count()

small = min(number_class0, number_class1, number_class2, number_class3, number_class4, number_class5)
if small > 30000:
    fraction = 30000/small
    
    data_class0 = data[(data['DepDelayClass'] == 0)]
    data_class1 = data[(data['DepDelayClass'] == 1)]
    data_class2 = data[(data['DepDelayClass'] == 2)]
    data_class3 = data[(data['DepDelayClass'] == 3)]
    data_class4 = data[(data['DepDelayClass'] == 4)]
    data_class5 = data[(data['DepDelayClass'] == 5)]
    
    class0_proportion = 30000/number_class0
    class1_proportion = 30000/number_class1
    class2_proportion = 30000/number_class2
    class3_proportion = 30000/number_class3
    class4_proportion = 30000/number_class4
    class5_proportion = 30000/number_class5
    data_class0 = data_class0.sample(frac=class0_proportion).reset_index(drop=True)
    data_class1 = data_class1.sample(frac=class1_proportion).reset_index(drop=True)
    data_class2 = data_class2.sample(frac=class2_proportion).reset_index(drop=True)
    data_class3 = data_class3.sample(frac=class3_proportion).reset_index(drop=True)
    data_class4 = data_class4.sample(frac=class4_proportion).reset_index(drop=True)
    data_class5 = data_class5.sample(frac=class5_proportion).reset_index(drop=True)
    
    balance_depDelayClass = pd.DataFrame()
    balance_depDelayClass = data_class0
    balance_depDelayClass = balance_depDelayClass.append(data_class1)
    balance_depDelayClass = balance_depDelayClass.append(data_class2)
    balance_depDelayClass = balance_depDelayClass.append(data_class3)
    balance_depDelayClass = balance_depDelayClass.append(data_class4)
    balance_depDelayClass = balance_depDelayClass.append(data_class5)
    np.random.seed(1)
    balance_depDelayClass = balance_depDelayClass.sample(frac=1).reset_index(drop=True)
elif small < 30000 and small > 20000:
    fraction = 20000/small
    
    data_class0 = data[(data['DepDelayClass'] == 0)]
    data_class1 = data[(data['DepDelayClass'] == 1)]
    data_class2 = data[(data['DepDelayClass'] == 2)]
    data_class3 = data[(data['DepDelayClass'] == 3)]
    data_class4 = data[(data['DepDelayClass'] == 4)]
    data_class5 = data[(data['DepDelayClass'] == 5)]
    
    class0_proportion = 20000/number_class0
    class1_proportion = 20000/number_class1
    class2_proportion = 20000/number_class2
    class3_proportion = 20000/number_class3
    class4_proportion = 20000/number_class4
    class5_proportion = 20000/number_class5
    data_class0 = data_class0.sample(frac=class0_proportion).reset_index(drop=True)
    data_class1 = data_class1.sample(frac=class1_proportion).reset_index(drop=True)
    data_class2 = data_class2.sample(frac=class2_proportion).reset_index(drop=True)
    data_class3 = data_class3.sample(frac=class3_proportion).reset_index(drop=True)
    data_class4 = data_class4.sample(frac=class4_proportion).reset_index(drop=True)
    data_class5 = data_class5.sample(frac=class5_proportion).reset_index(drop=True)
    
    balance_depDelayClass = pd.DataFrame()
    balance_depDelayClass = data_class0
    balance_depDelayClass = balance_depDelayClass.append(data_class1)
    balance_depDelayClass = balance_depDelayClass.append(data_class2)
    balance_depDelayClass = balance_depDelayClass.append(data_class3)
    balance_depDelayClass = balance_depDelayClass.append(data_class4)
    balance_depDelayClass = balance_depDelayClass.append(data_class5)
    np.random.seed(1)
    balance_depDelayClass = balance_depDelayClass.sample(frac=1).reset_index(drop=True)
elif small < 20000 and small > 10000:
    fraction = 10000/small
    
    data_class0 = data[(data['DepDelayClass'] == 0)]
    data_class1 = data[(data['DepDelayClass'] == 1)]
    data_class2 = data[(data['DepDelayClass'] == 2)]
    data_class3 = data[(data['DepDelayClass'] == 3)]
    data_class4 = data[(data['DepDelayClass'] == 4)]
    data_class5 = data[(data['DepDelayClass'] == 5)]
    
    class0_proportion = 10000/number_class0
    class1_proportion = 10000/number_class1
    class2_proportion = 10000/number_class2
    class3_proportion = 10000/number_class3
    class4_proportion = 10000/number_class4
    class5_proportion = 10000/number_class5
    data_class0 = data_class0.sample(frac=class0_proportion).reset_index(drop=True)
    data_class1 = data_class1.sample(frac=class1_proportion).reset_index(drop=True)
    data_class2 = data_class2.sample(frac=class2_proportion).reset_index(drop=True)
    data_class3 = data_class3.sample(frac=class3_proportion).reset_index(drop=True)
    data_class4 = data_class4.sample(frac=class4_proportion).reset_index(drop=True)
    data_class5 = data_class5.sample(frac=class5_proportion).reset_index(drop=True)
    
    balance_depDelayClass = pd.DataFrame()
    balance_depDelayClass = data_class0
    balance_depDelayClass = balance_depDelayClass.append(data_class1)
    balance_depDelayClass = balance_depDelayClass.append(data_class2)
    balance_depDelayClass = balance_depDelayClass.append(data_class3)
    balance_depDelayClass = balance_depDelayClass.append(data_class4)
    balance_depDelayClass = balance_depDelayClass.append(data_class5)
    np.random.seed(1)
    balance_depDelayClass = balance_depDelayClass.sample(frac=1).reset_index(drop=True)
else:
    data_class0 = data[(data['DepDelayClass'] == 0)]
    data_class1 = data[(data['DepDelayClass'] == 1)]
    data_class2 = data[(data['DepDelayClass'] == 2)]
    data_class3 = data[(data['DepDelayClass'] == 3)]
    data_class4 = data[(data['DepDelayClass'] == 4)]
    data_class5 = data[(data['DepDelayClass'] == 5)]
    
    if small == number_class0:
        proportion_class0 = 1
        proportion_class1 = number_class0/number_class1
        proportion_class2 = number_class0/number_class2
        proportion_class3 = number_class0/number_class3
        proportion_class4 = number_class0/number_class4
        proportion_class5 = number_class0/number_class5
        data_class0 = data_class0.sample(frac=proportion_class0).reset_index(drop=True)
        data_class1 = data_class1.sample(frac=proportion_class1).reset_index(drop=True)
        data_class2 = data_class2.sample(frac=proportion_class2).reset_index(drop=True)
        data_class3 = data_class3.sample(frac=proportion_class3).reset_index(drop=True)
        data_class4 = data_class4.sample(frac=proportion_class4).reset_index(drop=True)
        data_class5 = data_class5.sample(frac=proportion_class5).reset_index(drop=True)
    elif small == number_class1:
        proportion_class0 = number_class1/number_class0
        proportion_class1 = 1
        proportion_class2 = number_class1/number_class2
        proportion_class3 = number_class1/number_class3
        proportion_class4 = number_class1/number_class4
        proportion_class5 = number_class1/number_class5
        data_class0 = data_class0.sample(frac=proportion_class0).reset_index(drop=True)
        data_class1 = data_class1.sample(frac=proportion_class1).reset_index(drop=True)
        data_class2 = data_class2.sample(frac=proportion_class2).reset_index(drop=True)
        data_class3 = data_class3.sample(frac=proportion_class3).reset_index(drop=True)
        data_class4 = data_class4.sample(frac=proportion_class4).reset_index(drop=True)
        data_class5 = data_class5.sample(frac=proportion_class5).reset_index(drop=True)
    elif small == number_class2:
        proportion_class0 = number_class2/number_class0
        proportion_class1 = number_class2/number_class1
        proportion_class2 = 1
        proportion_class3 = number_class2/number_class3
        proportion_class4 = number_class2/number_class4
        proportion_class5 = number_class2/number_class5
        data_class0 = data_class0.sample(frac=proportion_class0).reset_index(drop=True)
        data_class1 = data_class1.sample(frac=proportion_class1).reset_index(drop=True)
        data_class2 = data_class2.sample(frac=proportion_class2).reset_index(drop=True)
        data_class3 = data_class3.sample(frac=proportion_class3).reset_index(drop=True)
        data_class4 = data_class4.sample(frac=proportion_class4).reset_index(drop=True)
        data_class5 = data_class5.sample(frac=proportion_class5).reset_index(drop=True)
    elif small == number_class3:
        proportion_class0 = number_class3/number_class0
        proportion_class1 = number_class3/number_class1
        proportion_class2 = number_class3/number_class2
        proportion_class3 = 1
        proportion_class4 = number_class3/number_class4
        proportion_class5 = number_class3/number_class5
        data_class0 = data_class0.sample(frac=proportion_class0).reset_index(drop=True)
        data_class1 = data_class1.sample(frac=proportion_class1).reset_index(drop=True)
        data_class2 = data_class2.sample(frac=proportion_class2).reset_index(drop=True)
        data_class3 = data_class3.sample(frac=proportion_class3).reset_index(drop=True)
        data_class4 = data_class4.sample(frac=proportion_class4).reset_index(drop=True)
        data_class5 = data_class5.sample(frac=proportion_class5).reset_index(drop=True)
    elif small == number_class4:
        proportion_class0 = number_class4/number_class0
        proportion_class1 = number_class4/number_class1
        proportion_class2 = number_class4/number_class2
        proportion_class3 = number_class4/number_class3
        proportion_class4 = 1
        proportion_class5 = number_class4/number_class5
        data_class0 = data_class0.sample(frac=proportion_class0).reset_index(drop=True)
        data_class1 = data_class1.sample(frac=proportion_class1).reset_index(drop=True)
        data_class2 = data_class2.sample(frac=proportion_class2).reset_index(drop=True)
        data_class3 = data_class3.sample(frac=proportion_class3).reset_index(drop=True)
        data_class4 = data_class4.sample(frac=proportion_class4).reset_index(drop=True)
        data_class5 = data_class5.sample(frac=proportion_class5).reset_index(drop=True)
    elif small == number_class5:
        proportion_class0 = number_class5/number_class0
        proportion_class1 = number_class5/number_class1
        proportion_class2 = number_class5/number_class2
        proportion_class3 = number_class5/number_class3
        proportion_class4 = number_class5/number_class4
        proportion_class5 = 1
        data_class0 = data_class0.sample(frac=proportion_class0).reset_index(drop=True)
        data_class1 = data_class1.sample(frac=proportion_class1).reset_index(drop=True)
        data_class2 = data_class2.sample(frac=proportion_class2).reset_index(drop=True)
        data_class3 = data_class3.sample(frac=proportion_class3).reset_index(drop=True)
        data_class4 = data_class4.sample(frac=proportion_class4).reset_index(drop=True)
        data_class5 = data_class5.sample(frac=proportion_class5).reset_index(drop=True)
    
    balance_depDelayClass = pd.DataFrame()
    balance_depDelayClass = data_class0
    balance_depDelayClass = balance_depDelayClass.append(data_class1)
    balance_depDelayClass = balance_depDelayClass.append(data_class2)
    balance_depDelayClass = balance_depDelayClass.append(data_class3)
    balance_depDelayClass = balance_depDelayClass.append(data_class4)
    balance_depDelayClass = balance_depDelayClass.append(data_class5)
    np.random.seed(1)
    balance_depDelayClass = balance_depDelayClass.sample(frac=1).reset_index(drop=True)

print("Finished balance_depDelayClass, begin registering balance_depDelayClass")
balance_depDelayClass.drop(columns=['level_0', 'index'], inplace=True)
balance_depDelayClass.to_csv('balance_depDelayClass.csv')


print("Finished Registering balance_depDelayClass, can now interrupt, rest is optionnal")
#cleaned_data.drop(columns='Cancelled', inplace=True)
#cleaned_data.dropna()
#cleaned_data = cleaned_data.fillna(0)
# cleaned_data.drop(columns='index', inplace= True)

#nonulldata = cleaned_data.copy()
#nonulldata.dropna()
#fillnulldata = cleaned_data.fillna(0)

np.random.seed(1)
l = cleaned_data.shape[0]
if l>100000:
    remove_n = cleaned_data.shape[0] - 100000
elif l > 80000 and l < 100000:
    remove_n = cleaned_data.shape[0] - 80000
elif l > 60000 and l < 80000:
    remove_n = cleaned_data.shape[0] - 60000
elif l > 30000 and l < 40000:
    remove_n = cleaned_data.shape[0] - 30000
elif l > 20000 and l < 30000:
    remove_n = cleaned_data.shape[0] - 20000
elif l > 10000 and l < 20000:
    remove_n = cleaned_data.shape[0] - 10000
else:
    remove_n = 0
    
drop_indices = np.random.choice(cleaned_data.index, remove_n, replace=False)
shuffled_data = cleaned_data.drop(drop_indices)

shuffled_data.reset_index(inplace=True)     #reset les index pour qu'ils correspondent

shuffled_data.drop(columns=['level_0', 'index'], inplace=True)
print("To csv")
shuffled_data.to_csv('shuffled_data3.csv')




 