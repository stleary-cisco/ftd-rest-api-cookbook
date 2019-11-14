# Example Code for the FTD REST API Cookbook Procedures


This project contains Python3 scripts for the [FTD REST API cookbook](https://developer.cisco.com/docs/firepower/threat-defense/ )

Use this example code to perform REST API operations as described in the cookbook on an FTD device.

The files in examples/ftd_api_scripts are standalone Python3 scripts to execute the end to end cookbook procedures.
The files in examples/ftd_api_resources contain the functions used to perform REST API requests from the standalone scripts.

## To execute from the command line:

These scripts require Python version 3.0 or greater and the [Requests](https://requests.kennethreitz.org/en/master/) library.

You will need to provide device host, port, user, passwd, and sometimes other parameters. For example,
````
cd examples/ftd_api_scripts
set PYTHONPATH=../examples
python deploy.py ftd.example.com 443 admin Admin123
````



