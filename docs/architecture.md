# Architecture Decision Notes

## 1. Partition key = sensor_id (Kinesis AND DynamoDB)
Per-sensor ordering guarantee end-to-end... trade-off vs random key (better 
load spread, no ordering)...

## 2. Kinesis PROVISIONED vs ON_DEMAND
Known low throughput → 1 provisioned shard (~$14/mo) vs on-demand floor (~$32/mo)...

## 3. Deduplication strategy: best-effort in compute, idempotence in storage
Intra-batch dedup in Lambda (cheap), but the real guarantee is the DynamoDB 
composite key (sensor_id + event_timestamp): writing twice = same result...

## 4. Poison-pill protection
Per-record try/except: one malformed event is rejected and logged instead of 
failing the invocation and blocking the shard in retry loops...

## 5. Validation placement: minimal in hot path, full schema in cold path
Why not Pydantic in the Lambda (packaging weight, latency, cold start) — 
schema enforcement belongs to the Databricks batch layer...

## 6. IAM: least privilege, three lessons
Trust policy vs permissions policy vs PassRole. Deployer scoped to 
`table/energy-*` name prefix. Known debt: AWSLambda_FullAccess to be replaced...