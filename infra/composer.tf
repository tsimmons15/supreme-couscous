# Cloud Composer (Airflow)
resource "google_composer_environment" "aeo_composer" {
  name   = "aeo-composer-${var.env}"
  region = var.region
  labels = {
    environment = var.env
  }

  config {
    node_config {
      zone         = "${var.region}-a"
      machine_type = var.env == "prod" ? "n1-standard-4" : "n1-standard-2"
    }

    database_config {
      machine_type = "db-n1-standard-2"
    }

    web_server_config {
      machine_type = "composer-2airflow-2"
    }

    software_config {
      image_version  = "composer-3-airflow-2"
      airflow_config_overrides = {
        core-load_default_connections = "false"
        core-dags_are_paused_at_creation = "true"
      }
      pypi_packages = {
        "apache-beam[gcp]==2.59.0" = ""
      }
    }

    environment_size = var.env == "prod" ? "LARGE" : "SMALL"
  }

  depends_on = [google_project_service.apis]
}

# Composer DAGs Bucket
resource "google_storage_bucket" "composer_dags" {
  name     = "${var.project}-aeo-composer-${var.env}"
  location = var.region
  force_destroy = var.env != "prod"
}
