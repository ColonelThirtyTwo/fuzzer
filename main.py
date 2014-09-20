import requests
import argparse
import sys

INIT = 'fuzz'
COMMANDS = ['discover']#ADD test
OPTIONS = ['--custom-auth','--common-words']#OPTIONAL --custom-auth 

def main():
    fuzz = argparse.ArgumentParser(description='fuzz [discover | test] url OPTIONS', add_help=False)

    #COMMANDS:
    fuzz.add_argument('discover',help='Output a comprehensive,human-readable list of all \
            discovered inputs to the system. Techniques include both crawling and guessing.')
    fuzz.add_argument('test',help='Discover all inputs, then attempt a list of exploit vectors\
            on those inputs. Report potential vulnerabilities.')
    
    #OPTIONS:
    fuzz.add_argument('--custom-auth=string',help='Signal that the fuzzer should use hard-coded\
            authentication for a specific application (e.g. DVWA).') #OPTIONAL TASK
    
    #Discover options:
    fuzz.add_argument('--common-words=file', help='Newline-delimited file of common words to be \
            used in page guessing and input guessing.')
    
    fuzz.print_help()
    
    for cmd in sys.stdin:
        cmd = cmd.split()
        process(cmd)


def process(cmd):
    if (cmd[0].lower() == INIT) & (cmd[1].lower() in COMMANDS):
        print(cmd[0])       #fuzz
        print(cmd[1])       #COMMAND        
        print(cmd[2])       #URL  
        element = cmd[3].split('=')
        print(element[1])   #FILE
        
    else:
        print ('Error command not supported.\n')
    return

main()





