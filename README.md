# Roam
This game allows you to explore a procedurally-generated 2D world and interact with your surroundings.

## Planning Document
The planning document can be found [here](./PLANNING.md)

## Controls
Key | Action
------------ | -------------
w | move up
a | move left
s | move down
d | move right
shift | run
ctrl | crouch
left mouse | gather
right mouse | place
1-0 | select item in hotbar
i | open/close inventory
print screen | take screenshot
esc | quit

## How to run
### Manually
1. If you don't have python installed, install it from [here](https://www.python.org/downloads/).
2. If you don't have git installed, install it from [here](https://git-scm.com/downloads).
3. Clone the repository with the following command:
> git clone https://github.com/Stephenson-Software/Roam.git
4. Install pygame with the following command:
> pip install pygame --pre
5. Install rest of dependencies with the following command:
> pip install -r requirements.txt
6. Run the game with the following command:
> python src/roam.py

### Run Script
There is also a run.sh script you can execute if you're on linux which will automatically attempt to install the dependencies for you.

## Support
You can find the support discord server [here](https://discord.gg/49J4RHQxhy).

## Authors and acknowledgement
### Developers
Name | Main Contributions
------------ | -------------
Daniel McCoy Stephenson | Creator

## Libraries
This project makes use of [graphik](https://github.com/Preponderous-Software/graphik) and [py_env_lib](https://github.com/Preponderous-Software/py_env_lib).
