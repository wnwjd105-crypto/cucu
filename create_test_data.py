import json
import ijson

# Create a smaller test dataset with only first few periods
test_boundaries = []
period_count = 0
max_periods = 10

with open('data/historical_boundaries.json', 'r', encoding='utf-8') as f:
    parser = ijson.parse(f)
    current_boundary = {}
    seen_periods = set()
    
    for prefix, event, value in parser:
        if prefix == 'boundaries.item.period_id':
            current_boundary['period_id'] = value
        elif prefix == 'boundaries.item.start_year':
            current_boundary['start_year'] = value
        elif prefix == 'boundaries.item.end_year':
            current_boundary['end_year'] = value
        elif prefix == 'boundaries.item.regions':
            if 'period_id' in current_boundary:
                pid = current_boundary['period_id']
                if pid not in seen_periods and period_count < max_periods:
                    seen_periods.add(pid)
                    period_count += 1
                    # Add this boundary to test data
                    test_boundaries.append({
                        'period_id': pid,
                        'start_year': current_boundary['start_year'],
                        'end_year': current_boundary['end_year'],
                        'regions': value
                    })
                    print(f"Added period {period_count}: {pid}")
            current_boundary = {}

result = {"boundaries": test_boundaries}

with open('data/historical_boundaries_test.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"\nCreated test file with {len(test_boundaries)} periods")
