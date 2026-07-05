module "energy_stream" {
  source = "../../modules/kinesis"

  stream_name = "energy-sensor-events-dev"
  shard_count = 1
}