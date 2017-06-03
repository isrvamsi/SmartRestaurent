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
