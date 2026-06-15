resource "aws_db_subnet_group" "main" {
  name       = var.name
  subnet_ids = aws_subnet.private[*].id
}

# Master password: generated, never hardcoded, stored in Secrets Manager.
resource "random_password" "db" {
  length  = 24
  special = false # keep it URL/CLI safe for a practice setup
}

resource "aws_secretsmanager_secret" "db_password" {
  name                    = "${var.name}/db-password"
  recovery_window_in_days = 0 # delete immediately on destroy (practice)
}

resource "aws_secretsmanager_secret_version" "db_password" {
  secret_id     = aws_secretsmanager_secret.db_password.id
  secret_string = random_password.db.result
}

resource "aws_db_instance" "main" {
  identifier     = var.name
  engine         = "postgres"
  engine_version = "16"
  instance_class = var.db_instance_class

  allocated_storage = 20
  storage_type      = "gp3"
  storage_encrypted = true

  db_name  = var.db_name
  username = var.db_username
  password = random_password.db.result

  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.db.id]
  publicly_accessible    = false
  multi_az               = false # single-AZ to keep practice costs down

  skip_final_snapshot = true
  deletion_protection = false
}
