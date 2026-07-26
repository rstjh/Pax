FROM node:latest

# Install dependencies into /gui/app, matching the layout docker-compose mounts at
# runtime (./webserver/gui/:/gui/) — index.html lives in gui/ and references
# ./app/node_modules/... relatively, so node_modules must stay under app/, not /gui/.
RUN mkdir -p /gui/app
WORKDIR /gui/app
ADD /gui/app/package.json /gui/app/

RUN apt-get update -qq && apt-get install -y build-essential nodejs
RUN npm install --legacy-peer-deps npm-check-updates
# --ignore-scripts: package.json's postinstall ("types install") references a binary
# that doesn't exist in the "typings" package (it's actually "typings install"), and
# has been broken for years.
RUN npm install --legacy-peer-deps --ignore-scripts

# lite-server serves its cwd as webroot; run it from /gui (where index.html lives)
# using the binary installed under app/node_modules.
WORKDIR /gui
CMD ["./app/node_modules/.bin/lite-server"]

# Expose ports
EXPOSE 3000
