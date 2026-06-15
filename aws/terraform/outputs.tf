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

output "db_endpoint" {
  description = "RDS endpoint (reachable only from the ECS tasks)"
  value       = aws_db_instance.main.address
}
