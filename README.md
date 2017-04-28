# HEXA-A Test Tool
HEXA-A Test Tool is simple GUI Test Tool that is used to get the Generated Output after running certain program under any input parameters and compare it with stored Expected Output of each Test Case.
>It uses the concept of Black-box Testing.

The main target is 3rd year students of Electronics and Communication Department, Faculty of Engineering - Cairo University, To easily test their C++ assignments with multiple Test Cases.

![Home](https://cloud.githubusercontent.com/assets/18114443/23592239/6a2f1218-0206-11e7-9579-bf727403ddae.PNG)

## Downloads
* [Windows Version](http://www.hexa-a.com/HEXA-A.Test.Tool.v1.0.(Windows).zip)
* [Linux Version](http://www.hexa-a.com/HEXA-A.Test.Tool.v1.0.(Linux).zip)

## Using The Tool

### Windows
1. Open Tool File: ```HEXA-A.exe``` 
1. Select Test Case
1. Select the Program you want to Test _(EXE File)_
1. Click **Start Test**

### Linux
> First Time Only, You need to run setupHEXA script to install all requirements automatically: ```sudo bash setupHEXA.sh```

1. Open Tool Script:
```python3 HEXA-A.py```
1. Select Test Case
1. Select the Program you want to Test _(.out File)_
1. Click **Start Test**

## Build EXE File for Windows

### Build Requirements
* __Python 3.5 or earlier__
* __PyQt 5__
* __PyInstaller 3.2.1__

### Build Steps
* From __CMD__:
```
pyinstaller --onefile --windowed HEXAmain.py
```
* Copy (icons) Folder to (dist) Folder before opening the Tool.

## Online Version
* [Online Test Tool](http://www.hexa-a.com)
* [Source Code](https://github.com/hexa-a/TestToolOnline)
