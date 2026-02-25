terraform {
  backend "gcs" {
    bucket      = "aeo-tf-state"  # Override in environments/* 
    prefix      = "terraform/${var.env}"
  }
}
