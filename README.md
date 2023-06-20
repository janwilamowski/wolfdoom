# WolfDoom

A Wolfenstein (pseudo) 3D game prototype written in Python, using a software renderer and ray
tracing. Based on https://github.com/StanislavPetrovV/DOOM-style-Game.

## Setup

- Install Conda
- `conda env create -f env.yml`
- compile Cython modules: `python setup.py build_ext --inplace`

## Play

- `conda activate wolfdoom`
- `python main.py`
