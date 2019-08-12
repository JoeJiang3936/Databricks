@ECHO OFF 
:: This batch will upload files to github automatically
TITLE GitPush
:: Section 1: test batch file

ECHO === git add * ===
git add * 

ECHO === git commit -am "-" ===
git commit -am "-"


ECHO === git push ===
git push

ECHO  bye...

exit /B
