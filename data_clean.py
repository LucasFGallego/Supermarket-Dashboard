import pandas as pd
import numpy as np

data = pd.read_csv('Dados brutos.csv')

data.drop(['Invoice ID','Branch','Tax 5%','cogs','gross margin percentage'], axis = 1, inplace = True)

data['Datetime'] = data['Date'] + ' ' + data['Time']

# Modificando os dados da coluna Date para datetime

data['Date'] = pd.to_datetime(data['Date'])
data['Datetime'] = pd.to_datetime(data['Datetime'])

# Fragmentando o tempo de acordo com Datetime
data['Datetime'] = pd.to_datetime(data['Datetime']) # Converte 'Datetime' para data
data['Hour'] = data['Datetime'].dt.hour # Adiciona coluna 'Hora'
data['Month'] = data['Datetime'].dt.month # Adiciona coluna 'Mês'
data['Week'] = np.ceil(data['Datetime'].dt.day / 7).astype(int)








