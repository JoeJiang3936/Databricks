@ECHO OFF 
:: This batch will upload files to github automatically
TITLE GitPush
:: Section 1: test batch file
ECHO ============================
ECHO Github Push
ECHO ============================
git add * 
git commit -am "-"
git push
ECHO ============================
ECHO done
ECHO ============================
exit