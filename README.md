Fuzzer Project
==============

Alex Parrill, Ryan Switzer, Brian Hanson

Project for SE 331 "Engineering Secure Software" at Rochester Institute of Technology

Usage
-----

Run this command to get usage information:

	python3 main.py --help

To get help with the subcommands:

	python3 main.py discover --help

OR

	python3 main.py test --help

Example Auth Strings
--------------------

DVWA:
	
	UNIX:
	--custom-auth='{"username":"admin","password":"password","Login":"login"}'
	
	Windows:
	--custom-auth="{\"username\":\"admin\",\"password\":\"password\",\"Login\":\"login\"}"

