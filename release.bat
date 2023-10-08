@echo off
:: Script to prepare for releasing a new version of a package.

:: Before running this script _version.py should be updated with the
:: next version label.

:: Tag repo with current package version (from _version.py).

:: Get package version using pdm
FOR /f "usebackq tokens=* delims=" %%A in (`pdm show --version`) do @set "TAGVERSION=%%A"

echo Creating tag %TAGVERSION%

:: Tag local repo
git tag %TAGVERSION%
IF %ERRORLEVEL% NEQ 0 ( Exit /b 1 )

:: Push tag to origin
git push -q origin %TAGVERSION%
IF %ERRORLEVEL% NEQ 0 ( Exit /b 1 )

:: Once complete the github action "release" should be run to publish
:: the package to pypi.
