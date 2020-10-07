FROM node:latest

# Install dependencies
RUN mkdir /gui
WORKDIR /gui
ADD /gui/app/package.json /gui/
#RUN npm install

RUN apt-get update -qq && apt-get install -y build-essential nodejs
RUN npm install npm-check-updates
RUN npm install

# NPM start
CMD npm view package.json
CMD npm install npm@latest -g
CMD npm audit fix
#CMD npm run lite

# Expose ports
EXPOSE 3000
