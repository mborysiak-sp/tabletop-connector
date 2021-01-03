# tabletop-connector

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
