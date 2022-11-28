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
data['DepTime'] = raw_data['DepTime']
data['DepDelay'] = raw_data['DepDelayMinutes']      #Si on prend la colonne DepDelay on a des delays négatifs ce qui nous intéresse pas
data['ArrTime'] = raw_data['ArrTime']  
data['ArrDelay'] = raw_data['ArrDelayMinutes']  
data['AirTime'] = raw_data['AirTime'] 
data['Distance'] = raw_data['Distance'] 
data['FlightNumber'] = raw_data['Flight_Number_Operating_Airline']


print("Indexes")

airlines = ['Endeavor Air Inc.', 'Delta Air Lines Inc.', 'Southwest Airlines Co.', 'Alaska Airlines Inc.', 'Hawaiian Airlines Inc.', 'SkyWest Airlines Inc.', 'Comair Inc.', 'Spirit Air Lines']

indexToDrop = data[(data['Cancelled'] == True) | (~data['Airline'].isin(airlines))].index

print("Indexes Finished")

cleaned_data = data[~data.index.isin(indexToDrop)].copy()  
print("cleaned")
cleaned_data.reset_index(inplace=True)     #reset les index pour qu'ils correspondent

cleaned_data.drop(columns='Cancelled', inplace=True)
cleaned_data.dropna()
# cleaned_data.drop(columns='index', inplace= True)

np.random.seed(1)
remove_n = cleaned_data.shape[0] - 10000
drop_indices = np.random.choice(cleaned_data.index, remove_n, replace=False)
shuffled_data = cleaned_data.drop(drop_indices)

shuffled_data.reset_index(inplace=True)     #reset les index pour qu'ils correspondent

shuffled_data.drop(columns=['level_0', 'index'], inplace=True)
print("To csv")
shuffled_data.to_csv('shuffled_data2.csv')



 