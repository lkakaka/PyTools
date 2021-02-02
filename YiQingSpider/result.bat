@echo off
python --version
cd src
::set path=%path%;.\src
::echo %path%
python result_spider.py 0
pause