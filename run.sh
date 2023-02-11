# /bin/bash
# Usage: ./run.sh

getLatest() {
    # get the latest version of the code
    echo "Pulling latest version of code from GitHub"
    git pull
}

printBranchStatus() {
    # print the current branch
    echo "Current branch: $(git branch --show-current)"
}

printVersion() {
    # print the current version
    echo "Current version: $(cat version.txt)"
}

checkDependencies() {
    # check that dependencies are installed
    echo "Checking dependencies"
    if ! command -v python &> /dev/null
    then
        echo "Python could not be found. Download it from https://www.python.org/downloads/"
        exit
    fi
    if ! command -v pip &> /dev/null
    then
        echo "Pip could not be found. Download it from https://pip.pypa.io/en/stable/installation/ or run 'python -m ensurepip' in a terminal"
        exit
    fi
    pip install pygame --pre --quiet
    pip install -r requirements.txt --quiet
}

startProgram() {
    # start program
    echo "Starting program"
    python src/roam.py > output.txt
}

# main
getLatest
printBranchStatus
printVersion
checkDependencies
startProgram