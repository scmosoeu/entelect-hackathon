# Entelect Hackathon

This repository contains the main solution code in `main.py`. A companion `.ipynb` notebook is included for experimental exploration only, the working implementation is in `main.py`.

## Setup

Initialise the a new python project

```bash
uv init
```

### Install dependencies with `uv`

Use `uv` to install the dependencies declared in `pyproject.toml`.

```bash
uv sync
```

If `uv` is not installed, follow the official installation instructions for your platform.

## Running the project

### Run the Python file with `uv`

Run the main entrypoint with:

```bash
uv run main_level_2.py
```

The results will be placed in the **output** directory, which will be created if it does not exist.

### Launch JupyterLab with `uv`

If you need to run the notebook for experiments or exploration, launch JupyterLab with:

```bash
uv run jupyter lab
```

> Note: the `.ipynb` notebook is experimental work and is not the primary source of truth. The real code lives in `main_level_2.py`.
