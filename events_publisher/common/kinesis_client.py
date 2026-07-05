"""Publish energy events to Kinesis."""

import json
import boto3

def publish_events(events: list[dict],
                   stream_name: str = "energy-sensor-events-dev",
                   region : str = "eu-west-1") -> None:
    """Send events to Kinesis in a single batch (max 500)."""
    client = boto3.client("kinesis", region_name=region)

    records = [
        {
            "Data": json.dumps(event).encode("utf-8"),
            "PartitionKey": event["sensor_id"],
        }
        for event in events
    ]

    response = client.put_records(StreamName=stream_name, Records=records)

    failed = response["FailedRecordCount"]
    print(f"Envoyés : {len(records) - failed}/{len(records)} | Échecs : {failed}")


def events_reader(stream_name: str = "energy-sensor-events-dev",
                  region: str = "eu-west-1") -> None:
    client = boto3.client("kinesis", region_name=region)

    iterator = client.get_shard_iterator(
        StreamName=stream_name,
        ShardId="shardId-000000000000",
        ShardIteratorType="TRIM_HORIZON",
    )["ShardIterator"]

    total = 0
    while iterator:
        response = client.get_records(ShardIterator=iterator, Limit=100)
        records = response["Records"]
        total += len(records)

        for record in records:
            event = json.loads(record["Data"])
            print(f"pk={record['PartitionKey']:20} | {event['measurements']['power_kw']} kW")

        if not records and response.get("MillisBehindLatest", 0) == 0:
            break

        iterator = response.get("NextShardIterator")

    print(f"\n{total} records lus")

events_reader()