terraform {
  required_version = ">= 1.5"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
  zone    = "${var.region}-a"
}

# VPC Network
resource "google_compute_network" "aeo_vpc" {
  name                    = "aeo-${var.env}-vpc"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "aeo_subnet" {
  name          = "aeo-${var.env}-subnet"
  ip_cidr_range = "10.${var.env == "prod" ? 10 : 20}.0.0/20"
  region        = var.region
  network       = google_compute_network.aeo_vpc.id
}

# Cloud Storage Buckets
resource "google_storage_bucket" "raw_data" {
  name                        = "${var.project_id}-aeo-raw-data-${var.env}"
  location                    = var.region
  force_destroy               = var.env != "prod"
  uniform_bucket_level_access = true

  lifecycle_rule {
    condition {
      age = 30
    }
    action {
      type = "Delete"
    }
  }
}

resource "google_storage_bucket" "templates" {
  name                        = "${var.project_id}-templates-${var.env}"
  location                    = var.region
  force_destroy               = true
  uniform_bucket_level_access = true
}

# Pub/Sub Topics
resource "google_pubsub_topic" "web_events" {
  name = "aeo-web-events-${var.env}"
}

# BigQuery Datasets
resource "google_bigquery_dataset" "raw" {
  dataset_id                  = "aeo_raw_${var.env}"
  location                    = var.region
  delete_contents_on_destroy  = var.env != "prod"
}

resource "google_bigquery_dataset" "curated" {
  dataset_id                  = "aeo_curated_${var.env}"
  location                    = var.region
  delete_contents_on_destroy  = var.env != "prod"
}

# BigQuery Tables
resource "google_bigquery_table" "pos_sales_fact" {
  dataset_id = google_bigquery_dataset.curated.dataset_id
  table_id   = "pos_sales_fact"
  deletion_protection = var.env == "prod" ? true : false

  time_partitioning {
    type   = "DAY"
    field  = "transaction_date"
  }

  clustering = ["store_id", "product_id"]
}

resource "google_bigquery_table" "web_events_fact" {
  dataset_id = google_bigquery_dataset.curated.dataset_id
  table_id   = "web_events_fact"
  deletion_protection = var.env == "prod" ? true : false

  time_partitioning {
    type   = "DAY"
    field  = "event_date"
  }

  clustering = ["session_id", "user_id"]
}

# Enable required APIs
