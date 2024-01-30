import os
from flask import Flask, jsonify

app = Flask(__name__)


# Expected input: none
# Expected output: version string or error json
@app.route('/version', methods=['GET'])
def version():
    if os.path.isfile("server/version.txt"):
        with open("server/version.txt", "r") as file:
            version = file.read()
            
            if version:
                return version
            else:
                return "{\"error\": \"Version file is empty\"}"
    else:
        return "{\"error\": \"Version file not found\"}"


if __name__ == '__main__':
    app.run(debug=True, port=5000)