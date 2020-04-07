import datetime
import time
import re
from influxdb import InfluxDBClient
import Filterx
#loggt file date
now = datetime.datetime.now()
strnow = now.strftime("%X") #current time

'''
Username and password for connect to InfluxDB , Please use Environment Variable.
'''

dbClient = InfluxDBClient('localhost', 8086, 'sabaszx', 'admin', 'trapEvent', ssl=False, verify_ssl=False)
dbClient.switch_database('trapEvent')

fileDate = now.strftime("%d-%b-%Y")
def replaceMultiple(mainString, toBeReplaces, newString):
    # Iterate over the strings to be replaced
    for elem in toBeReplaces :
        # Check if string is in the main string
        if elem in mainString :
            # Replace the string
            mainString = mainString.replace(elem, newString)
    return  mainString


#def readUPS():
#    with open('/var/log/client_logs/172.30.254.201/UPS.log',"r") as clientLog:
#        while True:
#            except EOFError:
#                break
#        print(clientLog.read())
#    clientLog.close()

def testRead():
    with open('/var/log/client_logs/syslog/snmptrapd.log','r') as test:
        while True:
            try:
                input_raw = test.read()
                if not input_raw:
                    time.sleep(1)

                filtered = input_raw.replace("<UNKNOWN>","" )
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
                print(result + '\n')
            except EOFError:
                break
    test.close()

if __name__ == '__main__':
    testRead()
#    readUPS()
