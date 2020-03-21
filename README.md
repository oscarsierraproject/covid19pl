# covid19pl
Collector of Polish data on the number of cases of COVID19 disease caused by the SARS-CoV-2 virus.

# Requirements
Python3.7 with additional packages listed in requirements.txt file.

# Running options
$> pythonn ./covid19pl.py --help

        Welcome to ./covid19pl.py in version 1.0.0
        Published on GNU General Public License 3.0 by oscarsierraproject.eu
        Copyright 2020, oscarsierraproject.eu
        GitHub: https://github.com/oscarsierraproject/covid19pl

    Usage: covid19pl.py --workspace=<PATH>

    Options:
      --version             show program's version number and exit
      -h, --help            show this help message and exit

      MANDATORY OPTIONS:
        --workspace=WORKSPACE
                            path to directory with data [default:
                            /home/$USER/covid19pl/data]

      OPTIONAL OPTIONS:
        --debug             Run script in debug mode
        --display           Display latest data for Poland
        --gather            Use this option to gather latest data from gov.pl

    Copyright 2020, oscarsierraproject.eu, GNU General Public License 3.0

# Sample usage
$> python ./covid19pl --display --gather

        Welcome to /home/sebastian/repo/covid19pl/covid19pl.py in version 1.0.0
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
    TIMESTAMP OF SAMPLES 2020-03-21 17:57:48
