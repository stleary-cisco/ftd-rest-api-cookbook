# Example Code for the FTD REST API Cookbook Procedures


This project contains Python3 scripts for the [FTD REST API cookbook](https://developer.cisco.com/docs/firepower/threat-defense/cookbook/)

Use this example code to perform REST API operations as described in the cookbook on an FTD device.

The files in examples/demo are standalone Python3 scripts to execute the end to end cookbook procedures.
The files in examples/resources contain the functions used to perform REST API requests from the standalone scripts.

## To execute from the command line:

These scripts require Python version 3.0 or greater and the [Requests](https://requests.kennethreitz.org/en/master/) library.

You will need to edit the demo*py files and set the correct host, port, user, and passwd values for your FTD device:
````
host = 'ftd.example'
port = '443'
user = 'admin'
passwd = 'Admin123'
````

To run the scripts:
````
cd examples
set PYTHONPATH=.
python demo/demo_deploy.py
````



