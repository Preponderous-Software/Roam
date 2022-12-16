# py_env_lib
This python library provides base classes for creating 2D virtual worlds.

## Classes
Name | Description
----- | -----
Entity | Represents an entity that can exist in a location.
Environment | Represents a virtual environment with an underlying 2D grid of locations that can contain entities.
Grid | Represents a grid of locations.
Location | Represents a location that can contain entities.

Entities exist in locations. Locations exist in grids. Grids exist in environments. Environments serve as the interface for developers to affect the locations and entities within.

## EnvironmentLib
This project is based on EnvironmentLib, the repository for which can be found [here](https://github.com/Preponderous-Software/EnvironmentLib).