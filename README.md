# seoulMap

서울시 택시데이터와 한국 지도(svg파일)을 이용한 히트맵 표현

구역별 택시차량 수에 따른 heatmap

데이터
----------------------
서울 택시 데이터 : http://data.seoul.go.kr/dataList/datasetView.do?infId=OA-12066&srvType=F&serviceKind=1

**P.S. 택시 데이터는 scala를 통해 자료를 가공했습니다.

실행 방법
---------------------
1. southKorea.py 코드를 실행 
2. 가공된 데이터의 택시차량의 수에 따라 구역마다 다른 색상 부여
3. Output : data 폴더의 'test.svg' 파일로 output 출력

이미지 예시
---------------------

![mapImage](./data/image/image.JPG)


