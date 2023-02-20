from fastapi import FastAPI
import pandas as pd

data = pd.read_csv('alltrails.csv')

# Convert _geoloc to latitude and longitude
data['latitude'] = data['_geoloc'].apply(lambda x: float(x.split(',')[0].split(':')[1]))
data['longitude'] = data['_geoloc'].apply(lambda x: float(x.split(',')[1].split(':')[1][:-1]))

app = FastAPI()
@app.get("/")
def test():
  return {"Server is running and ready for requests! Go to /nearby-trails for nearby trails or /all-trails for all trails."}

@app.get("/nearby-trails")
def nearby_trails(lat: float, long: float, radius: float, count: int = 10):
    data_with_distance = data.copy()
    data_with_distance['distance'] = ((data_with_distance['latitude'] - lat)**2 + (data_with_distance['longitude'] - long)**2)**0.5
    qualifying_trails = data_with_distance[data_with_distance['distance'] <= radius]
    qualifying_trails.sort_values(by=['distance'], inplace=True)
    qualifying_trails = qualifying_trails.head(count)
    return {qualifying_trails.to_csv()}

@app.get("/all-trails")
def all_trails():
    return {data.to_csv()}