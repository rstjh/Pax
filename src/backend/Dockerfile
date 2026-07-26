FROM python:3.5

# Debian buster is EOL and deb.debian.org/security.debian.org no longer serve it;
# switch to the pinned snapshot mirror already listed (commented out) in this base image.
RUN sed -i -e '/snapshot.debian.org/s/^# //' \
           -e '/^deb http:\/\/deb.debian.org/d' \
           -e '/^deb http:\/\/security.debian.org/d' \
           /etc/apt/sources.list

# Set up apt-get
RUN apt-get -qq update -o Acquire::Check-Valid-Until=false

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
