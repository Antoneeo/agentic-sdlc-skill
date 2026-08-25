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
REM RE-RUNNABLE: before each package the local version is compared against the
REM   registry, and a package already published at that version is SKIPPED without
REM   attempting a publish. So a partial run (expired code, network) is resumed by
REM   simply re-running, and a single-package release works: the two packages that
REM   did not change are skipped instead of aborting the run on the first one.
REM   (Until 2026-08-25 this comment promised the skip and the code did not do it:
REM   npm exits non-zero on an already-published version, which the error branch
REM   treated as a failure. Publish order is code -> kb -> mkt, so a kb-only
REM   release died on `code` and never reached kb.)
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
REM Twice now this block reported the PREVIOUS version after a successful
REM publish and read as a failure. --prefer-online alone was not enough: it
REM forces revalidation, but it cannot outrun CDN propagation of the `latest`
REM tag in the seconds after a publish. So each package is polled until the
REM registry agrees with the local version, or the attempts run out -- and the
REM local version is printed beside it, so "did it publish?" is answerable from
REM this output instead of requiring a manual `npm view` afterwards.
call :verify "%ROOT%."                              "@antoneeo/agentic-sdlc-skill"
call :verify "%ROOT%distributions\kb-agentic-skill" "@antoneeo/kb-agentic-skill"
call :verify "%ROOT%distributions\mkt-agentic-sdlc" "@antoneeo/mkt-agentic-sdlc-skill"
echo.
echo All three published.
exit /b 0

REM ---------------------------------------------------------------------------
:pub
REM %~1 = package dir, %~2 = package name
pushd "%~1" || ( echo [FAIL] cannot enter %~1 & exit /b 1 )
set "VER="
for /f "delims=" %%v in ('npm pkg get version') do set "VER=%%~v"
if not defined VER (
  echo [FAIL] cannot read a version from %~1\package.json
  popd & exit /b 1
)
REM Ask the registry BEFORE publishing rather than reading npm's error text
REM afterwards: an already-published version is a no-op to be reported, not a
REM failure to be parsed. `npm view` on a never-published package writes to
REM stderr and leaves PUB empty, which correctly falls through to the publish.
set "PUB="
for /f "delims=" %%v in ('npm view %~2 version --prefer-online 2^>nul') do set "PUB=%%v"
echo.
echo --- %~2 @ !VER! ---
if /I "!PUB!"=="!VER!" (
  echo   [ok] !VER! is already on the registry - skipped, nothing to do.
  popd & exit /b 0
)
if defined PUB (
  echo   registry has !PUB!, publishing !VER! ...
) else (
  echo   not on the registry yet, publishing !VER! ...
)
echo   Authorize in the browser when npm opens it...
call npm publish
if errorlevel 1 (
  echo [FAIL] %~2 publish failed at !VER!. Read the error above ^(authorization
  echo        expired, network, or registry refusal^), then re-run - the packages
  echo        already done are skipped, so a re-run retries only what is left.
  popd & exit /b 1
)
echo [ok] published %~2 @ !VER!.
popd & exit /b 0

REM ---------------------------------------------------------------------------
:verify
REM %~1 = package dir, %~2 = package name. Polls until the registry catches up.
pushd "%~1" || ( echo [FAIL] cannot enter %~1 & exit /b 1 )
set "WANT="
for /f "delims=" %%v in ('npm pkg get version') do set "WANT=%%~v"
set "GOT="
for /L %%i in (1,1,10) do (
  if not "!GOT!"=="!WANT!" (
    set "GOT="
    for /f "delims=" %%v in ('npm view %~2 version --prefer-online 2^>nul') do set "GOT=%%v"
    if not "!GOT!"=="!WANT!" ping -n 4 127.0.0.1 >nul
  )
)
if "!GOT!"=="!WANT!" (
  echo   [ok] %~2 = !GOT!
) else (
  echo   [??] %~2 : local !WANT!, registry reports !GOT! - the registry may still
  echo        be propagating. Re-check with: npm view %~2 versions --json --prefer-online
)
popd & exit /b 0
