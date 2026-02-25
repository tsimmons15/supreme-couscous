# Dataflow Service Account
resource "google_service_account" "dataflow_sa" {
  account_id   = "aeo-dataflow-${var.env}"
  display_name = "AEO Dataflow Service Account (${var.env})"
}

resource "google_project_iam_member" "dataflow_sa_roles" {
  for_each = toset([
    "roles/dataflow.worker",
    "roles/dataflow.developer",
    "roles/dataflow.jobUser",
    "roles/bigquery.dataEditor",
    "roles/bigquery.jobUser",
    "roles/storage.objectAdmin",
    "roles/pubsub.subscriber",
    "roles/logging.logWriter"
  ])
  project = var.project_id
  role    = each.key
  member  = "serviceAccount:${google_service_account.dataflow_sa.email}"
}

# POS Batch Dataflow Job
resource "google_dataflow_job" "pos_batch" {
  name                    = "aeo-pos-batch-${var.env}"
  template_gcs_path       = "gs://${var.project_id}-templates-${var.env}/pos_batch_template"
  project_id              = var.project_id
  region                  = var.region
  zone                    = "${var.region}-a"
  
  parameters = {
    input  = "gs://${google_storage_bucket.raw_data.name}/*.csv"
    output = "${var.project_id}:${google_bigquery_dataset.curated.dataset_id}.pos_sales_fact"
  }

  service_account_email = google_service_account.dataflow_sa.email
  
  depends_on = [
    google_storage_bucket.templates,
    google_storage_bucket.raw_data,
    google_project_service.apis
  ]
}

# Web Streaming Dataflow Job
resource "google_dataflow_job" "web_streaming" {
  name                    = "aeo-web-streaming-${var.env}"
  template_gcs_path       = "gs://${var.project_id}-templates-${var.env}/web_streaming_template"
  project_id              = var.project_id
  region                  = var.region
  
  parameters = {
    input_topic  = "projects/${var.project_id}/topics/${google_pubsub_topic.web_events.name}"
    output_table = "${var.project_id}:${google_bigquery_dataset.curated.dataset_id}.web_events_fact"
  }

  service_account_email = google_service_account.dataflow_sa.email
  on_delete             = "drain"
  
  depends_on = [
    google_storage_bucket.templates,
    google_pubsub_topic.web_events,
    google_project_service.apis
  ]
}
