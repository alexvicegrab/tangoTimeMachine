Provisioning a new site
=======================

## Required packages:

* nginx
* Python 3
* Git
* pip
* virtualenv

e.g. on Ubuntu:

	sudo apt-get install nginx git python3 python3-pip
	sudo pip3 install virtualenv

## Nginx Virtual Host config

* see nginx.template.config
* replace SITENAME with, e.g. myDomain-staging.com
* replace USERNAME

## Upstart Job

* see gunicorn-upstart.template.conf
* replace SITENAME with, e.g. myDomain-staging.com
* replace USERNAME

## Folder structure:

Assume we have a user account at /home/USERNAME

/home/USERNAME/sites

tangoTimeMachine
├── database
├── source
│   ├── deploy_tools
│   ├── djangoProject
│   ├── functional_tests
│   └── tangoAds
├── static
│   └── bootstrap
└── virtualenv
    ├── bin
    ├── include
    └── lib