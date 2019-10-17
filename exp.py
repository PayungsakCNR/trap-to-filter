import datetime
import re

def main():
    running = True
    now = datetime.datetime.now()
    # strnow = now.strftime("%X") #current time
    #log file date
    fileDate = now.strftime("%d-%b-%Y")
    fileName = "trapd-" + fileDate + ".log"
    output = open('/home/bass/trap-receiver/' + fileName, 'a')
    
    while running:
        try:
            input = raw_input()
            filtered = input.replace("<UNKNOWN>","")
            wrongtypeRemove = filtered.replace("Wrong Type (should be Gauge32 or Unsigned32)","")
            screen = re.sub('[^A-Za-z0-9]+[.]+[:]', '', wrongtypeRemove)

            #final result
            Result  = screen           
            output.write(Result + "\n")

        except EOFError:
            running = False
    output.close()
if __name__ == '__main__':
    main()
