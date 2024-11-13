import pandas as pd
import numpy as np
from math import sqrt
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
import plotly.express as px
import data_clean as dc

from data_clean import data

def elbow_method(df, criteria):
  """
  Função que retorna o número ótimo de clusters para determinado dataframe.

  Input:
   - df: dataframe a ser utilizado na clusterização;
   - criteria: lista de critérios segundo a qual será feita a clusterização (e.g: ['Rating', 'Quantity'])

  Output: número ótimo de clusters

    """
  # Calculando os valores de inércia numericamente, dado um critério de parada de 0.01
  n = [2]
  inertia_values = []  # valores de inércia
  inertia_diff = []    # valores de diferenças de inércia
  while True:
    if n[-1] == 2:
      kmeans = KMeans(n_clusters = n[-1])
      kmeans.fit(df[criteria])
      inertia = kmeans.inertia_
      inertia_values.append(inertia)
      n.append(n[-1]+1)
    elif n[-1] > 2:
      kmeans = KMeans(n_clusters = n[-1])
      kmeans.fit(df[criteria])
      inertia = kmeans.inertia_
      inertia_values.append(inertia)
      inertia_diff.append(abs(inertia_values[-2] - inertia_values[-1]))
      if inertia_diff[-1] <= 1:
        break
      else:
        n.append(n[-1] + 1)
        continue
  # Encontrando a equação da reta associada ao primeiro e ao último pontos:
  x_0, y_0 = n[0], inertia_values[0]    # primeiro ponto do gráfico
  x_n, y_n = n[-1], inertia_values[-1]  # último ponto do gráfico

  m = (y_n - y_0)/(x_n-x_0)   # Coeficiente angular

  # Parâmetros da Reta
  C = -(y_0 + m*(-x_0))
  A = -m
  B = 1

  # Encontrando todos os pontos do gráfico
  points = list(zip(n, inertia_values))

  #Aplicando a fórmula da distância para TODOS os pontos de points:
  d = []
  for i in points:
    x_1, y_1 = i[0], i[1]
    d.append((abs(A*x_1 + B*y_1 + C)/(sqrt(A**2+B**2))))
  argmax = d.index(max(d))
  optimal_n = points[d.index(max(d))][0]
  return optimal_n

kmeans = KMeans(n_clusters = elbow_method(data, ['Total','Rating']))
kmeans.fit(data[['Total','Rating']])

df_labels = data.copy()

labels = kmeans.labels_

df_labels['Label'] = labels

fig_2 = px.scatter(
    df_labels,
    x = 'Rating',
    y = 'Total',
    color = 'Label',
    color_continuous_scale=px.colors.sequential.Turbo,
    title = 'Clusterização para Total e Rating'
)

# Consolidando informações sobre as labels
max_label = []
min_label = []
avg_label = []
std_label = []
label_ = []
n_clients = []
total_spent = []

for label in df_labels['Label'].unique():
  max_label.append(df_labels[df_labels['Label'] == label]['Total'].max())
  min_label.append(df_labels[df_labels['Label'] == label]['Total'].min())
  avg_label.append(df_labels[df_labels['Label'] == label]['Total'].mean())
  std_label.append(df_labels[df_labels['Label'] == label]['Total'].std())
  label_.append(label)
  n_clients.append(len(df_labels[df_labels['Label'] == label]))
  total_spent.append(df_labels[df_labels['Label']== label]['Total'].sum())

consolidatedinfo_label = pd.DataFrame(
    {
        'Label': label_,
        'Max': max_label,
        'Min': min_label,
        'Avg': avg_label,
        'Std': std_label,
        '# Clients': n_clients,
        'Total Spent': total_spent
    }
)

consolidatedinfo_label.sort_values(by = 'Total Spent',ascending = False, inplace = True)
consolidatedinfo_label.reset_index(drop = True, inplace = True)
consolidatedinfo_label['% Total Spent'] = consolidatedinfo_label['Total Spent'].cumsum()/consolidatedinfo_label['Total Spent'].sum()*100
consolidatedinfo_label['Accum Clients'] = consolidatedinfo_label['# Clients'].cumsum()

def consolidation_final():
  
  """
  data_num = dc.data.copy()

  # Label encoding
  data_num['City'] = LabelEncoder().fit_transform(data_num['City'])
  data_num['Customer type'] = LabelEncoder().fit_transform(data_num['Customer type'])
  data_num['Gender'] = LabelEncoder().fit_transform(data_num['Gender'])
  data_num['Product line'] = LabelEncoder().fit_transform(data_num['Product line'])
  data_num['Payment'] = LabelEncoder().fit_transform(data_num['Payment'])

  data_num['Day'] = data_num['Datetime'].dt.day
  data_num['Month'] = data_num['Datetime'].dt.month
  data_num = data_num.drop(['Date', 'Datetime'], axis = 1)

  # Identificar o número de clusters com o método do cotovelo
  sse = []

  for i in range(1, 11):
    kmeans = KMeans(n_clusters = i, random_state = 42)
    kmeans.fit(data_num)
    sse.append(kmeans.inertia_)

  # Aplicar o K-Means
  kmeans = KMeans(n_clusters = 4, random_state = 42)
  kmeans.fit(data_num)
  labels = kmeans.labels_
  data_num['Clusters'] = labels
  """

  # Import data
  data_num = pd.read_csv('output_file.csv')

  # Convert 'Date' and 'Datetime' to datetime type
  data_num['Date'] = pd.to_datetime(data_num['Date'])
  data_num['Datetime'] = pd.to_datetime(data_num['Datetime'])

  # Extract time features from 'Datetime'
  data_num['Hour'] = data_num['Datetime'].dt.hour  # Extract Hour
  data_num['Month'] = data_num['Datetime'].dt.month  # Extract Month
  data_num['Week'] = np.ceil(data_num['Datetime'].dt.day / 7).astype(int)  # Extract Week

  # Ensure 'gross income', 'Unit price', 'Rating', 'Total' are numeric
  data_num['gross income'] = data_num['gross income'].astype(str).str.replace(',', '.').astype(float)
  data_num['Unit price'] = data_num['Unit price'].astype(str).str.replace(',', '.').astype(float)
  data_num['Rating'] = data_num['Rating'].astype(str).str.replace(',', '.').astype(float)
  data_num['Total'] = data_num['Total'].astype(str).str.replace(',', '.').astype(float)

  # Drop the original 'Date' and 'Datetime' columns as they are not needed for clustering
  data_num = data_num.drop(['Date', 'Datetime'], axis=1)

  # Identify the number of clusters using the elbow method
  sse = []
  for i in range(1, 11):
      kmeans = KMeans(n_clusters=i, random_state=42)
      kmeans.fit(data_num)
      sse.append(kmeans.inertia_)

  # Apply K-Means clustering with 4 clusters
  kmeans = KMeans(n_clusters=4, random_state=42)
  kmeans.fit(data_num)
  labels = kmeans.labels_
  data_num['Clusters'] = labels

  # Plot the clustered data
  fig = px.scatter(data_num, x=data_num['Unit price'], y=data_num['Quantity'],
                  color='Clusters',
                  title='Clusters de K-Means',
                  color_discrete_sequence=px.colors.qualitative.Set1)

  fig.update_layout(
      xaxis_title='Preço unitário',
      yaxis_title='Quantidade comprada'
  )

  # Return or plot the figure
  return fig

