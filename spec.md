# 지도 구현 기술 명세서 (spec.md)

## 1. 개요
역사적 시대별로 국가 경계와 이름이 동적으로 변경되는 인터랙티브 지도를 구현합니다. Cliopatria 데이터셋을 활용하여 실제 역사적 경계를 표시하고, 시간 슬라이더를 통해 시대 전환 시 자동으로 국가 경계와 이름을 업데이트합니다.

## 2. 데이터 구조

### 2.1 시간대 데이터 (time_periods.json)
```json
{
  "periods": [
    {
      "id": "ancient_4000_3000_bce",
      "name": "기원전 40세기-30세기",
      "start_year": -4000,
      "end_year": -3000,
      "description": "4대 문명 발생기 (수메르, 이집트, 인더스, 황하)"
    },
    {
      "id": "ancient_3000_2000_bce",
      "name": "기원전 30세기-20세기",
      "start_year": -3000,
      "end_year": -2000,
      "description": "초기 문명 발전기"
    }
  ]
}
```

### 2.2 Cliopatria 데이터 처리
Cliopatria GeoJSON 데이터 구조:
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "Name": "Roman Empire",
        "FromYear": -27,
        "ToYear": 476,
        "Type": "POLITY",
        "Area": 2500000,
        "Wikipedia": "Roman_Empire",
        "Wikidata": "Q22755"
      },
      "geometry": {
        "type": "Polygon",
        "coordinates": [[[lon, lat], ...]]
      }
    }
  ]
}
```

### 2.3 처리된 역사적 경계 데이터 형식
시대별로 분류된 데이터:
```json
{
  "boundaries": [
    {
      "period_id": "ancient_1st_century_ce",
      "regions": [
        {
          "name": "로마 제국",
          "original_name": "Roman Empire",
          "coordinates": [[[lon, lat], ...]],
          "wikipedia_url": "https://en.wikipedia.org/wiki/Roman_Empire",
          "wikidata_id": "Q22755",
          "area_km2": 2500000
        }
      ]
    }
  ]
}
```

## 3. 지도 렌더링 기술

### 3.1 기본 지도 설정 (Leaflet.js)
```javascript
const map = L.map('map').setView([20, 0], 2);

L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
  subdomains: 'abcd',
  maxZoom: 19
}).addTo(map);
```

### 3.2 역사적 경계 폴리곤 렌더링

#### 3.2.1 GeoJSON 레이어 사용
```javascript
function renderHistoricalBoundaries(periodId) {
  // 기존 경계 제거
  boundaryLayers.forEach(layer => map.removeLayer(layer));
  boundaryLayers = [];

  const boundaryData = historicalBoundaries.find(b => b.period_id === periodId);
  
  if (boundaryData) {
    boundaryData.regions.forEach(region => {
      const geoJsonFeature = {
        "type": "Feature",
        "properties": {
          "name": region.name,
          "original_name": region.original_name,
          "wikipedia_url": region.wikipedia_url
        },
        "geometry": {
          "type": "Polygon",
          "coordinates": region.coordinates
        }
      };

      const geoJsonLayer = L.geoJSON(geoJsonFeature, {
        style: function(feature) {
          return {
            color: getBoundaryColor(periodId),
            weight: 2,
            opacity: 0.8,
            fillOpacity: 0.3,
            fillColor: getBoundaryFillColor(periodId)
          };
        },
        onEachFeature: function(feature, layer) {
          layer.bindTooltip(feature.properties.name, {
            permanent: false,
            direction: 'center',
            className: 'boundary-label'
          });
          
          layer.on('click', function(e) {
            showRegionInfo(feature.properties);
          });
        }
      }).addTo(map);

      boundaryLayers.push(geoJsonLayer);
    });
  }
}
```

#### 3.2.2 시대별 색상 시스템
```javascript
function getBoundaryColor(periodId) {
  const colorMap = {
    // 고대 (기원전)
    'ancient_4000_3000_bce': '#8B4513',      // 갈색
    'ancient_3000_2000_bce': '#A0522D',      // 시에나
    'ancient_2000_1000_bce': '#CD853F',      // 페루
    'ancient_1000_500_bce': '#D2691E',       // 초콜릿
    'ancient_500_0_bce': '#B8860B',          // 다크골드
    
    // 고대 (기원후)
    'ancient_1st_century_ce': '#DAA520',     // 골든로드
    'ancient_2nd_century_ce': '#BDB76B',     // 다크카키
    'ancient_3rd_century_ce': '#F4A460',      // 샌디브라운
    'ancient_4th_century_ce': '#DEB887',      // 버건디
    'ancient_5th_century_ce': '#D2B48C',      // 탄
    
    // 중세
    'medieval_6th_century_ce': '#708090',     // 슬레이트그레이
    'medieval_7th_century_ce': '#2F4F4F',     // 다크슬레이트그레이
    'medieval_8th_century_ce': '#008080',     // 틸
    'medieval_9th_century_ce': '#4682B4',     // 스틸블루
    'medieval_10th_century_ce': '#5F9EA0',    // 카데트블루
    'medieval_11th_century_ce': '#6495ED',    // 코니플로워블루
    'medieval_12th_century_ce': '#483D8B',    // 다크슬레이트블루
    'medieval_13th_century_ce': '#6A5ACD',    // 슬레이트블루
    'medieval_14th_century_ce': '#7B68EE',    // 미디엄슬레이트블루
    'medieval_15th_century_ce': '#9370DB',    // 미디엄퍼플
    
    // 근대
    'modern_16th_century_ce': '#228B22',      // 포레스트그린
    'modern_17th_century_ce': '#32CD32',      // 라임그린
    'modern_18th_century_ce': '#006400',     // 다크그린
    'modern_19th_century_ce': '#008000',      // 그린
    'modern_20th_century_ce': '#2E8B57',      // 시그린
    'modern_21st_century_ce': '#3CB371'       // 미디엄시그린
  };
  
  return colorMap[periodId] || '#666666';
}

function getBoundaryFillColor(periodId) {
  const color = getBoundaryColor(periodId);
  // 투명도 30% 적용
  return color + '4D'; // Hex alpha: 4D = 30%
}
```

### 3.3 시대 전환 애니메이션
```javascript
function transitionToPeriod(newPeriodId) {
  const currentPeriod = timePeriods[currentPeriodIndex];
  const newPeriod = timePeriods.find(p => p.id === newPeriodId);
  
  // 부드러운 전환 효과
  boundaryLayers.forEach(layer => {
    layer.setStyle({
      opacity: 0,
      fillOpacity: 0
    });
  });
  
  setTimeout(() => {
    renderHistoricalBoundaries(newPeriodId);
    
    // 페이드 인 효과
    boundaryLayers.forEach(layer => {
      layer.setStyle({
        opacity: 0.8,
        fillOpacity: 0.3
      });
    });
  }, 300);
}
```

### 3.4 국가명 표시 및 변경

#### 3.4.1 라벨 스타일링
```css
.boundary-label {
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid #333;
  border-radius: 4px;
  padding: 4px 8px;
  font-size: 12px;
  font-weight: bold;
  color: #333;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
  white-space: nowrap;
}

.boundary-label.permanent {
  background: rgba(255, 255, 255, 0.95);
  border: 2px solid #000;
}
```

#### 3.4.2 다국어 국가명 지원
```javascript
function getRegionName(region, language = 'ko') {
  const nameMap = {
    'ko': region.name_korean || region.name,
    'en': region.original_name,
    'ja': region.name_japanese || region.original_name,
    'zh': region.name_chinese || region.original_name
  };
  
  return nameMap[language] || region.original_name;
}
```

### 3.5 클릭 상세 정보 표시
```javascript
function showRegionInfo(properties) {
  const popupContent = `
    <div class="region-popup">
      <h3>${properties.name}</h3>
      <p><strong>원문명:</strong> ${properties.original_name}</p>
      <a href="${properties.wikipedia_url}" target="_blank">위키피디아에서 보기</a>
    </div>
  `;
  
  L.popup()
    .setLatLng(e.latlng)
    .setContent(popupContent)
    .openOn(map);
}
```

## 4. 데이터 처리 파이프라인

### 4.1 Cliopatria 데이터 처리 스크립트
```python
import json
import geojson
from datetime import datetime

def process_cliopatria_data(input_file, output_file):
    """
    Cliopatria GeoJSON을 시대별로 분류하여 처리
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        cliopatria_data = json.load(f)
    
    # 시대별 데이터 구조 초기화
    period_boundaries = {}
    
    for feature in cliopatria_data['features']:
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
        
        # 한국어 번역 (예시 - 실제로는 번역 API 필요)
        korean_name = translate_to_korean(props['Name'])
        
        region_data = {
            "name": korean_name,
            "original_name": props['Name'],
            "coordinates": feature['geometry']['coordinates'],
            "wikipedia_url": f"https://en.wikipedia.org/wiki/{props['Wikipedia']}",
            "wikidata_id": props['Wikidata'],
            "area_km2": props['Area']
        }
        
        period_boundaries[period_id]['regions'].append(region_data)
    
    # 결과 저장
    result = {
        "boundaries": list(period_boundaries.values())
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

def get_period_id(from_year, to_year):
    """
    연도 범위를 기반으로 시대 ID 생성
    """
    if from_year < 0 and to_year < 0:
        # 기원전
        century_from = abs(from_year) // 100 + 1
        century_to = abs(to_year) // 100 + 1
        return f"ancient_{century_from}th_{century_to}th_century_bce"
    elif from_year >= 0 and to_year >= 0:
        # 기원후
        century_from = from_year // 100 + 1
        century_to = to_year // 100 + 1
        return f"ancient_{century_from}th_{century_to}th_century_ce"
    else:
        # 기원전-기원후跨越
        return f"transition_{abs(from_year)}_{to_year}"

def translate_to_korean(name):
    """
    국가명 한국어 번역 (실제 구현시 번역 API 사용)
    """
    # 임시 매핑 - 실제로는 번역 API 필요
    translations = {
        "Roman Empire": "로마 제국",
        "Han Dynasty": "한나라",
        "Mongol Empire": "몽골 제국",
        "Ottoman Empire": "오스만 제국"
    }
    return translations.get(name, name)
```

### 4.2 데이터베이스 스키마 (SQLite)
```sql
-- 시간대 테이블
CREATE TABLE time_periods (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    start_year INTEGER NOT NULL,
    end_year INTEGER NOT NULL,
    description TEXT
);

-- 역사적 경계 테이블
CREATE TABLE historical_boundaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    period_id TEXT NOT NULL,
    region_name TEXT NOT NULL,
    original_name TEXT NOT NULL,
    coordinates TEXT NOT NULL,  -- GeoJSON coordinates as JSON string
    wikipedia_url TEXT,
    wikidata_id TEXT,
    area_km2 REAL,
    FOREIGN KEY (period_id) REFERENCES time_periods(id)
);

-- 인덱스 생성
CREATE INDEX idx_boundaries_period ON historical_boundaries(period_id);
CREATE INDEX idx_boundaries_name ON historical_boundaries(region_name);
```

## 5. 백엔드 API 구현

### 5.1 Flask 엔드포인트
```python
from flask import Flask, jsonify, request
import sqlite3
import json

app = Flask(__name__)
DB_PATH = 'data/language_evolution.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/time-periods')
def get_time_periods():
    conn = get_db_connection()
    periods = conn.execute('SELECT * FROM time_periods ORDER BY start_year').fetchall()
    conn.close()
    
    return jsonify({
        'periods': [dict(period) for period in periods]
    })

@app.route('/api/historical-boundaries/<period_id>')
def get_historical_boundaries(period_id):
    conn = get_db_connection()
    boundaries = conn.execute(
        'SELECT * FROM historical_boundaries WHERE period_id = ?',
        (period_id,)
    ).fetchall()
    conn.close()
    
    regions = []
    for boundary in boundaries:
        region = dict(boundary)
        region['coordinates'] = json.loads(region['coordinates'])
        regions.append(region)
    
    return jsonify({
        'period_id': period_id,
        'regions': regions
    })
```

## 6. 프론트엔드 통합

### 6.1 시간 슬라이더 구현
```javascript
const slider = document.getElementById('time-slider');
slider.addEventListener('input', (e) => {
    const periodIndex = parseInt(e.target.value);
    const period = timePeriods[periodIndex];
    
    // UI 업데이트
    document.getElementById('current-period').textContent = period.name;
    document.getElementById('period-description').textContent = period.description;
    
    // 지도 업데이트
    transitionToPeriod(period.id);
});
```

### 6.2 초기 로드
```javascript
async function initializeMap() {
    // 데이터 로드
    const periodsRes = await fetch('/api/time-periods');
    const periodsData = await periodsRes.json();
    timePeriods = periodsData.periods;
    
    // 슬라이더 범위 설정
    slider.max = timePeriods.length - 1;
    
    // 초기 시대 로드
    const firstPeriod = timePeriods[0];
    renderHistoricalBoundaries(firstPeriod.id);
}
```

## 7. 성능 최적화

### 7.1 GeoJSON 타일링
```javascript
// 대용량 데이터의 경우 타일링 적용
const tileLayer = L.geoJSON(null, {
  style: boundaryStyle,
  onEachFeature: onEachFeature
}).addTo(map);

// 현재 뷰포트 내의 피처만 로드
function loadVisibleFeatures() {
  const bounds = map.getBounds();
  const visibleFeatures = filterFeaturesByBounds(allFeatures, bounds);
  tileLayer.clearLayers();
  tileLayer.addData(visibleFeatures);
}
```

### 7.2 캐싱 전략
```javascript
// 로드된 데이터 캐싱
const boundaryCache = {};

async function getBoundaries(periodId) {
  if (boundaryCache[periodId]) {
    return boundaryCache[periodId];
  }
  
  const response = await fetch(`/api/historical-boundaries/${periodId}`);
  const data = await response.json();
  boundaryCache[periodId] = data;
  return data;
}
```

## 8. 테스트 계획

### 8.1 기능 테스트
- 시대 전환 시 경계가 올바르게 변경되는지 확인
- 국가명이 시대에 맞게 표시되는지 확인
- 색상이 시대별로 올바르게 적용되는지 확인
- 클릭 시 상세 정보가 올바르게 표시되는지 확인

### 8.2 성능 테스트
- 대용량 GeoJSON 로드 시간 측정
- 시대 전환 애니메이션 부드러움 확인
- 메모리 사용량 모니터링
