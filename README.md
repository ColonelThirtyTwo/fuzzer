Fuzzer Project
==============

Alex Parrill, Ryan Switzer, Brian Hanson

Project for SE 331 "Engineering Secure Software" at Rochester Institute of Technology


Requirements
------------

Python: v3.2 or newer

	sudo apt-get install python3

Requests: v2.4.3 or newer

	sudo apt-get install python3-pip
	sudo pip install requests

Usage
-----

Run this command to get usage information:

	python3 main.py --help

To get help with the subcommands:

	python3 main.py discover --help

OR

	python3 main.py test --help

Note that the -v, -q, --blacklist, --custom-auth, and --cookies parameters must come before the subcommand (test|discover), and subcommand specific arguments must come after the subcommand.


Example Execution for DVWA
--------------------------

This assumes that DVWA is at localhost:8080/DVWA-1.0.8, but the URL is easily modified. Just don't forget to change the logout blacklisted page as well.

UNIX:

    python3 main.py -v --blacklist="/DVWA-1.0.8/logout.php" --cookies='{"security":"low"}' --custom-auth='{"username":"admin","password":"password","Login":"login"}' test http://localhost:8080/DVWA-1.0.8/login.php -v vectors.txt -s sensitive.txt --slow=1000

Windows:

    python3 main.py -v --blacklist="/DVWA-1.0.8/logout.php" --cookies="{\"security\":\"low"\}" --custom-auth="{\"username\":\"admin\",\"password\":\"password\",\"Login\":\"login\"}" test http://localhost:8080/DVWA-1.0.8/login.php -v vectors.txt -s sensitive.txt --slow=1000
