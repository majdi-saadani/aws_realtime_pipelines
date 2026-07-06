variable "function_name" {
  description = "Nom de la fonction Lambda"
  type        = string
}

variable "kinesis_stream_arn" {
  description = "ARN du stream Kinesis autorisé en lecture"
  type        = string
}

variable "source_file" {
  description = "Chemin vers le fichier handler.py à packager"
  type        = string
}
variable "dynamodb_table_arn" {
  description = "ARN de la table DynamoDB autorisée en écriture"
  type        = string
}
