@echo off
rem =========================================================
rem
rem =========================================================

echo(
echo ---------- My Grep (missing text) ----------


echo(
set /p s="Enter regexp search pattern [error] : "

IF "%s%x" EQU "x" (
   set s=error
)

echo(
set /p f="Enter regexp file name pattern [\.py] : "

IF "%f%x" EQU "x" (
   set f=\.py$
)

perl -w grepx.pl "%s%" "%f%"

pause