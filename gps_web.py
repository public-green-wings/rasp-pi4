from bs4 import BeautifulSoup
from pprint import pprint
import requests
import json

url = 'https://dsc-sookmyung.tistory.com/85'
# url = 'https://search.naver.com/search.naver?query=날씨'
html = requests.get(url)
print(html.raise_for_status()) # 정상 200
# <div class="MuiFormControl-root MuiTextField-root"><label class="MuiFormLabel-root MuiInputLabel-root MuiInputLabel-formControl MuiInputLabel-animated MuiInputLabel-shrink MuiInputLabel-outlined" data-shrink="true" for="lat" id="lat-label" readonly="">위도</label><div class="MuiInputBase-root MuiOutlinedInput-root MuiInputBase-formControl"><input aria-invalid="false" id="lat" type="text" class="MuiInputBase-input MuiOutlinedInput-input" value="37.2475"><fieldset aria-hidden="true" class="jss5 MuiOutlinedInput-notchedOutline"><legend class="jss7 jss8"><span>위도</span></legend></fieldset></div></div>
soup = BeautifulSoup(html.text, 'html.parser')

data1 = soup.find('div', {'class': 'article-view'})
data2 = soup.find('input',{'name':'id'})

#lat#lat
# <div class="print-only hUbt4d-print" id="print"></div>
# <div class="o-Yc-o-T" tabindex="0" role="link" aria-label="내 드라이브" data-target="folder" data-tooltip="내 드라이브" data-tooltip-align="b,c" data-tooltip-delay="500" data-tooltip-unhoverable="true" data-id="0ACTWIOd1ohQQUk9PVA">내 드라이브</div>
# <div class="sbib_b" id="sb_ifc50" role="combobox" aria-haspopup="grid" aria-owns="sbsg50" dir="ltr" aria-expanded="true"><div id="gs_lc50" style="position: relative;"><input autofocus="autofocus" value="" aria-label="37.248322, 127.075706 주변 검색" autocomplete="off" id="searchboxinput" name="q" jstcache="11" jsaction="keyup:omnibox.keyUp;input:omnibox.inputDetected" class="tactile-searchbox-input" jsan="7.searchboxinput,7.xiQnY,0.autofocus,0.value,0.placeholder,0.aria-label,0.autocomplete,0.id,0.name,22.jsaction" style="font-family: Roboto, Arial, sans-serif; border: none; padding: 0px; margin: 0px; height: auto; width: 100%; background: url(&quot;data:image/gif;base64,R0lGODlhAQABAID/AMDAwAAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw%3D%3D&quot;) transparent; position: absolute; z-index: 6; left: 0px; outline: none;" aria-autocomplete="list" aria-controls="sbsg50" dir="ltr" spellcheck="false"><input class="tactile-searchbox-input" disabled="" autocomplete="off" autocapitalize="off" aria-hidden="true" id="gs_taif50" dir="ltr" style="border: none; padding: 0px; margin: 0px; height: auto; width: 100%; position: absolute; z-index: 1; background-color: transparent; -webkit-text-fill-color: silver; color: silver; left: 0px; visibility: hidden; font-family: Roboto, Arial, sans-serif;"><input class="tactile-searchbox-input" disabled="" autocomplete="off" autocapitalize="off" aria-hidden="true" id="gs_htif50" dir="ltr" style="border: none; padding: 0px; margin: 0px; height: auto; width: 100%; position: absolute; z-index: 1; background-color: transparent; -webkit-text-fill-color: silver; color: silver; transition: all 0.218s ease 0s; opacity: 1; text-align: left; left: 0px; font-family: Roboto, Arial, sans-serif;"></div></div>
#sb_ifc50

#my-current-location > div:nth-child(4) > div:nth-child(1) > div:nth-child(1) > div
#my-current-location > div:nth-child(4) > div:nth-child(1) > div:nth-child(1) > div > div

# pprint(html.text)

print(data1)
print(data2)

result1 = data1.find('input',{'name':'id'})

print(result1)

# response = requests.get(url)

# if not response.ok:
#   raise Exception("There was an error calling the API")

# response = response.json()
# print(type(response))
# results = response.get("result")
# print(type(results))


# if not results:
#   print("Could not find any results for your search term :(")

# print([result.get("headline") for result in results])

# source = requests.get(url).text 
# json_reponse = json.loads(source)
# print(json_reponse)
# res = requests.get(html) 
 # 정상 200
# print(html.raise_for_status())
#웹페이지 요청을 하는 코드이다. 특정 url을 적으면 웹피이지에 대한 소스코드들을 볼 수 있다.

#pprint(html.text)
#pprint는 딕셔너리의 데이터가 긴 경우에 좀 더 보기 편하게 보여주게 도와준다.

# soup = BeautifulSoup(html.text, 'html.parser')
# #파이썬에서 보기 좋게, 다루기 쉽게 파싱작업을 거쳐야 각 요소에 접근이 쉬워진다.
# #이것을 도와주는게 beautifulsoup4 모듈이다.

# #soup 모듈의 find 함수를 사용해서 data1에 값을 저장한다.
# #find 함수를 사용할 때 주의할 점은 같은 웹피이지 소스코드에 같은 소스가 여러가지 있으면 맨 처음 탐색된것만 반환하고 나머지는 무시된다는 점이다.


# data1 = soup.find('div', {'class': 'MuiInputBase-root MuiOutlinedInput-root MuiInputBase-formControl'})
# data2 = soup.find('input',{'name':'id'})

# result1 = data1.find('input',{'name':'id'})

# print(result1)