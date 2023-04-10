import requests
import folium
import json
import pandas as pd

url = 'http://apis.data.go.kr/B553482/SeaTurtleRouteService/getSeaTurtleRoute'
params = {'serviceKey': '88xw0034yVxhwR4zKV9b4Nxi9cUCOMmYYcD1v5z5dFt1Jv/NmF/osS52GmPK9+ZhBOpDrmtoHqwvo5fBplKDdw==', 'numOfRows': '30', 'pageNo': '1', 'pttId': '152988',
          'resultType': 'json'}

response = requests.get(url, params=params)
json_str = response.content.decode("UTF-8")

json_object = json.loads(json_str)
data = pd.json_normalize(json_object['response']['body']['items']['item'])

# x좌표(위도),y좌표(경도) 리스트로 만들기
x = []
y = []
for i in range(len(data['obsrLat'])):
    x.append(data['obsrLat'][i])
    y.append(data['obsrLon'][i])
print('x갯수: ', len(x))
print('y갯수: ', len(y))

vworld_key = "25A7ADD2-49E3-361C-9FBA-846FFC23CB4F"

# 지도 중심 경위도 좌표(위도, 경도) 설정하기
lat, lon = 35.178739294057365, 129.12263821366713
# 줌 설정하기
zoom_size = 15

# folium 지도 생성하기
m = folium.Map(
    location=[lat, lon],
    zoom_start=zoom_size
)

# 배경지도 타일 설정하기
layer = "Satellite"
tileType = "jpeg"
tiles = f"http://api.vworld.kr/req/wmts/1.0.0/{vworld_key}/{layer}/{{z}}/{{y}}/{{x}}.{tileType}"
attr = "Vworld"

folium.TileLayer(
    tiles=tiles,
    attr=attr,
    overlay=True,
    control=True
).add_to(m)

# 지도 생성 및 marker 지정하기
for i in range(len(x)):
    folium.Marker([x[i], y[i]], icon=folium.Icon(
        color='red', icon='info-sign')).add_to(m)
m.save("index.html")
