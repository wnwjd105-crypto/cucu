import json
import os

def get_period_id(from_year, to_year):
    """
    연도 범위를 기반으로 시대 ID 생성
    """
    if from_year < 0 and to_year < 0:
        # 기원전
        century_from = abs(from_year) // 100 + 1
        century_to = abs(to_year) // 100 + 1
        if century_from == century_to:
            return f"ancient_{century_from}th_century_bce"
        return f"ancient_{century_from}th_{century_to}th_century_bce"
    elif from_year >= 0 and to_year >= 0:
        # 기원후
        century_from = from_year // 100 + 1
        century_to = to_year // 100 + 1
        if century_from == century_to:
            if century_from <= 5:
                return f"ancient_{century_from}th_century_ce"
            elif century_to <= 15:
                return f"medieval_{century_from}th_century_ce"
            else:
                return f"modern_{century_from}th_century_ce"
        else:
            if century_from <= 5:
                return f"ancient_{century_from}th_{century_to}th_century_ce"
            elif century_to <= 15:
                return f"medieval_{century_from}th_{century_to}th_century_ce"
            else:
                return f"modern_{century_from}th_{century_to}th_century_ce"
    else:
        # 기원전-기원후跨越
        return f"transition_{abs(from_year)}_{to_year}"

def translate_to_korean(name):
    """
    국가명 한국어 번역 (임시 매핑)
    """
    translations = {
        "Roman Empire": "로마 제국",
        "Han Dynasty": "한나라",
        "Mongol Empire": "몽골 제국",
        "Ottoman Empire": "오스만 제국",
        "Qing Dynasty": "청나라",
        "Ming Dynasty": "명나라",
        "Song Dynasty": "송나라",
        "Tang Dynasty": "당나라",
        "Yuan Dynasty": "원나라",
        "Byzantine Empire": "비잔틴 제국",
        "Sassanid Empire": "사산 제국",
        "Achaemenid Empire": "아케메네스 제국",
        "Maurya Empire": "마우리아 제국",
        "Gupta Empire": "굽타 제국",
        "Delhi Sultanate": "델리 술탄국",
        "Mughal Empire": "무굴 제국",
        "British Empire": "대영 제국",
        "French Empire": "프랑스 제국",
        "Spanish Empire": "스페인 제국",
        "Portuguese Empire": "포르투갈 제국",
        "Dutch Empire": "네덜란드 제국",
        "Russian Empire": "러시아 제국",
        "Austrian Empire": "오스트리아 제국",
        "German Empire": "독일 제국",
        "Japanese Empire": "일본 제국",
        "Korean Empire": "대한제국",
        "Joseon": "조선",
        "Goryeo": "고려",
        "Silla": "신라",
        "Baekje": "백제",
        "Goguryeo": "고구려",
        "Three Kingdoms": "삼국시대",
        "Unified Silla": "통일신라",
        "Balhae": "발해"
    }
    return translations.get(name, name)

def process_cliopatria_data(input_file, output_file):
    """
    Cliopatria GeoJSON을 시대별로 분류하여 처리
    """
    print(f"Loading Cliopatria data from {input_file}...")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        cliopatria_data = json.load(f)
    
    print(f"Total features: {len(cliopatria_data['features'])}")
    
    # 시대별 데이터 구조 초기화
    period_boundaries = {}
    
    processed_count = 0
    for feature in cliopatria_data['features']:
        try:
            props = feature['properties']
            from_year = props['FromYear']
            to_year = props['ToYear']
            
            # 시대별 ID 생성
            period_id = get_period_id(from_year, to_year)
            
            if period_id not in period_boundaries:
                period_boundaries[period_id] = {
                    "period_id": period_id,
                    "start_year": from_year,
                    "end_year": to_year,
                    "regions": []
                }
            
            # 한국어 번역
            korean_name = translate_to_korean(props['Name'])
            
            region_data = {
                "name": korean_name,
                "original_name": props['Name'],
                "coordinates": feature['geometry']['coordinates'],
                "wikipedia_url": f"https://en.wikipedia.org/wiki/{props['Wikipedia']}" if 'Wikipedia' in props else None,
                "wikidata_id": props.get('Wikidata', None),
                "area_km2": props.get('Area', 0)
            }
            
            period_boundaries[period_id]['regions'].append(region_data)
            processed_count += 1
            
            if processed_count % 1000 == 0:
                print(f"Processed {processed_count} features...")
                
        except Exception as e:
            print(f"Error processing feature: {e}")
            continue
    
    print(f"Processed total: {processed_count} features")
    print(f"Total periods: {len(period_boundaries)}")
    
    # 결과 저장
    result = {
        "boundaries": list(period_boundaries.values())
    }
    
    print(f"Saving to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print("Processing complete!")

if __name__ == "__main__":
    input_file = "data/cliopatria_polities_only.geojson"
    output_file = "data/historical_boundaries.json"
    
    if os.path.exists(input_file):
        process_cliopatria_data(input_file, output_file)
    else:
        print(f"Input file {input_file} not found!")
