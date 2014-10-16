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

  another option to install requests is to clone the repo:
    git clone git://github.com/kennethreitz/requests.git
  and then navigate to the requests clone and run:
    python setup.py install


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

OR

		sh fuzz_test_ux

Windows:

    python3 main.py -v --blacklist="/DVWA-1.0.8/logout.php" --cookies="{\"security\":\"low\"}" --custom-auth="{\"username\":\"admin\",\"password\":\"password\",\"Login\":\"login\"}" test http://localhost:8080/DVWA-1.0.8/login.php -v vectors.txt -s sensitive.txt --slow=1000

OR

		fuzz_test

*Note the given scripts will only attempt to establish connections with localhost:8080/DVWA-1.0.8 and 127.0.0.1/dvwa.
