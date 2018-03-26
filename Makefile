export PATH := ./bin:$(PATH)
export SHELL := /bin/bash

.PHONY: githooks run migrate-db tag deploy-version-check check-alembic

migrate-db:
	alembic upgrade head

githooks:
	rm -rf .git/hooks
	ln -sf ../githooks .git/hooks

deploy-version-check: VERSION=$(shell cat VERSION)
deploy-version-check:
	@if aws elasticbeanstalk describe-application-versions --application-name users | jq ".ApplicationVersions[] | .VersionLabel" | grep -F $(VERSION) > /dev/null 2>&1; then \
		cecho -br "Version $(VERSION) already exists as an Application Version" && exit 1; fi

tag: VERSION=$(shell cat VERSION)
tag:
	git tag $(VERSION)
	git push origin $(VERSION)

primordia:
	@docker network inspect primordia > /dev/null 2>&1 || (echo 'Creating Docker Network' && docker network create primordia)

run: primordia
	bash -c "trap 'docker-compose down' EXIT; docker-compose up --build"

check-alembic:
	@cecho -bc "Checking for duplicate alembic down revisions"
	@OUTPUT=$$(grep -h down_revision alembic/versions/*.py | sort | uniq -d) && \
		if [[ $$OUTPUT ]]; then \
			echo "$$OUTPUT" && \
			cecho -br "There are duplicate down revisions" && \
			exit 1; \
		else \
			cecho -bg "Alembic OK"; \
		fi

upgrade:
	docker-compose run --entrypoint alembic migrate upgrade head

downgrade:
	docker-compose run --entrypoint alembic migrate downgrade -1
