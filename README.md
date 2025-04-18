# sre-take-home-exercise-python-blightjl

### Intalling and running the code:

1. Download the source code
2. Change directory into the source code
3. Create a local virtual environment by running the following: python3 -m venv venv
4. Activate the virtual environment by running: source venv/bin/acitivate
5. Now ensure these modules are downloaded in the environment: yaml, asyncio, aiohttp, json, requests, time
6. If any are missing, install them via the following command: pip install <missing_module_name>
7. Run the program with the following: python3 main.py sample.yaml
8. To stop the program enter the following keys: Control + C
9. To exit out of the activated environment run: deactivate

### Issues addressed and code changes:

Changes made to the main.py file:

bugs found:
> running requests.request when Method is empty from the sample.yaml file
    > should simply return "DOWN" when this is the case
> added a function to check the argument being passed in to be of type yaml file
