@echo off
setlocal enabledelayedexpansion
set bookmaker_tmp=S:\bookmaker_tmp
set testdir_name=bookmaker_tests
set tests_tmpdir=%bookmaker_tmp%\%testdir_name%
set test_manuscript_dir=S:\resources\bookmaker_scripts\bookmaker_tests\test_manuscripts
REM setup
if not exist "%tests_tmpdir%" mkdir "%tests_tmpdir%"

REM for each test_ms: tear down last run, create dir and copy in test ms
for %%f in (%test_manuscript_dir%\*.docx) do (
  set "test_ms_name=%%~nxf"
  set "test_ms_dirname=%%~nf"
  REM echo !test_ms_name!
  set test_ms_dir=!tests_tmpdir!\!test_ms_dirname!
  REM echo !test_ms_dir!

  REM tear down last run, create dir, copy ms.docx
  if exist "!test_ms_dir!" rmdir /s /q "!test_ms_dir!\"
  mkdir "!test_ms_dir!"
  echo f | xcopy /f "!test_manuscript_dir!\!test_ms_name!" "!test_ms_dir!\!test_ms_name!"

  REM makedir for images and copy (if present)
  mkdir "!test_ms_dir!\submitted_files"
  if exist "!test_manuscript_dir!\!test_ms_dirname!_images" (
    xcopy /s "!test_manuscript_dir!\!test_ms_dirname!_images" "!test_ms_dir!\submitted_files"
    )

  REM run .bat
  REM S:\resources\bookmaker_scripts\bookmaker_deploy\bookmaker_test_direct.bat "!test_ms_dir!\!test_ms_name!" 'direct'
  REM \/ spawn .bat instead of run ^ (better for multiple files)
  start /b S:\resources\bookmaker_scripts\bookmaker_deploy\bookmaker_test_direct.bat "!test_ms_dir!\!test_ms_name!" 'direct' "" ""
)

PAUSE
