@ECHO off

%SYSTEMROOT%\py.exe installer.py
IF %ERRORLEVEL% NEQ 0 (ECHO "Installation failed. Please make sure you have Python (at least version 3.5) installed.") ELSE (ECHO "Successfully installed the Metacritic Scraper. Start it by opening 'scraper.bat'!")
PAUSE

