# Example Code for the FTD REST API Cookbook Procedures


Link to the [FTD REST API cookbook](https://developer.cisco.com/docs/firepower/threat-defense/cookbook/)

Use this example code to perform REST API operations as described in the cookbook on an FTD device.

Standalone Python3 scripts are in examples/demo. These scripts execute the end to end cookbook procedures.

Python3 scripts in examples/resources contain the functions used to perform single operations in the standalone Python scripts.

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



