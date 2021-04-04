# RecSys

## API

### Local Dev.

Requirement: `Docker`, `docker-compose` (make sure docker has plenty of
resources - cpu, mem)

From the root type `make deploy`.

This will trigger the elasticsearch cluster to spin up, the service to spin
up/create the index, and the model to train and write predictions. Should take
about 5 minutes for the endpoint to be ready (maybe less depending on your
machine.)

#### Sample Queries

In your browser you can hit the following endpoints to see the results.

1. Get similar users [http://localhost:8000/users/3](http://localhost:8000/users/3)
2. Get similar users that have done something with Java [http://localhost:8000/users/3?q=java](http://localhost:8000/users/3?q=java)
3. Get 20 similar users [http://localhost:8000/users/3?size=20](http://localhost:8000/users/3?size=20)

### Docs

API docs can be found at [http://localhost:8000/docs](http://localhost:8000/docs)

## Notebooks

### Local Dev.

- `make notebook-up`
- copy the url output to your browser to open the notebooks
- `ctrl-c` to quit
