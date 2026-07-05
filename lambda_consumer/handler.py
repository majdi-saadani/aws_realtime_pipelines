"""Kinesis consumer: dedup + filter negative readings."""

import base64
import json
from typing import Any


def lambda_handler(event: dict[str, Any], context: Any) -> dict[str, int]:
    """Process a batch of Kinesis records.

    Pipeline per record:
    1. Decode & parse (rejected if malformed -> poison pill protection)
    2. Dedup on event_id (within batch)
    3. Filter negative power readings (faulty sensor)
    """
    seen_ids: set[str] = set()
    valid_events: list[dict[str, Any]] = []
    duplicates = 0
    negatives = 0
    rejected = 0

    for record in event["Records"]:
        # 1. Décodage + validation minimale (anti poison-pill)
        try:
            payload = base64.b64decode(record["kinesis"]["data"])
            energy_event = json.loads(payload)
            event_id = energy_event["event_id"]
            power_kw = energy_event["measurements"]["power_kw"]
        except (KeyError, json.JSONDecodeError, TypeError) as exc:
            rejected += 1
            print(f"REJECTED: {exc!r}")
            continue

        # 2. Dedup sur event_id
        if event_id in seen_ids:
            duplicates += 1
            continue
        seen_ids.add(event_id)

        # 3. Filtrage des mesures négatives (capteur défaillant)
        if power_kw < 0:
            negatives += 1
            continue

        valid_events.append(energy_event)

    print(f"Batch: {len(event['Records'])} reçus | "
          f"{duplicates} doublons | {negatives} négatifs | "
          f"{rejected} rejetés | {len(valid_events)} valides")


    return {
        "received": len(event["Records"]),
        "duplicates": duplicates,
        "negatives": negatives,
        "rejected": rejected,
        "valid": len(valid_events),
    }