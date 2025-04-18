import yaml
import requests
import time
import json
import asyncio
import aiohttp
from collections import defaultdict

# asyncio.Lock() to ensure safe updates to domain_stats
lock = asyncio.Lock()

# Function to assert that the configuration file is of YAML file type
def valid_file_type(config_file):
    if (len(config_file) < 5 or config_file[-5:] != ".yaml"):
        return False
    return True

# Function to load configuration from the YAML file
def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Function to perform health checks
async def check_health(endpoint):
    domain = endpoint["url"].split("//")[-1].split("/")[0].split(":")[0]

    url = endpoint['url']
    method = endpoint.get('method')
    headers = endpoint.get('headers')
    body = endpoint.get('body')

    if method == None:
        method = "GET"
    if body != None:
        body = json.loads(endpoint.get('body'))

    try:
        async with aiohttp.ClientSession() as session:
            start_time = time.perf_counter()
            async with session.request(method, url, headers=headers, json=body) as response:
                end_time = time.perf_counter()
                response_time = (end_time - start_time) * 1000
                if 200 <= response.status < 300 and response_time <= 500:
                    return (domain, "UP")
                else:
                    return (domain, "DOWN")
    except aiohttp.ClientError:
        return (domain, "DOWN")

# Main function to monitor endpoints
async def monitor_endpoints(file_path):
    endpoints = load_config(file_path)
    domain_stats = defaultdict(lambda: {"up": 0, "total": 0})

    while True:
        # the following should always be executed every 15s
        tasks = [check_health(endpoint) for endpoint in endpoints]
        responses = await asyncio.gather(*tasks)

        for response in responses:
            domain = response[0]
            status = response[1]

            async with lock:
                domain_stats[domain]["total"] += 1
                if status == "UP":
                    domain_stats[domain]["up"] += 1

            print("DOMAIN_STATS: ")
            print(dict(domain_stats))

        # Log cumulative availability percentages
        for domain, stats in domain_stats.items():
            availability = round(100 * stats["up"] / stats["total"])
            print(f"{domain} has {availability}% availability percentage")

        print("---")
        time.sleep(15)

# Entry point of the program
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python monitor.py <config_file_path>")
        sys.exit(1)

    config_file = sys.argv[1]

    # assert that the config _file provide is of YAML file type
    if not valid_file_type(config_file):
        print("config_file must be of YAML file type")
        sys.exit(1)

    try:
        asyncio.run(monitor_endpoints(config_file))
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")