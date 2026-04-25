variable "resource_group_name" {
  default = "rg-labor-costs-lab4"
}

variable "location" {
  default = "swedencentral"
}

variable "vm_name" {
  default = "vm-labor-costs"
}

variable "admin_username" {
  default = "azureuser"
}

variable "repo_url" {
  description = "GitHub repository URL"
  type        = string
}