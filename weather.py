import pyowm

API_key = 'c6bdddd20f81d9097821a0885181481c'
owm = pyowm.OWM(API_key) 
latlong = (-0.107331, 51.503614)

def get_data():
	data = {}
	obs = owm.weather_at_coords(*latlong)
	w = obs.get_weather()
	data['temperature'] = w.get_temperature(unit='celsius')
	data['humidity'] = w.get_humidity()
	data['w_description'] = "Partly Cloudy"
	return data
