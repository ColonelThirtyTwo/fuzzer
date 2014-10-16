@echo off
echo FUZZER
python main.py -h

set /p answer=Start fuzzing DVWA (Y/N)?
if /i "%answer%"=="Y" goto start
if /i "%answer%"=="N" goto finish

:start
echo Fuzzing commencing!..
echo Establishing connection to localhost:8080/DVWA-1.0.8/..
python3 main.py -v --blacklist="/DVWA-1.0.8/logout.php" --cookies="{\"security\":\"low\"}" --custom-auth="{\"username\":\"admin\",\"password\":\"password\",\"Login\":\"login\"}" test http://localhost:8080/DVWA-1.0.8/login.php -v vectors.txt -s sensitive.txt --slow=1000
echo Establishing connection to 127.0.0.1/dvwa/..
python3 main.py -v --blacklist="/dvwa/logout.php" --cookies="{\"security\":\"low\"}" --custom-auth="{\"username\":\"admin\",\"password\":\"password\",\"Login\":\"login\"}" test http://127.0.0.1/dvwa/login.php -v vectors.txt -s sensitive.txt --slow=1000


:finish
echo Fuzzer closing..
