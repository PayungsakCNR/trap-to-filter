import datetime
import re
import string
import sys
import Filterx
import time
#from influxdb import InfluxDBClient

def replaceMultiple(mainString, toBeReplaces, newString):
    # Iterate over the strings to be replaced
    for elem in toBeReplaces :
        # Check if string is in the main string
        if elem in mainString :
            # Replace the string
            mainString = mainString.replace(elem, newString)

    return  mainString

def main():
    running = True
    now = datetime.datetime.now()
    strnow = now.strftime("%X") #current time
    #log file date
    fileDate = now.strftime("%d-%b-%Y")
    fileName = "trapd-" + fileDate + ".log"
    output = open('/home/bass/receive/' + fileName, 'a')
    readfile = open('/home/bass/receive/' + fileName, 'r')
#
#    dbClient = InfluxDBClient('localhost', 8086, 'sabaszx', 'admin', 'trapEvent', ssl=False, verify_ssl=False)
#    dbClient.create_database('trapEvent')

    #print('Database created, go check in shell')

#    dbClient.switch_database('trapEvent')
    known_ssid_list = ["PSU WiFi 802.1x","PSU WiFi 5GHz","TrueMove H","CoEIoT","CoEWiFi"]

    while running:
        try:
            raw_input = input()
            filtered = raw_input.replace("<UNKNOWN>","" )
            showDate = filtered.replace("UDP: [172.30.232.2]:32768->[172.30.232.250]:162", strnow)

            #filter out lookoup from Filterx  module 
            wrongtypeRemove = replaceMultiple(showDate, Filterx.wronglist, '')
            timestamp = wrongtypeRemove.replace("DISMAN-EVENT-MIB::", "")
            hideMIB = replaceMultiple(timestamp, Filterx.mibList, '')
            event = hideMIB.replace("snmpTrapOID","Event")
            prefixRemove = replaceMultiple(event, Filterx.prefixList, '')
            weirdRemove = replaceMultiple(prefixRemove, Filterx.weirdList, ' ')
            bad_chars = "/\\!$^&*|'({)[}>_<]~+=#$%;`@?"

            outstr  = replaceMultiple(weirdRemove,bad_chars,'')
            #outstr - write log files into local server
            result = replaceMultiple(outstr,Filterx.bad_list,' ')
            #write to local
            output.write(result + '\n')

           
        except EOFError:
            running = False
    output.close()

if __name__ == '__main__':
    main()
