<p align="center">
<a href="" rel="noopener">
<img src="assets/artipy_logo.svg" alt="artipy logo"></a>
</p>
<h3 align="center">artipy</h3>
<div align="center">

![GitHub Release](https://img.shields.io/github/v/release/trumully/artipy.svg?sort=semver&style=for-the-badge&logo=python&logoColor=white)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/trumully/artipy/main.yml.svg?style=for-the-badge&logo=githubactions&logoColor=white)
![License](https://img.shields.io/github/license/trumully/artipy.svg?style=for-the-badge&logo=unlicense&logoColor=white)

</div>

---

<p align="center"> Easily generate Genshin Impact artifacts.
    <br>
</p>

## 📚 Table of Contents
- [About](#📝-about)
- [Getting Started](#📦-getting-started)
- [Deployment](#🚀-deployment)
- [Usage](#⚙️-usage)
- [License](LICENSE)
- [Changelog](CHANGELOG.md)
- [Acknowledgements](#🎉-acknowledgements)

## 📝 About
This is a Python package that can generate Genshin Impact artifacts as close to how they are in the game as possible. It is intended to be used for statistical analysis 

## 📦 Getting Started
To install and use the package right away, you can use `pip`:
```shell
python -m pip install -U git+https://github.com/trumully/artipy.git
# or if you don't have 'git' installed:
python3 -m pip install -U https://github.com/trumully/artipy/zipball/main
```

For development, follow the steps below:

### Prerequisites
To set up a dev environment you'll need `pipx` & `poetry`. Installation instructions for `pipx` on your respective operating system can be found [here](https://pipx.pypa.io/stable/installation/).

Once `pipx` is installed, install `poetry`:
```shell
pipx install poetry
```

### Installing
Clone the repository:
```shell
git clone https://github.com/trumully/artipy.git
```

Activate virtual environment:
```shell
poetry shell
```

Install dependencies:
```shell
poetry install
```

## 🧪 Running tests
Run tests using `pytest`:
```shell
poetry run pytest
```

## ⚙️ Usage
For example usage, look [here](example.py)

## 🚀 Deployment
Build the package using `poetry`:
```shell
poetry build
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

## 🎉 Acknowledgements <a href="acknowledgements"></a>
* Original header image belongs to HoYoverse