output "public_ip" {
  description = "Public IP address of the FoodExpress EC2 instance"
  value       = aws_instance.foodexpress_server.public_ip
}
