output "alb_url" {
  description = "Public URL of the ALB"
  value       = "http://${aws_lb.main.dns_name}"
}

output "ecr_repository_url" {
  description = "ECR repository to push the image to"
  value       = aws_ecr_repository.main.repository_url
}

output "region" {
  value = var.region
}

output "cluster_name" {
  value = aws_ecs_cluster.main.name
}

output "service_name" {
  value = aws_ecs_service.main.name
}

output "dynamodb_table" {
  description = "DynamoDB table (reachable only through the VPC endpoint, from the ECS task role)"
  value       = aws_dynamodb_table.main.name
}

output "dynamodb_vpc_endpoint_id" {
  description = "The only network path allowed to the table's data plane"
  value       = aws_vpc_endpoint.dynamodb.id
}
