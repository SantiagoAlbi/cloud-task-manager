output "vpc_id" {
  value = aws_vpc.main.id
}

output "public_subnets" {
  value = aws_subnet.public[*].id
}

output "private_subnets" {
  value = aws_subnet.private[*].id
}

output "ecr_backend_url" {
  value = aws_ecr_repository.backend.repository_url
}

output "ecr_frontend_url" {
  value = aws_ecr_repository.frontend.repository_url
}

output "cluster_name" {
  value = aws_eks_cluster.main.name
}

output "cluster_endpoint" {
  value = aws_eks_cluster.main.endpoint
}

output "cluster_version" {
  value = aws_eks_cluster.main.version
}

output "db_endpoint" {
  value = aws_db_instance.main.address
}

output "db_secret_name" {
  value = aws_secretsmanager_secret.db_credentials.name
}

output "backend_role_arn" {
  value = aws_iam_role.backend_pod.arn
}

output "lbc_role_arn" {
  value = aws_iam_role.lbc.arn
}
