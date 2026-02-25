# AEO Data Platform (GCP)

Recreation of American Eagle Outfitters GCP analytics platform using Apache Beam Python, Dataflow, BigQuery, Pub/Sub, and Cloud Composer.

## Architecture
POS/CRM Files → GCS → Dataflow (Beam Python) → BigQuery (partitioned/clustered)
Web Events → Pub/Sub → Dataflow (Beam Python streaming) → BigQuery
Cloud Composer → Orchestrates batch jobs + monitors streaming

## Quick Start
```bash
# Infrastructure (dev)
cd infra
terraform init -backend-config=../environments/dev/backend.tf
terraform apply -var-file=../environments/dev/terraform.tfvars

# Build templates
cd ../pipelines/pos-batch
pip install -r requirements.txt
python setup.py sdist
./../ci-cd/scripts/build-template.sh

# Test locally
aeo-pos-batch --input=gs://test/*.csv --output=test.table --runner=DirectRunner
Environments
dev: Full features, small scale

staging: Production config, synthetic data

prod: Production scale + monitoring