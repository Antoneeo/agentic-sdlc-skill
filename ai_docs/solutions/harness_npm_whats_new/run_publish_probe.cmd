@echo off
REM F-070 probe: run publish_all.bat with npm replaced by npm_stub.js.
REM Usage: run_publish_probe.cmd all^|none ^<repo dir^> ^<log file^>
REM Both paths are made absolute here: publish_all.bat changes directory per package.
setlocal
set "PATH=%~dp0;%PATH%"
set "NPM_STUB_REGISTRY=%~1"
set "NPM_STUB_LOG=%~f3"
cd /d "%~f2" || exit /b 9
echo y| "%~f2\publish_all.bat"
