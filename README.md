# JAD Project - Japanese Accent Dictionary Project

This is the project of the NCU class: *"Network and Database Programming"*.


## Contents
- [JAD Project - Japanese Accent Dictionary Project](#jad-project---japanese-accent-dictionary-project)
    - [Contents](#contents)
    - [Usage](#usage)
        - [Prepare](#prepare)
        - [Run](#run)
        - [JAD Shell](#jad-shell)


## Usage

### Prepare

```bash
# Prepare `virtualenv` if needed
pip3 install virtualenv
virtualenv venv -p 3.9  # Use Python 3.9.6 as default
.\venv\Scripts\activate.bat  # For Windows
source venv/bin/activate  # For Linux

# Install the required packages
pip3 install -r requirements.txt
```

### Run

```bash
# Normally run the application
python -m jadcli.main
# Show the simple document of this application
python -m jadcli.main --help
# Able to pass the arguments `-c` and `-v`
python -m jadcli.main -c -v
```

### JAD Shell

```bash
# Print the documents
help
# Exit the applicaiton
exit

# Print the documents of the command `dict`
dict --help
# Print the documents of the command `opt`
opt --help
```
