#!/usr/bin/env bash

set -ex

deploy-to-region () {
  AWS_ACCOUNT_ID=0000000000000
  ECR_REPO=$AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/migrations
  EB_BUCKET=$AWS_ACCOUNT_ID-eb-$REGION-versions

  docker tag $SHA1 $ECR_REPO:$VERSION
  docker push $ECR_REPO:$VERSION

  # Create new Elastic Beanstalk version
  sed "s/<TAG>/$VERSION/" < eb/Dockerrun.aws.json.template > eb/Dockerrun.aws.json
  (cd eb && zip -r ../$VERSION.zip .)
  aws s3 cp $VERSION.zip s3://$EB_BUCKET/$APPLICATION_NAME/$VERSION.zip
  aws --region $REGION elasticbeanstalk create-application-version --application-name $APPLICATION_NAME \
    --version-label $VERSION --source-bundle S3Bucket=$EB_BUCKET,S3Key=$APPLICATION_NAME/$VERSION.zip

  sleep 10

   aws --region $REGION elasticbeanstalk update-environment --application-name $APPLICATION_NAME --environment-name $APPLICATION_NAME-dev --version-label $VERSION
}

SHA1=$1
VERSION=$2
APPLICATION_NAME=users
DOCKERRUN_FILE=$SHA1-Dockerrun.aws.json

# Deploy to us-east-1
REGION=us-east-1 deploy-to-region
