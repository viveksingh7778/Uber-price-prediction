from flask import Flask, render_template, request
import pickle
import pandas as pd
from Weather import data1
import datetime
import pytz
import numpy as np

app = Flask(__name__,static_url_path='/static')

# Load the pre-trained machine learning models
with open("XGB_model.pkl", 'rb') as file:
    XGB_model = pickle.load(file)
with open("XGB_model_distance.pkl", 'rb') as file1:
    XGB_model_distance = pickle.load(file1)
with open("encoded_value.pkl", 'rb') as file2:
    encoded_value = pickle.load(file2)


def date_time():
    current_time = datetime.datetime.now(pytz.timezone('America/New_York'))
    return current_time

# label encoded values for html page droup down input mapping
class CustomData:
    def __init__(self, Current_Location: str, Destination: str, Car_type: str):
        location_mapping = {
            'Back Bay': 0,
            'Beacon Hill': 1,
            'Boston University': 2,
            'Fenway': 3,
            'Financial District': 4,
            'Haymarket Square': 5,
            'North End': 6,
            'North Station': 7,
            'Northeastern University': 8,
            'South Station': 9,
            'Theatre District': 10,
        }

        self.Current_Location = location_mapping.get(Current_Location, 11)
        self.Destination = location_mapping.get(Destination, 11)

        self.name = {
            'Black': 0,
            'Black SUV': 1,
            'UberPool': 2,
            'UberX': 3,
            'UberXL': 4,
        }
        self.Car_type = self.name.get(Car_type, 5)

    def get_data_as_data_frame(self):
        current_time = date_time()
        custom_data_input_dict = {
            "destination": [self.Destination],
            "source": [self.Current_Location],
            "name": [self.Car_type],
            "temp": [data1["main"]["temp"]-273],
            "location": [self.Current_Location],
            "pressure": [data1["main"]["pressure"]],
            "rain": [data1.get("rain", {}).get("1h", 0)],
            "humidity": [data1["main"]["humidity"]/100],
            "wind": [data1["wind"]["speed"]],
            "Wweek": [current_time.day % 7],
            "Whour": [current_time.hour]
        }

        return pd.DataFrame(custom_data_input_dict)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predictdata', methods=['POST'])
def predict_datapoint():
    data = CustomData(
        Current_Location=request.form.get('Current_Location'),
        Destination=request.form.get('Destination'),
        Car_type=request.form.get('Car_type'))
    pred_df1 = data.get_data_as_data_frame()
    pred_df2 = data.get_data_as_data_frame()

    pred_df1.drop(['name', 'temp', 'location', 'pressure', 'rain', 'humidity', 'wind', 'Wweek', 'Whour'],
                  axis=1, inplace=True)
    #model 1
    distance = XGB_model_distance.predict(pred_df1)[0]
    print(distance)
    # Create a DataFrame with the "distance" column
    distance_df = pd.DataFrame({'distance': [distance]})

    # Add the "distance" column to pred_df2 using the assign method
    pred_df3=pred_df2
    pred_df3.insert(0, 'distance', distance_df['distance'])
    print(pred_df3.columns)

    #model2
    predicted_price = round(XGB_model.predict(pred_df3)[0],2)

    return render_template('index.html', results=predicted_price)


if __name__ == "__main__":

    app.run(host="0.0.0.0",port=8000,debug=True)
