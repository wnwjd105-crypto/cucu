import json

# Read the boundaries file
with open('data/historical_boundaries.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Get all unique period IDs
period_ids = sorted(set(b['period_id'] for b in data['boundaries']))

print("All unique period IDs from historical_boundaries.json:")
for pid in period_ids:
    print(f"  {pid}")

print(f"\nTotal unique period IDs: {len(period_ids)}")
