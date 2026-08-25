@echo off
setlocal EnableDelayedExpansion
REM ===========================================================================
REM publish_all.bat - publish the three @antoneeo agentic-sdlc packages in one run.
REM   code : @antoneeo/agentic-sdlc-skill       (repo root)
REM   kb   : @antoneeo/kb-agentic-skill         (distributions\kb-agentic-skill)
REM   mkt  : @antoneeo/mkt-agentic-sdlc-skill   (distributions\mkt-agentic-sdlc)
REM
REM PRECONDITION: versions bumped + committed + tagged (run git_push_tag.bat FIRST).
REM   npm publish packs the WORKING TREE, so publish from the clean tagged checkout.
REM 2FA (web-based): npm prints an authentication URL and opens your browser for
REM   EACH package - authorize each one there to continue. (If your account instead
REM   uses an authenticator APP, append  --otp=CODE  to the npm publish line below.)
REM RE-RUNNABLE: a package whose version is already on the registry is skipped,
REM   so if a publish fails (expired code, network) just re-run this script.
REM access=public is already in each package.json publishConfig - no flag needed.
REM ===========================================================================
set "ROOT=%~dp0"

echo ============================================================
echo   Publish the agentic-sdlc triplet  (code / kb / mkt)
echo   Precondition: bump + commit + tag done (git_push_tag.bat).
echo   npm opens a browser to authorize EACH package.
echo ============================================================
set /p "GO=Proceed? [y/N]: "
if /I not "!GO!"=="y" ( echo Aborted. & exit /b 1 )

call :pub "%ROOT%."                              "@antoneeo/agentic-sdlc-skill"     || exit /b 1
call :pub "%ROOT%distributions\kb-agentic-skill" "@antoneeo/kb-agentic-skill"       || exit /b 1
call :pub "%ROOT%distributions\mkt-agentic-sdlc" "@antoneeo/mkt-agentic-sdlc-skill" || exit /b 1

echo.
echo === verify (registry versions) ===
call npm view @antoneeo/agentic-sdlc-skill version
call npm view @antoneeo/kb-agentic-skill version
call npm view @antoneeo/mkt-agentic-sdlc-skill version
echo.
echo All three published.
exit /b 0

REM ---------------------------------------------------------------------------
:pub
REM %~1 = package dir, %~2 = package name
pushd "%~1" || ( echo [FAIL] cannot enter %~1 & exit /b 1 )
set "VER="
for /f "delims=" %%v in ('npm pkg get version') do set "VER=%%~v"
echo.
echo --- %~2 @ !VER! ---
echo   Publishing %~2 - authorize in the browser when npm opens it...
call npm publish
if errorlevel 1 (
  echo [FAIL] %~2 publish failed. Read the error above ^(re-authorize, or the version
  echo        is already published^), then re-run - retry only the packages not yet done.
  popd & exit /b 1
)
echo [ok] published %~2 @ !VER!.
popd & exit /b 0
