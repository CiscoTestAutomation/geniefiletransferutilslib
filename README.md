# Genie File Transfer Utilities

This library contains the open-source library used in pyATS/Genie for
transferring files from devices/to servers.


## About

Genie is both a library framework and a test harness that facilitates rapid
development, encourage re-usable and simplify writing test automation. Genie
bundled with the modular architecture of pyATS framework accelerates and
simplifies test automation leveraging all the perks of the Python programming
language in an object-orienting fashion.

pyATS is an end-to-end testing ecosystem, specializing in data-driven and
reusable testing, and engineered to be suitable for Agile, rapid development
iterations. Extensible by design, pyATS enables developers to start with small,
simple and linear test cases, and scale towards large, complex and asynchronous
test suites.

Genie was initially developed internally in Cisco, and is now available to the
general public starting early 2018 through [Cisco DevNet].

[Cisco Devnet]: https://developer.cisco.com/

This is a sub-component of Genie that contains utility functions for a file
transfer to/from server.

# Installation

This package is automatically installed when Genie gets installed.

```bash
bash$ pip install genie
```

Detailed installation guide can be found on [our website].

[our website]: https://developer.cisco.com/site/pyats/


# Development

To develop this package, assuming you have Genie already installed in your
environment, follow the commands below:

```bash
# remove the packages
bash$ pip uninstall -y genie.libs.filetransferutils

# clone this repo
bash$ git clone https://github.com/CiscoTestAutomation/geniefiletransferutilslib.git

# put all packages in dev mode
bash$ cd genielibs
bash$ make develop
```

Now you should be able to develop the files and see it reflected in your runs.