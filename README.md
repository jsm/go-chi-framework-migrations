# Users

## Setup
* Install [Docker for OSX](https://docs.docker.com/docker-for-mac/install/)
* Install [Homebrew](https://brew.sh/)

## Deploying to dev
* Increase version number.
* Make pull request and merge the version number change.
* Run `make deploy-dev`.
* Create release notes for the newly created release tag.

## Promoting to Prod
1. Go to the AWS interface for the `users` app.
1. Select `Application Versions`
1. Select the version to deploy.
1. Hit the `Deploy` button.
1. Select the environment (`users-prod`).
