output "project_id" {
  value = var.project_id
}

output "raw_bucket_name" {
  value = google_storage_bucket.raw_data.name
}

output "templates_bucket_name" {
  value = google_storage_bucket.templates.name
}

output "web_events_topic" {
  value = google_pubsub_topic.web_events.id
}

output "curated_dataset" {
  value = google_bigquery_dataset.curated.dataset_id
}

output "dataflow_sa_email" {
  value = google_service_account.dataflow_sa.email
}

output "composer_name" {
  value = google_composer_environment.aeo_composer.name
}

output "dags_bucket" {
  value = google_storage_bucket.composer_dags.name
}
