import os

if "ROAM_SERVER_PORT" in os.environ:
    port = os.environ["ROAM_SERVER_PORT"]
else:
    print("ROAM_SERVER_PORT environment variable not set, using default port 5000")
    port = 5000

if "ROAM_SERVER_ADDRESS" in os.environ:
    address = os.environ["ROAM_SERVER_ADDRESS"]
else:
    print("ROAM_SERVER_ADDRESS environment variable not set, using default address localhost")
    address = "localhost"

print(f"Listening on {address}:{port}")
url = f"http://{address}:{port}"


def getVersion():
    toReturn = os.popen("curl " + url + "/version").read()
    if toReturn:
        return toReturn
    else:
        return "Could not retrieve version from server"