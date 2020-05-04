import urllib.request
import json
import datetime
from database_models import Hotel, sqlite_db
import credentials
import re


seoul_gu_names = ["남구", "강동구","강북구", "강서구", "관악구","광진구",
                    "구로구", "금천구", "노원구","도봉구","동대문구", "동작구",
                    "마포구", "서대문구", "서초구", "성동구", "성북구", "송파구",
                    "양천구", "영등포구", "용산구", "은평구", "종로구", "중구", "중랑구"]

BASE_URL = "https://openapi.naver.com/v1/"


def search_places(query, display=30, start=1, sort="random"):

    encText = urllib.parse.quote(query)
    url = BASE_URL + "search/local.json" + \
          "?query=" + encText + \
          "&display=" + str(display) + \
          "&start=" + str(start) + \
          "&sort=" + sort
    # print(url)
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", credentials.CLIENT_ID)
    request.add_header("X-Naver-Client-Secret", credentials.CLIENT_SECRET)
    response = urllib.request.urlopen(request)

    response_code = response.getcode()

    if response_code == 200:
        response_body = response.read()
        decoded_body = response_body.decode('utf-8')

        # 결과를 JSON 키값으로 접근하기 위해 json.loads 를 한다.
        result = json.loads(decoded_body)
        print(result)
        save_to_database_server(result)

        # 결과가 30개 이상이면 start 를 30 더해서 다시 검색한다.
        if len(result["items"]) >= display:
            search_places(query, start=start+30)

    else:
        print("Error Code:" + response_code)


def save_to_database_server(results):
    sqlite_db.connect(reuse_if_open=True)
    timestamp = datetime.datetime.now()

    for item in results["items"]:
        formatted_name = format_hotel_name(item["title"])
        query = Hotel.insert(name=formatted_name, address=item["roadAddress"], website_link=item["link"],
                      latitude=float(item["mapx"]), longitude=float(item["mapy"]),
                      phone_number=item["telephone"], created_at=timestamp)
        try:
            query.on_conflict(action='REPLACE')
            query.execute()
        except Exception as e:
            print(e)
            sqlite_db.rollback()


hotel_name_list = []


def format_hotel_name(name):
    if '<b>' or '&amp' in name:
        name = re.sub('<b>|</b>', '', name)
        name = re.sub('&amp;', '&', name)
    return name


# def get_all_hotel_names_from_database():
#     query = Hotel.select(Hotel.name)
#     for hotel in query:
#         name = hotel.name
#         if '<b>' or '&amp' in name:
#             name = re.sub('<b>|</b>', '', name)
#             name = re.sub('&amp;', '&', name)
#         hotel_name_list.append(name)


if __name__ == '__main__':
    # get_all_hotel_names_from_database()
    # for name in hotel_name_list:
    #     print(name)

    for name in seoul_gu_names:
        # time.sleep(0.5)
        print("==== RESULT OF " + name + " ====")
        search_places(query=name + " 애견호텔")

