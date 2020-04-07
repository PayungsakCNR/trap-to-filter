from influxdb import InfluxDBClient

'''
Username and password for connect to InfluxDB , Please use Environment Variable.
'''
dbClient = InfluxDBClient('localhost', 8086, 'sabaszx', 'admin', 'trapEvent', ssl=False, verify_ssl=False)
dbClient.switch_database('trapEvent')

#Count number (NEW)
def countSSID(receive, ssid_name):
json_body = [{
                "measurement": "countSSID",
                "tags": {
                    "SSIDName": ssid_name,
                "type": "known_ssid"},
                "fields": {

                    "item": receive}
                    }
            ]
    dbClient.write_points(json_body)
'''
#count number
def countAIS(receive):
    json_body = [{
                "measurement": "countSSID",
                "tags": {
                    "SSIDName": "AIS Smart Login",
                "type": "known_ssid"},
                "fields": {

                    "item": receive}
                    }
                ]
    dbClient.write_points(json_body)
    
def count802(receive):
        json_body = [{
                "measurement": "countSSID",
                "tags": {
                    "SSIDName": "PSU Wifi 802.1x",
                "type": "known_ssid"},
                "fields": {
                    "item": receive}
                    }
                ]
        dbClient.write_points(json_body)

def countPSU5Ghz(receive):
            json_body = [{
                "measurement": "countSSID",
                "tags": {
                    "SSIDName": "PSU Wifi 5Ghz",
                "type": "known_ssid_number"},
                "fields": {
                    "item": receive}
                    }
                ] 
            dbClient.write_points(json_body)

def countTruemove(receive):
            json_body = [{
                "measurement": "countSSID",
                "tags": {
                    "SSIDName": "TrueMove H",
                "type": "known_ssid_number"},
                "fields": {
                    "item": receive}
                    }
                ]
            dbClient.write_points(json_body)

def countCoeIot(receive):
            json_body = [{
                "measurement": "countSSID",
                "tags": {
                    "SSIDName": "CoEIIoT",
                "type": "known_ssid_number"},
                "fields": {
                    "item": receive}
                    }
                ]
            dbClient.write_points(json_body)

def countCoeWifi(receive):
            json_body = [{
                "measurement": "countSSID",
                "tags": {
                    "SSIDName": "CoEWifi",
                "type": "known_ssid_number"},
                "fields": {
                    "item": receive}
                    }
                ]
            dbClient.write_points(json_body)

def countOthers(receive):
        json_body = [{
                "measurement": "countSSID",
                "tags": {
                    "SSIDName": "Unknown",
                "type": "unknown_ssid_number"},
                "fields": {
                    "item": receive}
                    }
                ]
        dbClient.write_points(json_body)
'''

#Count Percentage (NEW)
def countSSID_percentage(receive,percentage_SSID):
    json_body = [{
                "measurement": "percentage_SSID",
                "tags": {
                    "SSIDName": percentage_SSID,
                "type": "percentage"},
                "fields": {
                    "item": receive}
                    }
                ]
    dbClient.write_points(json_body)

'''
#Percentage
def countAIS_percentage(receive):
    json_body = [{
                "measurement": "percentage_SSID",
                "tags": {
                    "SSIDName": "percentage_AIS Smart Login",
                "type": "percentage"},
                "fields": {
                    "item": receive}
                    }
                ]
    dbClient.write_points(json_body)

def count802_percentage(receive):
        json_body = [{
                "measurement": "percentage_SSID",
                "tags": {
                    "SSIDName": "percentage_PSU Wifi 802.1x",
                "type": "percentage"},
                "fields": {
                    "item": receive}
                    }
                ]
        dbClient.write_points(json_body)

def countPSU5Ghz_percentage(receive):
            json_body = [{
                "measurement": "percentage_SSID",
                "tags": {
                    "SSIDName": "percentage_PSU Wifi 5Ghz",
                "type": "known_ssid_number"},
                "fields": {
                    "item": receive}
                    }
                ] 
            dbClient.write_points(json_body)

def countTruemove_percentage(receive):
            json_body = [{
                "measurement": "percentage_SSID",
                "tags": {
                    "SSIDName": "percentage_TrueMove H",
                "type": "known_ssid_number"},
                "fields": {
                    "item": receive}
                    }
                ]
            dbClient.write_points(json_body)

def countCoeIot_percentage(receive):
            json_body = [{
                "measurement": "percentage_SSID",
                "tags": {
                    "SSIDName": "percentage_CoEIIoT",
                "type": "known_ssid_number"},
                "fields": {
                    "item": receive}
                    }
                ]
            dbClient.write_points(json_body)

def countCoeWifi_percentage(receive):
            json_body = [{
                "measurement": "percentage_SSID",
                "tags": {
                    "SSIDName": "percentage_CoEWifi",
                "type": "known_ssid_number"},
                "fields": {
                    "item": receive}
                    }
                ]
            dbClient.write_points(json_body)
'''


#count users
def countClient(receive):
            json_body = [{
                "measurement": "number_of_client",
                "tags": {
                    "SSIDName": "number",
                "type": "number"},
                "fields": {
                    "item": receive}
                    }
                ]
            dbClient.write_points(json_body)