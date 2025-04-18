# sre-take-home-exercise-python-blightjl

### Intalling and running the code:

1. Download the source code
2. Change directory into the source code
3. Create a local virtual environment by running the following: python3 -m venv venv
4. Activate the virtual environment by running: source venv/bin/acitivate
5. Now ensure these modules are downloaded in the environment: pyyaml, requests, aiohttp {these will need to be installed via pip}
6. Install the previous defined modules via the following command: pip install <missing_module_name>
7. Run the program with the following: python3 main.py sample.yaml
8. To stop the program enter the following keys: Control + C
9. To exit out of the activated environment run: deactivate

### Issues addressed and code changes:

Changes made to the main.py file:
* added a function to check the argument being passed in to be of type yaml file

* running requests.request when Method is empty from the sample.yaml file
    * should simply return "DOWN" when this is the case
    * which now properly checks the endpoints and their respective status

* used the time module to ensure that only requests in the 200s range and responses within 500ms resolved to an UP status for an endpoint

* uses asyncio.Lock() to appropriately update increments to up and total responses returned from requests

* within the check_health() function, it has an additional split function by ":" and returns the first element to discard the port used to connect to an endpoint {which ensures the domain being monitored remains the same no matter which port it is listening on}

* uses asyncio and aiohttp to make asynchronous requests every 15 seconds such that there is no blocking at all and no matter what every 15 seconds a request blast is made to all endpoints on the .yaml file