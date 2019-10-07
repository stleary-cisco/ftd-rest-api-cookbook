# Example Code for FTD REST API Cookbook Procedures

[https://developer.cisco.com/docs/firepower/threat-defense/cookbook/](https://developer.cisco.com/docs/firepower/threat-defense/cookbook/)

Use this example code to perform REST API operations on an FTD device.

Scripts in examples/demo perform end to end operations as described in the FTD REST API cookbook. Edit connection_constants.py
to customize the connection information for your FTD device.

Scripts in examples/resources contain the functions used to perform single operations on the FTD device.


You can run these scripts in Pycharm or from the command line.

From Pycharm: create a pure python project, do not use the remote deploy kick server. Instead you can execute locally.
From the command line:
You will need the requests lib. To see if you have it:
````
	python
	import requests
````

If you get an error, execute these lines inside the python console:
````
	from pip._internal import main
	main(['install', 'requests'])
````

To get the files:
git clone https://github.com/stleary-cisco/ftd-rest-api-cookbook.git

To run the scripts:
````
	cd examples
	set PYTHONPATH=.
	python demo/demo_troubleshoot.py
````

You will need to edit the demo*py files and set the correct host, port, and password values:
````
    host = '10.89.21.72'
    port = '3139'
    user = 'admin'
    passwd = 'Admin123$'
````


