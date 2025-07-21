from translate import Translator
from langdetect import detect, LangDetectException
import requests
import json

IS_TRANSLATE_NAME = False
IS_TRANSLATE_SECTION = True

source_list = ["https://trollfools.slpmods.net/"]
endFix = "trollpackages.json"


translator = Translator(to_lang="zh")

def translatoor(text2trans):
    try:
        if not text2trans or text2trans.strip() == "":
            return text2trans
        language = detect(text2trans)
        # 如果已经是中文，直接返回
        if language == "zh":
            return text2trans
        
        return translator.translate(text2trans)
    except (LangDetectException, Exception) as e:
        print(f"翻译错误: {str(e)}，原文本: {text2trans}")
        return text2trans  

def get_json_from_url(url):
    try:
        response = requests.get(url, timeout=25)  
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"请求失败: {url}: {e}")
        return None

for url in source_list:
    json_data = get_json_from_url(url + endFix)
    if json_data:
        for package in json_data:
            
            if "name" in package and IS_TRANSLATE_NAME:
                package["name"] = translatoor(package["name"])
            if "description" in package:
                package["description"] = translatoor(package["description"])
            if "section" in package and IS_TRANSLATE_SECTION:
                package["section"] = translatoor(package["section"])
            print(f"翻译处理: {package.get('name', '未知包名')}")
        
        
        with open(f"tmp/{url}zh-cn_{endFix}", "w+", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)
        print(f"翻译完成: {url}")
    else:
        print(f"无数据处理: {url}")