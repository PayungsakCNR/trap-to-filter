import datetime
import re
import string
import sys
import Filterx

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
 
    while running:
        try:
            read = raw_input()
            filtered = read.replace("<UNKNOWN>","" )
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
            sameAp = outstr.replace("ApName", "APName")
            result = replaceMultiple(sameAp,Filterx.bad_list,' ')
            output.write(result + '\n')
            
           
        except EOFError:
            running = False
    output.close()
if __name__ == '__main__':
    main()
