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

#cleaned_data.drop(columns='Cancelled', inplace=True)
#cleaned_data.dropna()
#cleaned_data = cleaned_data.fillna(0)
# cleaned_data.drop(columns='index', inplace= True)

nonulldata = cleaned_data.copy()
nonulldata.dropna()
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


np.random.seed(1)
l = nonulldata.shape[0]
if l>60000:
    remove_n = nonulldata.shape[0] - 60000
elif l > 50000 and l < 60000:
    remove_n = nonulldata.shape[0] - 50000
elif l > 40000 and l < 50000:
    remove_n = nonulldata.shape[0] - 40000
elif l > 30000 and l < 40000:
    remove_n = nonulldata.shape[0] - 30000
elif l > 20000 and l < 30000:
    remove_n = nonulldata.shape[0] - 20000
elif l > 10000 and l < 20000:
    remove_n = nonulldata.shape[0] - 10000
else:
    remove_n = 0
    
drop_indices = np.random.choice(nonulldata.index, remove_n, replace=False)
shuffled_data = nonulldata.drop(drop_indices)

shuffled_data.reset_index(inplace=True)     #reset les index pour qu'ils correspondent

shuffled_data.drop(columns=['level_0', 'index'], inplace=True)
print("To csv")
shuffled_data.to_csv('nonullshuffled_data3.csv')


 