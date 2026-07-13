import json
import ijson

# Extract period IDs using ijson to avoid memory issues
period_ids = set()

with open('data/historical_boundaries.json', 'r', encoding='utf-8') as f:
    # Parse the file incrementally
    parser = ijson.parse(f)
    current_period_id = None
    
    for prefix, event, value in parser:
        if prefix == 'boundaries.item.period_id':
            period_ids.add(value)
            if len(period_ids) % 50 == 0:
                print(f"Found {len(period_ids)} unique period IDs so far...")

print(f"\nTotal unique period IDs: {len(period_ids)}")
print("\nAll period IDs:")
for pid in sorted(period_ids):
    print(f"  {pid}")
