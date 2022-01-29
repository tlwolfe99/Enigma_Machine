@echo off
rem =========================================================
rem
rem =========================================================

echo(
echo ---------- My Grep (find text) ----------


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

perl -w grep.pl "%s%" "%f%"

pause