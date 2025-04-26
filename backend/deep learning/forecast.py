import numpy as np
import torch
import torch.optim as optim
import torch.utils.data as Data
import torch.nn as nn
import pandas as pd
import matplotlib.pyplot as plt
import csv

class Model(nn.Module):
    def __init__(self, io_size, hidden_size, num_layers):
        super().__init__()
        self.lstm = nn.LSTM(input_size=io_size, hidden_size=hidden_size, num_layers=num_layers, batch_first=True)
        self.linear = nn.Linear(hidden_size, io_size)
    def forward(self, x):
        x, _ = self.lstm(x)
        x = self.linear(x)
        return x

def create_dataset(dataset, lookback):
    X, y = [], []
    for i in range(len(dataset)-lookback):
        feature = dataset[i:i+lookback]
        target = dataset[i+1:i+lookback+1]
        X.append(feature)
        y.append(target)
    return torch.stack(X, dim=0), torch.stack(y, dim=0)

def train_model(obs_filepath, lookback, hidden_dim, epochs, train_pct):
    data = pd.read_csv(obs_filepath)
    data.insert(0, 'Day of Year', pd.to_datetime(data['Date']).dt.day_of_year)

    data = torch.from_numpy(data.drop('Date', axis=1).values).float()
    training_len = int(len(data) * train_pct)
    train, test = data[:training_len], data[training_len:]
    
    X_train, y_train = create_dataset(train, lookback=lookback)
    X_test, y_test = create_dataset(test, lookback=lookback)
    #print(X_train.shape, y_train.shape)
    #print(X_test.shape, y_test.shape)

    model = Model(len(train[0]), hidden_dim, 1)
    optimizer = optim.Adam(model.parameters())
    loss_fn = nn.MSELoss()
    loader = Data.DataLoader(Data.TensorDataset(X_train, y_train), shuffle=True, batch_size=8)
     
    n_epochs = epochs
    for epoch in range(n_epochs):
        model.train()
        for X_batch, y_batch in loader:
            y_pred = model(X_batch)
            loss = loss_fn(y_pred, y_batch)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        # Validation
        if epoch % 5 != 0:
            continue
        model.eval()
        with torch.no_grad():
            y_pred = model(X_train)
            train_rmse = np.sqrt(loss_fn(y_pred, y_train))
            y_pred = model(X_test)
            test_rmse = np.sqrt(loss_fn(y_pred, y_test))
        print("Epoch %d: train RMSE %.4f, test RMSE %.4f" % (epoch, train_rmse, test_rmse))

    model.eval()
    with torch.no_grad():
        y_pred = model(X_train)
        train_rmse = np.sqrt(loss_fn(y_pred, y_train))
        y_pred = model(X_test)
        test_rmse = np.sqrt(loss_fn(y_pred, y_test))
    print("Final model: train RMSE %.4f, test RMSE %.4f" % (train_rmse, test_rmse))

    return model

def generate_forecast(model, previous_observations, days_forward):
    steps_forward = 4 * days_forward
    previous = previous_observations

    day = previous_observations[-1][0]
    if day >= 365:
        day = 1
    else:
        day += 1
    hour = 6
    forecast = []
    with torch.no_grad():
        for i in range(steps_forward):
            pred = model(previous)
            pred = pred[-1:,:]
            
            pred[-1, 0] = day
            pred[-1, 1] = hour
            if hour == 24:
                if day == 365:
                    day = 1
                else:
                    day += 1
                hour = 6
            else:
                hour += 6

            forecast.append(pred[-1, :])
            previous = torch.cat((previous[1:, :], pred), dim=0)
    
    return torch.stack(forecast, dim=0).numpy()

def fetch_previous_observations(obs_filepath, from_date, to_date):
    data = pd.read_csv(obs_filepath)
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index(['Date', 'Hour'], inplace=True)
    data = data.loc[(from_date, 6):(to_date, 24)]
    data.reset_index(inplace=True)
    doy = pd.to_datetime(data['Date']).dt.day_of_year
    data.drop('Date', axis=1, inplace=True)
    data.insert(0, 'Day of Year', doy)
    data = torch.from_numpy(data.values).float()
    return data

def save_forecast(forecast_filepath, forecast, days_forecast, obs_filepath, first_date):
    with open(obs_filepath) as ff:
        reader = csv.reader(ff)
        cols = next(reader)
    
    df = pd.DataFrame(list(forecast), columns=(['Day of Year'] + cols[1:])).round(2)
    df[df < 0] = 0
    
    date = pd.to_datetime(first_date)
    dates = []
    for i in range(30):
        dates.extend([date, date, date, date])
        date += pd.Timedelta(days=1)
    
    df.insert(0, 'Date', pd.Series(dates))
    df.to_csv(forecast_filepath, index=False)

class Forecaster:
    def __init__(self, observation_filepath, forecast_filepath):
        self.model = None
        self.obs_filepath = observation_filepath
        self.days_lookback = 7
        self.lstm_hidden_dim = 60
        self.train_pct = 0.6
        self.epochs_to_train = 20
        self.forecast_filepath = forecast_filepath
    def train(self):
        self.model = train_model(self.obs_filepath, 4 * self.days_lookback, self.lstm_hidden_dim, self.epochs_to_train, self.train_pct)
    def generate(self, from_date, for_days=7):
        date = pd.to_datetime(from_date)
        start = date - pd.Timedelta(days=self.days_lookback)
        end = date - pd.Timedelta(days=1)
        previous = fetch_previous_observations(self.obs_filepath, start, end)
        forecast = generate_forecast(self.model, previous, for_days)
        save_forecast(self.forecast_filepath, forecast, for_days, self.obs_filepath, from_date)
        