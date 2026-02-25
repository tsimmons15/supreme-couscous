#!/bin/bash
set -e

PIPELINE_DIR=$1
TEMPLATE_NAME=$2
PROJECT_ID=$3
REGION=$4

cd $PIPELINE_DIR
python setup.py sdist

TEMPLATE_FILE=$(ls -t dist/*.tar.gz | head -1)
gcloud dataflow templates create \
  --template-location=gs://${PROJECT_ID}-templates/${TEMPLATE_NAME} \
  --template-file=${TEMPLATE_FILE} \
  --region=${REGION}
