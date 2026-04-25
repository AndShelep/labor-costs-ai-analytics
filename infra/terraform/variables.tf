variable "resource_group_name" {
  default = "labor-costs-rg"
}

variable "location" {
  default = "westeurope"
}

variable "vm_name" {
  default = "labor-costs-vm"
}

variable "admin_username" {
  default = "shelep"
}

variable "repo_url" {
  description = "GitHub repository URL"
  type        = string
}