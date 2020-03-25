# covid19pl
Collector of Polish data on the number of cases of COVID19 disease caused by the
SARS-CoV-2 virus. Information chaos can be tiring. Insulate yourself from him
and stay in touch with relevant information on demand. Take a look how disease
spreads in Poland and start following the guidelines and recommendations of
official government health authorities. 

## Changelog
  - Ver. 1.4.0:  Split project into multiple files
  - Ver. 1.3.0:  Add plot with total cases in Poland
  - Ver. 1.2.0:  Add email reports with 
  - Ver. 1.1.0:  Remove **mandatory** options, add default path to
                 workspace direcotry containing COVID19 data
  - Ver. 1.0.0:  Initial script version

## Requirements
### Software
Python3.7 with additional packages listed in requirements.txt file.

### Environment setup
If you don't want to use **--email** option this step is not necessary.
Sending email requires to have defined four system variables containing
sensitive data necessary to communicate with SMTP server. Variables can be
defined globally for the system or locally for the script in **.env** file.
Default localization of **.env** file is the script directory, but you can
change it with **--env** option.
Below example shows how to prepare configuration for GMAIL service in **.env**:
```
export EMAIL_SMTP_SRV_ADDR="smtp.gmail.com"
export EMAIL_SMTP_SRV_PORT=587
export EMAIL_SMTP_SRV_LOGIN="SOME_GMAIL_ADDRESS@gmail.com"
export EMAIL_SMTP_SRV_PASSWORD="SECRET PASSWORD"
```
Using Google SMTP servers may require enable less secure apps to access 
gmail accounts.

## How to use the script
In order to get help please go to the directory with **covid19pl.py** file and
execute **python ./covid19pl.py --help** command. Keep in mind that at before
you do that all packages listed in **requirements.txt** files should be 
installed either in your system globally, or in virtual environment.

## Sample usage
To run the script with on screen data display and sending email on 
'sent\_it\_to@gmail.com' run command:
```
$> python ./covid19pl --display --gather --email=sent_it_to@gmail.com
```
Together with sending email you this is the output you will see in your terminal:
```
Welcome to /home/sebastian/repo/covid19pl/covid19pl.py in version 1.2.0
Published on GNU General Public License 3.0 by oscarsierraproject.eu
Copyright 2020, oscarsierraproject.eu
GitHub: https://github.com/oscarsierraproject/covid19pl

SARS-CoV-2 data with 1 day change summary
Location            :   Total   Death   Cured  CHANGE:   Total   Death   Cured
Cała Polska         :     452       5       0               27       0       0
dolnośląskie        :      61       2       0                3       0       0
kujawsko-pomorskie  :      16       0       0                2       0       0
lubelskie           :      30       1       0                2       0       0
lubuskie            :       9       0       0                0       0       0
mazowieckie         :     107       0       0                0       0       0
małopolskie         :      15       0       0                1       0       0
opolskie            :      10       0       0                0       0       0
podkarpackie        :      20       1       0                1       0       0
podlaskie           :       5       0       0                2       0       0
pomorskie           :      11       0       0                1       0       0
warmińsko-mazurskie :      20       0       0                3       0       0
wielkopolskie       :      26       1       0                8       0       0
zachodniopomorskie  :      10       0       0                1       0       0
łódzkie             :      57       0       0                0       0       0
śląskie             :      49       0       0                3       0       0
świętokrzyskie      :       6       0       0                0       0       0
TIMESTAMP OF SAMPLES 2020-03-22 17:57:48
```
