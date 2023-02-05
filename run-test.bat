@echo off
set workflow=D:\4. Development\lome-files\workflows\1963276b-fda0-4fce-8566-ca1393243a1a\workflow.json
set output=D:\4. Development\lome-files\scratch\8e25accd-21b4-474f-8f0c-27b3783014c8
set experiment=%output%\experiment.json

set PYTHONPATH=%PYTHONPATH%;
@echo

python "D:\4. Development\ogse-workflow\main.py" --workflow "%workflow%" --experiment "%experiment%" --output "%output%"

pause