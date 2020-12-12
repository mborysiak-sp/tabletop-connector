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

Run a command inside the docker container:

```bash
docker-compose run --rm web [command]
```
Run tests
```bash
docker-compose run web pytest --cov
```
