#!/usr/bin/python

#NOTE: this requires pythoon 2.3 minumum

###
# To the extent possible under law, Red Hat, Inc. has dedicated all copyright to this software to the public domain worldwide, pursuant to the CC0 Public Domain Dedication. 
# This software is distributed without any warranty.  See <http://creativecommons.org/publicdomain/zero/1.0/>.
###


__author__ = "Felix Dewaleyne"
__credits__ = ["Felix Dewaleyne"]
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Felix Dewaleyne"
__email__ = "fdewaley@redhat.com"
__status__ = "prod"


import xmlrpclib, sys
#connection part
client = xmlrpclib.Server("https://rhn.redhat.com/rpc/api")
sys.stderr.write("enter your RHN login: ")
login = raw_input().strip()
password = getpass.getpass(prompt="enter your RHN Password: ")
sys.stderr.write("\n")
key = client.auth.login(login,password)
#remove the password from memory
del password

#fetch the data
print "Fetching the list of systems and the details for each of your system. This may take some time"
rhn_data={}
for system in client.system.listUserSystems(key):
    #gather the details for each system
    rhn_data[system['id']] = {'id': system['id'], 'last_checkin': system['last_checkin']}
    #add all the data from getDetails to this dictionary
    rhn_data[system['id']].update(client.system.getDetails(key,system['id']))
    #add all the network details as well
    rhn_data[system['id']].update(client.system.getNetwork(key,system['id']))

client.auth.logout()
#now write the csv file
print "Writing data to the csv file"
headers={'ID':'id' , 'Profile name':'profile_name', 'Hostname':'hostname', 'IP':'ip', 'Last checkin':'last_checkin', 'Base Entitlement': 'base_entitlement', 'Description': 'description', 'Adress 1': 'adress1','Adress 2':'adress2', 'City':'city', 'State': 'state', 'Country':'country', 'Building':'building', 'Room':'room', 'Rack':'rack'}
import csv
with open('systems_'+login+'.csv', 'wb' ) as csvfile:
    csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    csv_writer.writerow(headers.keys())
    for system in rhn_data:
        line = ()
        for value in headers:
            line.append(system.get(value))
        csv_writer.writerow(line)
        del line
del rhn_data