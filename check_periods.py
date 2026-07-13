import json

# Read the boundaries file in chunks to avoid memory issues
with open('data/historical_boundaries.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Get unique period IDs from first 100 entries
period_ids = set()
for boundary in data['boundaries'][:100]:
    period_ids.add(boundary['period_id'])

print("Sample period IDs from historical_boundaries.json:")
for pid in sorted(period_ids)[:20]:
    print(f"  {pid}")

print(f"\nTotal unique period IDs in first 100 entries: {len(period_ids)}")
