#!/bin/bash

#set -x

# This script will create and set up a Python virtual environment. It requires that you provide an argument when executing it
# which is the name of the virtual environment. You can also set the version of Python that you want to create your virtual environment with.
# Furthermore, you can also specify a list of Python modules that you may want to be installed inside your virtual environment.
# The script as it is will run on debian but can also run on RedHat/Centos by replacing the 'apt-get' command with 'yum'.



RED='\e[1;31m'
GREEN='\e[0;32m'
BLUE='\e[0;96m'
ORANGE='\e[0;33m'
NC='\e[0m' # No Color

SOME_VIRTUAL_ENV="$1"
PYTHON_VERSION="3.6.5"
INSTALLED_PYTHON_VERSIONS=$HOME/python_versions


if [ -z "$(echo $SOME_VIRTUAL_ENV | xargs)" ]
then
	echo -e "${RED}Please provide an installation directory for the virtualenv${NC}"
	exit 1
fi

[[ ! -d $SOME_VIRTUAL_ENV ]] && mkdir -p $SOME_VIRTUAL_ENV
[[ ! -d $INSTALLED_PYTHON_VERSIONS ]] && mkdir -p $INSTALLED_PYTHON_VERSIONS/source \
										  && mkdir -p $INSTALLED_PYTHON_VERSIONS/compiled

function install(){
	wget https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz -O /tmp/Python-${PYTHON_VERSION}.tgz --no-check-certificate
	tar -xzvf /tmp/Python-${PYTHON_VERSION}.tgz -C $INSTALLED_PYTHON_VERSIONS/source
	rm -rf /tmp/Python-${PYTHON_VERSION}.tgz
	cd $INSTALLED_PYTHON_VERSIONS/source/Python-${PYTHON_VERSION} && \
				./configure --enable-shared --prefix=$INSTALLED_PYTHON_VERSIONS/compiled/python${PYTHON_VERSION} \
				LDFLAGS=-Wl,-rpath=$INSTALLED_PYTHON_VERSIONS/compiled/python${PYTHON_VERSION}/lib \
				&& make && make altinstall
	compile_ret=$?
	if [ ! $compile_ret -eq 0 ]
	then
		echo -e "${RED}Failed to compile Python ${PYTHON_VERSION}${NC}" && exit 1
	fi
	
}

if ! which pip > /dev/null 2>&1
then
	echo -e "${GREEN}Installing python-pip on this machine${NC}"
	sudo apt-get install python-pip -y
	if [ ! $? -eq 0 ]
	then
		echo -e "${RED}Failed to install python-pip package${NC}"
		exit 1
	fi
	# below are requirements
	sudo apt-get install zlib1g-dev zlibc gcc libssl-dev -y
	
	if ! which virtualenv > /dev/null 2>&1
	then
		echo -e "${GREEN}Installing virtualenv on this machine${NC}"
		pip install virtualenv --upgrade
		if [ ! $? -eq 0 ]
		then
			echo -e "${RED}Failed to install virtualenv${NC}"
			exit 1
		fi
	fi
fi

if [ ! -d $INSTALLED_PYTHON_VERSIONS/compiled/python${PYTHON_VERSION} ]
then
	echo -e "${GREEN}Installing Python-${PYTHON_VERSION} on this machine${NC}"
	install
	if [ ! $? -eq 0 ]
	then
		echo -e "${RED}Failed to install Python ${PYTHON_VERSION}${NC}" && exit 1
	fi
fi

if [[ ! -f $SOME_VIRTUAL_ENV/bin/activate ]]
then
	echo -e "${GREEN}Creating virtualenv...${NC}"
	virtualenv --python $INSTALLED_PYTHON_VERSIONS/compiled/python${PYTHON_VERSION}/bin/python3.6 $SOME_VIRTUAL_ENV
	if [ ! $? -eq 0 ]
	then
		echo -e "${RED}Failed to create virtualenv${NC}" && exit 1
	fi
fi

# Below is the list of modules to be installed in the virtualenv
source $SOME_VIRTUAL_ENV/bin/activate && pip install beautifulsoup4 requests-ntlm boto3 ConfigParser pymsteams termcolor python-logstash --upgrade > /dev/null 2>&1 && deactivate


# Cleaning up - this must only be present when the virtualenv is being created. After that is not used anymore.
rm -rf $INSTALLED_PYTHON_VERSIONS/source/Python-${PYTHON_VERSION}
