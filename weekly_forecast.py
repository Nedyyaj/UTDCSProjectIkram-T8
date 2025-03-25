import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
from scipy import interpolate
from sklearn.ensemble import RandomForestRegressor

class TemperatureModel:
    def __init__(self):
        self.tm    = 0
        self.tb    = 0
        self.a     = 0
        self.b     = 0
        self.epoch = '2000-01-01'
    def _date_to_DDOY(self, date_str, plus_days=0):
        date = pd.to_datetime(date_str) + pd.Timedelta(days=plus_days)
        D = (date - pd.to_datetime(self.epoch)).days
        DOY = date.day_of_year
        return D, DOY
    def _predict_t(self, day, tm, tb, a, b):
        w = 2*np.pi / 365.25
        return tb + tm*day + a*np.sin(w*day) + b*np.cos(w*day)
    def fit(self, X_days, Y_temps):
        reg, cov = curve_fit(self._predict_t, X_days, Y_temps)
        self.tm, self.tb, self.a, self.b = reg
        return cov
    def predict(self, date_str, plus_days=0):
        day, _ = self._date_to_DDOY(date_str, plus_days)
        w = 2*np.pi / 365.25
        t = self.tb + self.tm*day + self.a*np.sin(w*day) + self.b*np.cos(w*day)
        tp = self.tm + self.a*w*np.cos(w*day) - self.b*w*np.sin(w*day)
        return t, tp
    
class VolatilityModel:
    def __init__(self):
        self.daily_volatility = None
        self.epoch            = '2000-01-01'
    def _date_to_DDOY(self, date_str, plus_days=0):
        date = pd.to_datetime(date_str) + pd.Timedelta(days=plus_days)
        D = (date - pd.to_datetime(self.epoch)).days
        DOY = date.day_of_year
        return D, DOY
    def fit(self, X_days_of_year, Y_deviations):
        knot_numbers = 5
        x_new = np.linspace(0, 1, knot_numbers+2)[1:-1]
        q_knots = np.quantile(X_days_of_year, x_new)
        t, c, k = interpolate.splrep(X_days_of_year, Y_deviations, t=q_knots, s=1)
        spline = interpolate.BSpline(t, c, k)
        self.daily_volatility = spline(X_days_of_year)
        return np.cov(self.daily_volatility, Y_deviations)[0][1]
    def predict(self, date_str, plus_days=0):
        _, day_of_year = self._date_to_DDOY(date_str, plus_days)
        return self.daily_volatility[day_of_year - 1]

class NormalForecast:
    def __init__(self):
        self.temp_model = None
        self.vol_model  = None
        self.epoch      = '2000-01-01'
    def fit(self, station_df, target):
        temp_df = station_df[['Date', target]]
        temp_df['Date'] = pd.to_datetime(temp_df['Date'])

        reference_date = pd.to_datetime(self.epoch)
        temp_df['Days since epoch'] = (temp_df['Date'] - reference_date).dt.days
        temp_df['Day of year'] = temp_df['Date'].dt.day_of_year

        training_cutoff = 4000

        self.temp_model = TemperatureModel()
        t_cov = self.temp_model.fit(temp_df['Days since epoch'].iloc[:training_cutoff], temp_df[target].iloc[:training_cutoff])

        #print('Temperature model covariance with training data:', t_cov)

        volatility = temp_df.iloc[:training_cutoff].groupby(['Day of year'])[target].agg(['mean','std'])
        self.vol_model = VolatilityModel()
        v_cov = self.vol_model.fit(volatility['std'].index, volatility['std'].values)

        #print('Volatility model covariance with training data:', v_cov)
    def predict(self, date_str, plus_days=0):
        mean = self.temp_model.predict(date_str, plus_days)[0]
        std  = self.vol_model.predict(date_str, plus_days)
        return np.random.normal(mean, std)
    def forecast_weekly(self, beginning_date_str):
        forecast = []
        for i in range(7):
            daily = self.predict(beginning_date_str, plus_days=i)
            forecast.append(np.round(daily))
        return np.array(forecast)

class RandomForestForecast:
    def __init__(self):
        self.temp_model    = None
        self.regressor     = None
        self._n_estimators = 10000
        self.epoch         = '2000-01-01'
    def fit(self, station_df, target):
        temp_df = station_df[['Date', target]]
        temp_df['Date'] = pd.to_datetime(temp_df['Date'])

        reference_date = pd.to_datetime(self.epoch)
        temp_df['Days since epoch'] = (temp_df['Date'] - reference_date).dt.days
        temp_df['Day of year'] = temp_df['Date'].dt.day_of_year

        training_cutoff = 4000

        self.temp_model = TemperatureModel()
        t_cov = self.temp_model.fit(temp_df['Days since epoch'].iloc[:training_cutoff], temp_df[target].iloc[:training_cutoff])

        #print('Temperature model covariance with training data:', t_cov)

        modeling_df2 = temp_df.rename({'Days since epoch':'D', 'Day of year':'DOY', target: 'T'}, axis=1)
        modeling_df2['T_lag1'] = modeling_df2['T'].shift(1)
        modeling_df2['T_pred'] = modeling_df2['Date'].apply(lambda x: (self.temp_model.predict(x))[0])
        modeling_df2['T_pred_prime'] = modeling_df2['Date'].apply(lambda x: (self.temp_model.predict(x))[1])
        modeling_df2.set_index(modeling_df2['D'], inplace=True)

        self.regressor = RandomForestRegressor(n_estimators=self._n_estimators, max_depth=4, random_state=0)
        self.regressor.fit(modeling_df2[['T_lag1', 'T_pred', 'T_pred_prime']].loc[1000:training_cutoff], modeling_df2['T'].loc[1000:training_cutoff])

        score = self.regressor.score(modeling_df2[['T_lag1', 'T_pred', 'T_pred_prime']].loc[1000:training_cutoff], modeling_df2['T'].loc[1000:training_cutoff])

        #print('Random forest regressor covariance with training data:', score)
    def _get_next_day_temp_probs(self, starting_conditions):
        tree_predictions = [tree.predict(np.array(starting_conditions).reshape(1, -1))[0] for tree in self.regressor.estimators_]
        rounded = [round(x) for x in tree_predictions]
        prob_distribution_X = [x for x in range(120)]
        prob_distribution_Y = [rounded.count(x)/len(rounded) for x in prob_distribution_X]
        final = {x:y for x, y in zip(prob_distribution_X, prob_distribution_Y) if y > 0}
        return final
    def predict(self, from_temp, date_str, plus_days=0):
        t_pred, t_pred_prime = self.temp_model.predict(date_str, plus_days)
        starting_conditions = [from_temp, t_pred, t_pred_prime]
        next_day_temps = self._get_next_day_temp_probs(starting_conditions)
        return np.random.choice(list(next_day_temps.keys()), 1, p=list(next_day_temps.values()))[0]
    def forecast_weekly(self, beginning_date_str, starting_temp):
        forecast = [starting_temp]
        for i in range(7):
            daily = self.predict(forecast[-1], beginning_date_str, plus_days=i)
            forecast.append(np.round(daily))
        return np.array(forecast[1:])