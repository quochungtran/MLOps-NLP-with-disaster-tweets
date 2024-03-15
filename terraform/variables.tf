// Variables to use accross the project
// which can be accessed by var.project_id
variable "project_id" {
  description = "The project ID to host the cluster in"
  default     = "mlops-415023"
}

variable "region" {
  description = "The region the cluster in"
  default     = "europe-west4-a"
}