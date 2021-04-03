.PHONY: notebook-image, notebook

# ----------------------------------------------------------------------------
# VARIABLES
#  All images will be tagged with `latest` for ease of use in the local dev
#  system.

PROJECT=recsys
TAG=latest

# ----------------------------------------------------------------------------
# NOTEBOOK HELPERS
notebook-image:
	docker build -f docker/notebook.Dockerfile -t $(PROJECT)/notebook:$(TAG) .

notebook-up: notebook-image
	docker-compose -f notebooks/docker-compose.yaml up --remove-orphans


