import requests
import argparse


print("fuzz [discover | test] url OPTIONS")

cmds = argparse.ArgumentParser(description='COMMANDS:')
cmds.add_argument('discover',help='Output a comprehensive,human-readable list of all \
        discovered inputs to the system. Techniques include both crawling and guessing.')
cmds.add_argument('test',help='Discover all inputs, then attempt a list of exploit vectors\
        on those inputs. Report potential vulnerabilities.')

ops = argparse.ArgumentParser(description='OPTIONS:')
ops.add_argument('--custom-auth=string',help='Signal that the fuzzer should use hard-coded\
        authentication for a specific application (e.g. DVWA).') #OPTIONAL

cmds.print_help()
ops.print_help()

