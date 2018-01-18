# NOWPASS Command Line Client

> Please note that NOWPASS is currently in an early alpha stage and not ready for productive use.

This is the python based command line client of the Open Source NOWPASS password manager.


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites

Required software:

* Python 3.x and the following modules
* Python requests module
* [Python Terminaltables >= 3.0](https://pypi.python.org/pypi/terminaltables)

### Installing

Clone the project and install all dependencies needed to run the application (With pip3 or easy_install)

```bash
git clone --depth 1 https://github.com/nowpass/python-cli
```

If you want to use your own [NOWPASS API server](https://github.com/nowpass/server) you need to start it. 

## Running the app

On the first start the application (with any parameter), the one time configuration is started.

You can obtain your API key at your account page. If you use nowpass.org as API server, you can find it 
[here](https://nowpass.org/account).

Check `./nowpass.py --help` for an overview over all commands. 

For more details on the command parameters use `./nowpass.py list --help` with the command word before.

## Available commands

### List passwords

```bash
./nowpass.py list
```

Optional arguments:

```bash
  -p, --passwords  Including passwords
  -t, --today      Elements today
  -j, --json       Output as JSON string
```

### Search for an URL

```bash
./nowpass.py search URL
```


### Add a Login (Interactive)

```bash
./nowpass.py add
```

Optional arguments:

```bash
  -t TITLE,    --title TITLE          Title for the Element
  -u URL,      --url URL              URL for the login
  -p PASSWORD, --password PASSWORD    Set the Password

```

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/nowpass/vue-frontend/tags). 

## License

This project is licensed under the GPLv3 License - see the [LICENSE.md](LICENSE.md) file for details
