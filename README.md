# tabletop-connector

[![Build Status](https://travis-ci.org/mborysiak-sp/tabletop-connector.svg?branch=main)](https://travis-ci.org/mborysiak-sp/tabletop-connector)
[![Built with](https://img.shields.io/badge/Built_with-Cookiecutter_Django_Rest-F7B633.svg)](https://github.com/agconti/cookiecutter-django-rest)

None. Check out the project's [documentation](http://mborysiak-sp.github.io/tabletop-connector/).

# Prerequisites

- [Docker](https://docs.docker.com/docker-for-mac/install/)  

# Local Development

Start the dev server for local development:
```bash
docker-compose up
```
Get games from API:
```bash
docker-compose run web python games_downloader.py
```
Add games to database:
```bash
docker-compose run web python run_load_games.py
```
Run tests
```bash
docker-compose run web pytest --cov
```
Run black
```bash
docker-compose run web black tabletop_connector_api/
```
