# sre-take-home-exercise-python-blightjl
Changes made to the main.py file:

bugs found:
> running requests.request when Method is empty from the sample.yaml file
    > should simply return "DOWN" when this is the case
> added a function to check the argument being passed in to be of type yaml file
