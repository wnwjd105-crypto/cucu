import json
import ijson

# Extract period IDs and their year ranges using ijson
period_data = {}

with open('data/historical_boundaries.json', 'r', encoding='utf-8') as f:
    parser = ijson.parse(f)
    current_boundary = {}
    
    for prefix, event, value in parser:
        if prefix == 'boundaries.item.period_id':
            current_boundary['period_id'] = value
        elif prefix == 'boundaries.item.start_year':
            current_boundary['start_year'] = value
        elif prefix == 'boundaries.item.end_year':
            current_boundary['end_year'] = value
        elif prefix == 'boundaries.item.regions':
            # End of a boundary item
            if 'period_id' in current_boundary:
                pid = current_boundary['period_id']
                if pid not in period_data:
                    period_data[pid] = {
                        'start_year': current_boundary['start_year'],
                        'end_year': current_boundary['end_year']
                    }
            current_boundary = {}

# Create time periods JSON
periods = []
for pid in sorted(period_data.keys()):
    data = period_data[pid]
    start_year = data['start_year']
    end_year = data['end_year']
    
    # Generate name and description
    if start_year < 0 and end_year < 0:
        name = f"기원전 {abs(start_year)//100 + 1}세기-{abs(end_year)//100 + 1}세기"
        description = f"기원전 {abs(start_year)}년-{abs(end_year)}년"
    elif start_year >= 0 and end_year >= 0:
        name = f"기원후 {start_year//100 + 1}세기-{end_year//100 + 1}세기"
        description = f"기원후 {start_year}년-{end_year}년"
    else:
        name = f"기원전 {abs(start_year)}년-기원후 {end_year}년"
        description = f"기원전 {abs(start_year)}년-기원후 {end_year}년"
    
    periods.append({
        "id": pid,
        "name": name,
        "start_year": start_year,
        "end_year": end_year,
        "description": description
    })

result = {"periods": periods}

with open('data/time_periods.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"Created time_periods.json with {len(periods)} periods")
print("Sample periods:")
for p in periods[:10]:
    print(f"  {p['id']}: {p['name']}")
