FROM python:3.5

# Set up apt-get
RUN apt-get -qq update

# Download Python framework and dependencies
RUN apt-get -y install -qq -y build-essential libffi-dev python-dev

# Set up Django framework
RUN mkdir /Pax
WORKDIR /Pax
ADD requirements.txt /Pax/
RUN pip3 install -r requirements.txt

# Add the Pax directory
ADD . /Pax/

# Expose ports
EXPOSE 8210
