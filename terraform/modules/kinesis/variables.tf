variable "stream_name" {
  description = "Nom du stream Kinesis côté AWS"
  type        = string
}

variable "shard_count" {
  description = "Nombre de shards (1 shard = 1 MB/s en écriture)"
  type        = number
  default     = 1
}

variable "retention_hours" {
  description = "Rétention des records en heures (24 = minimum, gratuit)"
  type        = number
  default     = 24
}