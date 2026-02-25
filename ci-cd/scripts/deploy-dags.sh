#!/bin/bash
set -e

COMPOSER_NAME=$1
PROJECT_ID=$2
REGION=$3
BUCKET=$4

echo "Deploying DAGs to Composer $COMPOSER_NAME"

# Upload DAGs
gsutil -m rsync -d dags/ gs://$BUCKET/dags/

# Restart scheduler (if needed)
gcloud composer environments update $COMPOSER_NAME \
    --location $REGION \
    --update-airflow-configs=web_server.web_server_access_log_max_files=100
