import requests, json
# fetching live location
apiKey = "b31bfd798d36eaad614e73ba309a11fe"

baseURL = "https://api.openweathermap.org/data/2.5/weather?q="

completeURL = baseURL + "Boston" + "&appid=" + apiKey

response = requests.get(completeURL)

data1 = response.json()
print(data1)

print("Current Temperature ",data1["main"]["temp"])
print("Maximum Temperature ",data1["main"]["temp_max"])
print("Minimum Temperature ",data1["main"]["temp_min"])
print("Current Pressure ",data1["main"]["pressure"])
print("Current Humidity ",data1["main"]["humidity"])
print("Current wind speed",data1["wind"]["speed"])