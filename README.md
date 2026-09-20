# Pax

## Overview

Pax (*"peace"* in Latin) is a Python-based web application that provides a set of interfaces to facilitate joint users in planning and evaluating courses of action within a mission environment. As such, it allows users to oversee and prepare for missions that combine cyber and physical components. Courses of action are evaluated based on the time taken to achieve the mission, the probability of success, what the enemy is preparing to do and the risk inherent within the course of action.

**Research.** We use [game theory](https://en.wikipedia.org/wiki/Game_theory) as our main set of tools for evaluating the risk inherent within a course of action. Research was conducted in constructing the theory and algorithms around the Pax project. This research can be found in the [`NetworkDefence`](https://github.com/O1sims/NetworkDefence) repository. This article develops an attack-defence game within a topological structure.

## Technology stack

The Python web application uses [Django](https://www.djangoproject.com/) as the backend framework and [Angular](https://angular.io/) as the frontend framework. Documentation of the RESTful API service is handled by [Swagger](https://swagger.io/). Development is done within a [Docker](https://www.docker.com/) environment. We use [MongoDB](https://www.mongodb.com/) as the main database and [MongoDB Compass](https://www.mongodb.com/products/compass) as the database GUI.

## Building the application

We use Docker in the development of Pax to make it easy to build, run and share. The application is built across two Docker containers — a Django backend (`pax:latest`) and an Angular frontend (`pax-gui:latest`), each with its own Dockerfile under `src/backend/` and `src/webserver/`. From the root directory of the Pax application:
```
./build.sh all
```
This builds both images (equivalent to `docker build -t pax:latest src/backend/.` and `docker build -t pax-gui:latest src/webserver/.`), including the installation of the relevant Python and Node packages. To manually install Node packages instead, ensure you have Node (NPM) and install the frontend packages by executing the following commands from the root directory:
```
cd src/webserver/gui/app
npm install
```
The Typescript (`.ts`) files can be compiled, as normal, with the `tsc` command.

## Running the application

Running the application is different from building the application. The application is run with the following command from the root directory:
```
./build.sh up
```
(equivalent to `docker-compose up` from `src/`). By default, the backend API is accessible on port `8200` and the frontend GUI on port `3000`, with MongoDB on port `8210`. Swagger API documentation can be found at `localhost:8200/swagger/`; the application itself is at `localhost:3000`.

The env vars each service is started with — `DB_PORT`, `DB_HOSTNAME`, `DB_NAME`, `UI_PORT`, `PAX_PORT`, `PAX_HOSTNAME`, etc. — are defined in [`src/docker-compose.yml`](src/docker-compose.yml), which is the source of truth for them; edit that file to change ports or hostnames.

## Contact

The best way to troubleshoot or ask for a new feature or enhancement is to create a Github [issue](https://github.com/O1sims/Pax/issues). However, if you have any further questions you can contact [me](mailto:sims.owen@gmail.com) directly.
