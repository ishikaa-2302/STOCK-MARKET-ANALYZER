# importing the required libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import pandas as pd

# importing the dataset
dataset=pd.read_csv("data.csv",index_col="Date",parse_dates=True)

dataset.head()
dataset.isna().any()
dataset.info()
dataset['Open'].plot(figsize=(16,6))
#convert column "a" of a Dataframe
#dataset['Close'] = dataset['Close'].str.replace(',',' ').astype(float)

#dataset["Volume"]=dataset["Volume"].str.replace(',','').astype(float)
# 7 day rolling mean
dataset.rolling(7).mean().head(20)

dataset['Open'].plot(figsize=(16,6))
dataset.rolling(window=30).mean()['Close'].plot()
#dataset['Close : 30 Day Mean '] =dataset['Close'].rolling(window=30).mean()
#dataset[['Close','Close: 30 Day Mean']].plot(figsize=(16,6))
# Optional Specify a minimum number of periods
dataset['Close'].expanding(min_periods=1).mean().plot(figsize=(16,6))
training_set=dataset['Open']
training_set=pd.DataFrame(training_set)
#Data cleaning
dataset.isna().any()
# Feature Scaling
from sklearn.preprocessing import MinMaxScaler
sc=MinMaxScaler(feature_range=(0,1))
training_set_scaled = sc.fit_transform(training_set)
# Crearting a datastructure with 60 timesteps and 1 output
X_train=[]
y_train=[]
for i in range(60,1225):
    X_train.append(training_set_scaled[i-60:i, 0])
    y_train.append(training_set_scaled[i, 0])
X_train, y_train = np.array(X_train),np.array(y_train)
# Reshaping
X_train=np.reshape(X_train,(X_train.shape[0],X_train.shape[1],1))
# PART 2 -Building the RNN
# Importing the Keras libraries and packages
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
# Initialising the RNN
regressor=Sequential()
# Adding the first LSTM layer and some dropout regularisation
regressor.add(LSTM(units= 50, return_sequences=True,input_shape=(x_train.shape[1]) ))
regressor.add(Dropout(0,2))
# Adding a second LSTM layer and some Dropout regularisation
regressor.add(LSTM(units=50 , return_sequences=True))
regressor.add(Dropout(0,2))
# Adding a third LSTM layer and some Dropout regularisation
regressor.add(LSTM(units=50 , return_sequences =True))
regressor.add(Dropout(0,2))
# Adding fourth LSTM layer and some dropout reagularisation
regressor.add(LSTM(units=50))
regressor.add(Dropout(0,2))
# Adding the first LSTM layer and some dropout regularisation
regressor.add(LSTM(units= 50, return_sequences=True,input_shape=(x_train.shape[1]) ))
regressor.add(Dropout(0,2))
# Adding a second LSTM layer and some Dropout regularisation
regressor.add(LSTM(units=50 , return_sequences=True))
regressor.add(Dropout(0,2))
# Adding a third LSTM layer and some Dropout regularisation
regressor.add(LSTM(units=50 , return_sequences =True))
regressor.add(Dropout(0,2))
# Adding fourth LSTM layer and some dropout reagularisation
regressor.add(LSTM(units=50))
regressor.add(Dropout(0,2))
# Adding the output layer
regressor.add(Dense(units = 1))
# Compiling the RNN
regressor.compile(optimizer = 'adam',loss='mean_squared_error')
#Fitting the RNN to the training set
regressor.fit(x_train,y_train,epochs=100,batch_size=32)
# Part 3 - Making the predictions and visualising the results
#Getting the real stock price of 2017
dataset_test=pd.read_csv('data.csv',index_col="Date",parse_dates=True)
real_stock_price=dataset_test.iloc[:,1:2].values
dataset_test.head()
dataset_test.info()
dataset_test['Volume']=dataset_test['Volume'].str.replace(',','').astype(float)
test_set=dataset_test['Open']
test_set=pd.DataFrame(test_set)
test_set.info()
# Getting the predicted stock price
dataset_total=pd.contact((dataset['Open'],dataset_test['Open']),axis=0)
inputs=dataset_total[len(dataset_total)-len(dataset_test)-66:].values
inputs=inputs.reshape(-1,1)
inputs=sc.transform(inputs)
X_test=[]
for i in range(60,80):
    X_test.append(inputs[i-60:i,0])
X_test=np.array(X_test)
X_text=np.reshape(X_test,(X_test.shape[0],X_test.shape[1],1))
predicted_stock_price=regressor.predict(X_test)
predicted_stock_price=sc.inverse_transform(predicted_stock_price)
predicted_stock_price=pd.DataFrame(predicted_stock_price)
predicted_stock_price.info()
#Visualising the results
plt.plot(real_stock_price,color='red',label="Stock Price")
plt.plot(predicted_stock_price,color="blue",label="Predicted Stock Price")
plt.title("Stock price prediction")
plt.xlabel('Time')
plt.ylabel('Stock Prices')
plt.legend()
plt.show()
