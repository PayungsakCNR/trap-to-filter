import datetime
import Filterx
import time
from influxdb import InfluxDBClient

now = datetime.datetime.now()
strnow = now.strftime("%X") #current time
#log file date
fileDate = now.strftime("%d-%b-%Y")
fileName = "trapd-" + fileDate + ".log"

def replaceMultiple(mainString, toBeReplaces, newString):
    # Iterate over the strings to be replaced
    for elem in toBeReplaces:
        # Check if string is in the main string
        if elem in mainString :
            # Replace the string
            mainString = mainString.replace(elem, newString)

    return  mainString

def main():    
    output = open('/home/bass/receive/' + fileName, 'a')
    
    known_ssid_list = ["PSU WiFi 802.1x","PSU WiFi 5GHz","TrueMove H","CoEIoT","CoEWiFi"]

    while True:
        try:
            rawInput = raw_input()
            filtered = rawInput.replace("<UNKNOWN>","")
            showDate = filtered.replace("UDP: [172.30.232.2]:32768->[172.30.232.250]:162", strnow)
            wrongtypeRemove = replaceMultiple(showDate, Filterx.wronglist, '')
            timestamp = wrongtypeRemove.replace("DISMAN-EVENT-MIB::", "")
            hideMIB = replaceMultiple(timestamp, Filterx.mibList, '')
            event = hideMIB.replace("snmpTrapOID","Event")
            prefixRemove = replaceMultiple(event, Filterx.prefixList, '')
            weirdRemove = replaceMultiple(prefixRemove, Filterx.weirdList, ' ')
            bad_chars = "/\\!$^&*|'({)[}>_<]~+=#$%;`@?"
            #outstr - write log files into local server
            outstr  = weirdRemove.translate(None, bad_chars)
            result = replaceMultiple(outstr,Filterx.bad_list,' ')
            #write to local
            output.write(result + '\n')

            
        except EOFError:
            break
    output.close()

def sendToDB():
    readfile = open('/home/bass/receive/' + fileName, 'r')
    dbClient = InfluxDBClient('localhost', 8086, 'sabaszx', 'admin', 'trapEvent', ssl=False, verify_ssl=False)
    dbClient.create_database('trapEvent')
    #export to db
    line = readfile.read()
    if not line:
        time.sleep(1) 

    #print('Database created, go check in shell')

    dbClient.switch_database('trapEvent')

if __name__ == '__main__':
    main()
    sendToDB()
