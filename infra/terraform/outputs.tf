output "public_ip_address" {
  value = azurerm_public_ip.public_ip.ip_address
}

output "web_url" {
  value = "http://${azurerm_public_ip.public_ip.ip_address}:5000"
}