# get the latest version of the code
echo "Pulling latest version of code from GitHub"
git pull

# print branch status
echo "Current branch: $(git branch --show-current)"

# check that dependencies are installed
echo "Checking dependencies"
pip install pygame --pre
pip install -r requirements.txt

# start program
echo "Starting program"
python src/roam.py