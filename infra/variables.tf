variable "project" {
  description = "GCP Project ID"
  type        = string
}

variable "region" {
  description = "GCP Region"
  type        = string
  default     = "us-east1"
}

variable "env" {
  description = "Environment (dev/staging/prod)"
  type        = string
}

variable "zone" {
  description = "GCP Zone"
  type        = string
  default     = "us-east1-a"
}
