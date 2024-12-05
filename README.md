<p align="center">
<a href="" rel="noopener"><img src="assets/banner.svg" alt="artipy logo"></a>
</p>
<h3 align="center">artipy</h3>
<div align="center">

![GitHub Release](https://img.shields.io/github/v/release/trumully/artipy.svg?sort=semver&logo=github&logoColor=white)
[![CI Status](https://img.shields.io/github/actions/workflow/status/trumully/artipy/main.yml.svg?logo=github&logoColor=white)](https://github.com/trumully/artipy/actions/workflows/main.yml)
[![Docs Status](https://img.shields.io/github/actions/workflow/status/trumully/artipy/pages%2Fpages-build-deployment?branch=gh-pages&style=flat&logo=github&logoColor=white&label=docs)](https://trumully.github.io/artipy/)
[![License](https://img.shields.io/github/license/trumully/artipy.svg)](LICENSE)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

    
</div>

---

<p align="center">Easily generate Genshin Impact artifacts.
    <br>
</p>

## 📚 Table of Contents
- [About](#about)
- [Getting Started](#getting_started)
- [Deployment](#deployment)
- [Documentation](https://trumully.github.io/artipy/)
- [Usage](#usage)
- [License](LICENSE)
- [Changelog](CHANGELOG.md)
- [Acknowledgements](#acknowledgements)

## 📝 About <a name = "about" ></a>
This is a Python package that can generate Genshin Impact artifacts as close to how they are in the game as possible. It is intended to be used for statistical analysis 

## 📦 Getting Started <a name = "getting_started" ></a>
To install and use the package right away, you can use `pip`:
```shell
python -m pip install -U git+https://github.com/trumully/artipy.git
# or if you don't have 'git' installed:
python3 -m pip install -U https://github.com/trumully/artipy/zipball/main
```

For development, follow the steps below:

### Prerequisites
* Python >=3.13.0
* [uv](https://docs.astral.sh/uv/getting-started/installation/)

### Installing
Clone the repository:
```shell
git clone https://github.com/trumully/artipy.git
```

Install dependencies:
```shell
uv sync
```

## 🧪 Running tests
Run tests using `pytest`:
```shell
uv run pytest
```

## 🔧 Usage <a name ="usage" ></a>
Check out the [documentation](https://trumully.github.io/artipy) for usage examples.

## 🚀 Deployment <a name ="deployment" ></a>
Build the package using `uv`:
```shell
uv build
```
This will create a `tar.gz` and `whl` in the `dist/` directory:
```shell
dist/
├── artipy-(version)-py3-none-any.whl
└── artipy-(version).tar.gz
```

You can install the built package using `pip`:
```shell
python -m pip install -U dist/artipy-(version)-py3-none-any.whl
# or
python -m pip install -U dist/artipy-(version).tar.gz
```

## 🎉 Acknowledgements <a name = "acknowledgements"></a>
✨ Original header image belongs to HoYoverse

✨ The [Genshin Optimizer](https://github.com/frzyc/genshin-optimizer) project for hugely inspiring this project.