@ECHO OFF
REM Batch file to run test on a Windows machine

ECHO Running tests
ECHO.

ECHO Creating test directory
MKDIR test

ECHO Creating keywords.txt
ECHO car > test/keywords.txt
ECHO cat >> test/keywords.txt
ECHO apple >> test/keywords.txt

ECHO.
ECHO Test 1: python imscraper.py -k fan -p table -se bing -st 90 -o ./test/test1
python imscraper.py -k fan -p table -se bing -st 90 -o ./test/test1

ECHO.
ECHO Test 2: python imscraper.py -f test/keywords.txt -n 20 -o ./test/test2
python imscraper.py -f test/keywords.txt -n 20 -o ./test/test2

ECHO.
ECHO Test 3: python imscraper.py -c https://logodix.com/linux -o test/linux
python imscraper.py -c https://logodix.com/linux -o test/linux

ECHO.
ECHO Done
PAUSE