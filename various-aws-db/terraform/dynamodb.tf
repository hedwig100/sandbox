resource "aws_dynamodb_table" "main" {
  name         = var.name
  billing_mode = "PAY_PER_REQUEST" # on-demand: no capacity planning for a sandbox
  hash_key     = "pk"

  attribute {
    name = "pk"
    type = "S"
  }

  tags = { Name = var.name }
}

# --- Resource-based policy: lock data access to the VPC endpoint ---
#
# Identity policies (the ECS task role) grant *who* may call DynamoDB. This
# resource policy adds a hard *network* guardrail on the table itself: any
# data-plane request (GetItem/PutItem/Query/...) that did NOT arrive through
# our DynamoDB VPC endpoint is explicitly denied -- including calls made with
# your own admin credentials from a laptop or the AWS console.
#
# Notes:
#   * The Deny is scoped to data actions only, so control-plane actions
#     (DescribeTable, UpdateTable, PutResourcePolicy, ...) that Terraform and
#     the console need keep working from anywhere -- you don't lock yourself
#     out of managing the table.
#   * Access is *granted* purely via the ECS task role's identity policy
#     (see ecs.tf); this policy never grants, it only restricts.
data "aws_iam_policy_document" "table" {
  statement {
    sid    = "DenyDataAccessOutsideVPCEndpoint"
    effect = "Deny"

    principals {
      type        = "AWS"
      identifiers = ["*"]
    }

    actions = [
      "dynamodb:GetItem",
      "dynamodb:BatchGetItem",
      "dynamodb:Query",
      "dynamodb:Scan",
      "dynamodb:PutItem",
      "dynamodb:UpdateItem",
      "dynamodb:DeleteItem",
      "dynamodb:BatchWriteItem",
    ]

    resources = [
      aws_dynamodb_table.main.arn,
      "${aws_dynamodb_table.main.arn}/index/*",
    ]

    condition {
      test     = "StringNotEquals"
      variable = "aws:SourceVpce"
      values   = [aws_vpc_endpoint.dynamodb.id]
    }
  }
}

resource "aws_dynamodb_resource_policy" "main" {
  resource_arn = aws_dynamodb_table.main.arn
  policy       = data.aws_iam_policy_document.table.json
}
