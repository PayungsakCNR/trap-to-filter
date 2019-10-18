import datetime
import re
import string

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
    output = open('/home/bass/trap-receiver/' + fileName, 'a')
    
    while running:
        try:
            input = raw_input()
            filtered = input.replace("<UNKNOWN>","" )
            showDate = filtered.replace("UDP: [172.30.232.2]:32768->[172.30.232.250]:162", strnow)
        
            wronglist = ['Wrong Type (should be Gauge32 or Unsigned32)', 'Wrong Type should be Timeticks:']

            wrongtypeRemove = replaceMultiple(showDate, wronglist, '')
            timestamp = wrongtypeRemove.replace("DISMAN-EVENT-MIB::", "")
            mibList = ['SNMPv2-MIB::','CISCO-LWAPP-SI-MIB::','CISCO-LWAPP-RRM-MIB::',
            'CISCO-LWAPP-ROGUE-MIB::','AIRESPACE-WIRELESS-MIB::',
            'CISCO-LWAPP-DOT11-CLIENT-MIB::','CISCO-LWAPP-AP-MIB::','CISCO-LWAPP-AP-MIB::']
            hideMIB = replaceMultiple(timestamp, mibList, '')
            event = hideMIB.replace("snmpTrapOID","Event")
            prefixList = ['bsn','cL','cldc','Dot11','Dot3']
            weirdList = ['.0',". ",'.1 ','"',' : ']
            prefixRemove = replaceMultiple(event, prefixList, '')
            weirdRemove = replaceMultiple(prefixRemove, weirdList, '')
            bad_chars = "/\\!$^&*|'({)[}>_<]~+=#$%;`@?"
            #rgx = re.compile('[%s]' % bad_chars)
            # pattern = "^.A-Za-Z0-9'&{8,9}"
            # replace = ''
            #outstr
            bad_list = ['.......','..N...','.t....','..N..i.','..V...','..:..j',
            '......f','......','..a.bk','    .','....np','..N..j.','.hx.G','...z.A.','..p-:.e'
            ,'.p....']
            outstr  = weirdRemove.translate(None, bad_chars)
            result = replaceMultiple(outstr,bad_list,'')

            output.write(result + '\n')

        except EOFError:
            running = False
    output.close()
if __name__ == '__main__':
    main()
