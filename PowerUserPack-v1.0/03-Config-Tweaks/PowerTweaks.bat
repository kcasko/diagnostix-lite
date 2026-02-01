@echo off
color 0A
echo Applying power tweaks...

powercfg /setacvalueindex scheme_current sub_processor PROCTHROTTLEMAX 100
powercfg /setacvalueindex scheme_current sub_processor PROCTHROTTLEMIN 5
powercfg /setactive scheme_current

echo Done.
pause