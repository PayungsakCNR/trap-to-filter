import datetime
import json

def main():
    #running = True
    now = datetime.datetime.now()
    #strnow = now.strftime("%X") #current time
    #log file date
    fileDate = now.strftime("%d-%b-%Y")
    fileName = "trapd-" + fileDate + ".log"
    read = open('/home/bass/trap-receiver/' + fileName, 'r')
    read.readline()
    
if __name__ == '__main__':
    main()

