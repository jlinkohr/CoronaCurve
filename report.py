import pandas as pd 
import matplotlib.pyplot as plt 

dataFile = "coronaData.csv"

# read the data
data = pd.read_csv(dataFile)

total=data[['Date', 'Total']]

print (f"Totals:\n{total}")
plt.figure()
plt.show()

total.plot.bar()

print(data)

p = input()
