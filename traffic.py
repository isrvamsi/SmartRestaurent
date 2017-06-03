import urllib2
import json


# http://msdn.microsoft.com/en-us/library/hh441726.aspx
# get lat/lon data from http://itouchmap.com/latlong.html

# form a rectangle and get the traffic data within the rectangle

latN = str(33.725325)
latS = str(33.58748)
lonW = str( -117.867336)
lonE = str(-117.721213)

url = 'http://dev.virtualearth.net/REST/v1/Traffic/Incidents/'+latS+','+lonW+','+latN+','+lonE+'?key=Av6_H8GIYQyP-DLQwLOKDknW64QfmVgJmVpfiSO861v0x_j1pLPCOW6s-70nCzEW'
#url ='http://dev.virtualearth.net/REST/v1/Traffic/Incidents/37,-105,45,-94?key=Av6_H8GIYQyP-DLQwLOKDknW64QfmVgJmVpfiSO861v0x_j1pLPCOW6s-70nCzEW'

response = urllib2.urlopen(url).read()
data = json.loads(response.decode('utf8'))
resources = data['resourceSets'][0]['resources']
print '----------------------------------------------------'
count =0;
avgseverity=0;
for resourceItem in resources:
 description = resourceItem['description']
 severity = resourceItem['severity']
 avgseverity = avgseverity + severity
 count = count +1
 print description
 print severity
 print '----------------------------------------------------'

avgseverity = avgseverity/count
print "Avg Traffic severity  =" + str(avgseverity)


#weather 
'''

owm = pyowm.OWM('c6bdddd20f81d9097821a0885181481c')  # You MUST provide a valid API key

# Have a pro subscription? Then use:
# owm = pyowm.OWM(API_key='your-API-key', subscription_type='pro')

# Will it be sunny tomorrow at this time in Milan (Italy) ?
forecast = owm.daily_forecast("Milan,it")
tomorrow = pyowm.timeutils.tomorrow()
forecast.will_be_sunny_at(tomorrow)  # Always True in Italy, right? ;-)

# Search for current weather in London (UK)
observation = owm.weather_at_place('London,uk')
w = observation.get_weather()
print(w)                      # <Weather - reference time=2013-12-18 09:20,
                              # status=Clouds>

# Weather details
w.get_wind()                  # {'speed': 4.6, 'deg': 330}
w.get_humidity()              # 87
w.get_temperature('celsius')  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}

# Search current weather observations in the surroundings of
# lat=22.57W, lon=43.12S (Rio de Janeiro, BR)
observation_list = owm.weather_around_coords(-22.57, -43.12)
'''
