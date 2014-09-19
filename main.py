import requests
import argparse


fuzz = argparse.ArgumentParser(description='fuzz [discover | test] url OPTIONS', add_help=False)

#print('COMMANDS:')
fuzz.add_argument('discover',help='Output a comprehensive,human-readable list of all \
        discovered inputs to the system. Techniques include both crawling and guessing.')
fuzz.add_argument('test',help='Discover all inputs, then attempt a list of exploit vectors\
        on those inputs. Report potential vulnerabilities.')

#print('OPTIONS:')
fuzz.add_argument('--custom-auth=string',help='Signal that the fuzzer should use hard-coded\
        authentication for a specific application (e.g. DVWA).') #OPTIONAL

#print('Discover options:')
fuzz.add_argument('--common-words=file', help='Newline-delimited file of common words to be \
        used in page guessing and input guessing.')


fuzz.print_help()
