# FMC-RESTAPI-LABS

DevNet Firepower Management Center (FMC) Representative State Transfer (REST) Application Programming Interface (API) Learning Labs
 
## Use Case Description

These scripts are the examples from the Firepower Management Center (FMC) DevNet API Learning Lab.
requestToken.py is a script that assists in requesting and refreshing an authorization token from the FMC
getNetObjs.py is a script that displays all Network Objects from the specified FMC
bulkPostNetObjs.py is a script that takes a CSV file of Network Objects and adds them to the specified FMC

## Installation

To make use of these scripts, please run the following pip3 command in the downloaded script directory.
It will install the python3 modules required for the scripts to function properly.
```shell
FMC-RESTAPI-LABS %> pip3 install -r ./requirements.txt
```


## Configuration

No configuration is necessary to run this code outside of the python3 modules.

## Usage

**requestToken.py:**
```shell
FMC-RESTAPI-LABS % python3 ./requestToken.py --help
usage: requestToken.py [-h] username password ip_address

positional arguments:
  username    API username
  password    password of API user
  ip_address  IP of FMC

optional arguments:
  -h, --help  show this help message and exit
```

**getNetObjs.py:**
```shell
FMC-RESTAPI-LABS % python3 ./getNetObjs.py --help
usage: getNetObjs.py [-h] username password ip_address

positional arguments:
  username    API username
  password    password of API user
  ip_address  IP of FMC

optional arguments:
  -h, --help  show this help message and exit
```

**bulkPostNetObjs.py:**
```shell
FMC-RESTAPI-LABS % python3 ./bulkPostNetObjs.py -h
usage: bulkPostNetObjs.py [-h] username password ip_address csvInput

...         input file formatting – one name per line
...         --------------------------------
...         name,value,description,overridable,type

positional arguments:
  username    API username
  password    password of API user
  ip_address  IP of FMC
  csvInput    provide the csv of network objects to add.

optional arguments:
  -h, --help  show this help message and exit
```


### DevNet Learning Lab

Please go to the DevNet Learning Lab for Firepower Management Center (FMC) to learn how to use these scripts:  
https://developer.cisco.com/learning/modules/fmc-api


### DevNet Sandbox

The Sandbox which can implement this script is at:
https://devnetsandbox.cisco.com/RM/Diagram/Index/1228cb22-b2ba-48d3-a70a-86a53f4eecc0?diagramType=Topology

## Getting help

If you have questions, concerns, bug reports, etc., please create an issue against this repository.

## Author(s)

This project was written and is maintained by the following individual(s):  

* Sudhir H. Desai <suddesai@cisco.com>
