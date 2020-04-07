import time
import datetime
import Filterx
import JadeBowx
import re
import subprocess
import collections
import os

now = datetime.datetime.now()
strnow = now.strftime("%X") #current time
#log file date
fileDate = now.strftime("%d-%b-%Y") #day-month-year
path = '/home/bass/receive/'
fileName = "trapd-" + fileDate + ".log"

'''
MAC Address List should be load from some Database for flexible use (If add more AP)
'''
#lists of ap mac address each floor
floor01_mac_list = ['bc:16:f5:98:8:0','68:3b:78:e1:8e:c0','68:3b:78:e1:94:20','f4:4e:5:a2:a1:d0',
                    'dc:8c:37:4c:2e:e0','f4:4e:5:b5:24:b0']

floor02_mac_list = ['88:1d:fc:a:f1:20','88:1d:fc:6:3f:b0','70:10:5c:b1:a4:d0','a0:e0:af:3d:c7:80',
                   'f4:4e:5:a2:a1:10','f4:4e:5:b5:65:90']

floor03_mac_list = ['a0:3d:6f:31:b7:e0','f4:4e:5:df:4e:f0','f4:4e:5:db:f0:40','70:10:5c:b1:9e:d0',
                    '68:3b:78:e1:93:0','68:3b:78:e1:93:80','68:3b:78:e9:47:40']

floor04_mac_list = ['a0:e0:af:22:6e:70','a0:3d:6f:31:b7:f0','a0:3d:6f:31:b7:d0','a0:e0:af:95:9c:40',
                   'a0:3d:6f:dd:2d:70']

#all ap mac addresses in building

buildingMacList = floor01_mac_list + floor02_mac_list + floor03_mac_list + floor04_mac_list

def listDuplicates(seq): 
    seen = set()
    seen_add = seen.add
    # adds all elements it doesn't know yet to seen and all other to seen_twice
    seen_twice = set( x for x in seq if x in seen or seen_add(x) )
    # turn the set into a list (as requested)
    return list( seen_twice )

# def findDuplicates(seq):
#     result = ([item for item, count in collections.Counter(seq).items() if count > 1])
#     return result 

def compileMacPattern(receive):
    pattern = re.compile(r'(?:[0-9a-fA-F]:?){12}')
    resultMac = re.findall(pattern, receive) #now there's only list of mac addresses
    return str(resultMac)

def replaceMultiple(mainString, toBeReplaces, newString):
    # Iterate over the strings to be replaced
    for elem in toBeReplaces :
        # Check if string is in the main string
        if elem in mainString :
            # Replace the string
            mainString = mainString.replace(elem, newString)
    return  mainString

def calculatePercentage(value,total):
    percentage = (value/total) * 100
    return percentage

def readAndInsertSSID():
    #extract specific line
    output = '' #empty string to be merge into long single line
    with open(path + fileName,'r') as f:
        for line in f:
            line = line.rstrip()
            if re.search('SSID', line):
                output += line.replace('SSID ','') #concat string and replace string
    f.close() #close file
  
    #value of each ssid
    sumTrue = (int(output.count('TrueMove H')))
    sumCoE = (int(output.count('CoEWiFi')))
    sumPsu = (int(output.count('PSU WiFi 802.1x')))
    sum5G  = (int(output.count('PSU WiFi 5GHz')))
    sumAis = (int(output.count('AIS SMART Login')))
    sumIot = (int(output.count('CoEIoT')))

    #total number of ssids
    overall = int(output.count('TrueMove H')) + int(output.count('CoEWiFi')) + int(output.count('PSU WiFi 802.1x')) + int(output.count('PSU WiFi 5GHz')) + int(output.count('AIS SMART Login')) + int(output.count('CoEIoT'))

    '''
    #insert to database
    JadeBowx.countTruemove(sumTrue)
    JadeBowx.countCoeWifi(sumCoE)
    JadeBowx.count802(sumPsu)
    JadeBowx.countPSU5Ghz(sum5G)
    JadeBowx.countAIS(sumAis)
    JadeBowx.countCoeIot(sumIot)
    '''

    #insert to DB
    JadeBowx.countSSID(sumTrue,"TrueMove H")
    JadeBowx.countSSID(sumCoE,"CoEWiFi")
    JadeBowx.countSSID(sumXXX,"XXX")

    try:
        #insert percentage
        perTrue = calculatePercentage(sumTrue,overall)
        perCoe = calculatePercentage(sumCoE,overall)
        perPsu = calculatePercentage(sumPsu,overall)
        per5G = calculatePercentage(sum5G,overall)
        perAis = calculatePercentage(sumAis,overall)
        perIoT = calculatePercentage(sumIot,overall)
        
   
    except ZeroDivisionError:
        overall = 1
    
    finally:
        '''
        #insert percantage
        JadeBowx.countTruemove_percentage(sumTrue)
        JadeBowx.countCoeWifi_percentage(sumCoE)
        JadeBowx.count802_percentage(sumPsu)
        JadeBowx.countPSU5Ghz_percentage(sum5G)
        JadeBowx.countAIS_percentage(sumAis)
        JadeBowx.countCoeIot_percentage(sumIot)
        '''
        JadeBowx.countSSID_percentage(sumSSID1,"SSID_NAME1")
        JadeBowx.countSSID_percentage(sumSSID2,"SSID_NAME2")
    
    
#read an    d insert
def readAndInsert():
    with open(path + fileName,'r') as readTest:
        #delete specific lines (session ID):
        macPattern = compileMacPattern(str(readTest)) #this return all mac addresses
        duplicateMac = listDuplicates(macPattern) # return dupliccated mac addresses (include ap)
        
        #return number of client addres
        clientMac = list(set(duplicateMac) - set(buildingMacList))
        toInsert = str(len(clientMac)) #result to be insert
        JadeBowx.countClient(toInsert)

    readTest.close

def main():
   
    output = open( path + fileName, 'a') #write into local server

    while True:
        try:
            input_raw = input()
            #filter weird string sction
            subprocess.call(['sed','-i','/.*SessionID.*/d',path + fileName])
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

            #write to local serever
            output.write(result + '\n')

        except EOFError:
            break
        finally:
            output.close
#            os.remove(path+fileName)
            
if __name__ == '__main__':
    main()
    readAndInsert()
    readAndInsertSSID()
