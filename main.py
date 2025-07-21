from urllib.parse import urlparse
from translate import Translator
from langdetect import detect, LangDetectException
import requests
import os 
import json

source_list = []

from config import source_list
from baiduTranslate import *

#TODO: 支持同时翻译为多种语言并保存至多个文件夹

IS_USE_API = True  # 是否使用API进行翻译
IS_TRANSLATE_NAME = False
IS_TRANSLATE_SECTION = False # 不能开启，开启无法适配


endFix = "trollpackages.json"



def translatoor(text2trans):
    try:
        # 加载 mapping.json 文件
        mapping = {}
        try:
            with open("mapping.json", "r", encoding="utf-8") as f:
                mapping = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # 文件不存在或内容损坏，创建空字典
            pass  # mapping 已初始化为空字典

        # 如果原文在 mapping 中，直接返回译文
        if text2trans in mapping:
            return mapping[text2trans]

        # 空文本直接返回
        if not text2trans or text2trans.strip() == "":
            return text2trans

        
        if not IS_USE_API:
            # 检测语言
            language = detect(text2trans)
            if language == "zh":
                return text2trans
            translator = Translator(from_lang=language,to_lang="zh")

            # 翻译
            translated_text = translator.translate(text2trans)

            # 更新 mapping 并保存
            mapping[text2trans] = translated_text
            with open("mapping.json", "w", encoding="utf-8") as f:
                json.dump(mapping, f, ensure_ascii=False, indent=4)

            return translated_text
        elif IS_USE_API:
            langDetect(text2trans)
            translated_text = translate(text2trans)
            if translated_text:
                # 更新 mapping 并保存
                mapping[text2trans] = translated_text
                with open("mapping.json", "w", encoding="utf-8") as f:
                    json.dump(mapping, f, ensure_ascii=False, indent=4)
                return translated_text
            else:
                print(f"翻译失败，使用API时未返回结果: {text2trans}")
                return text2trans

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
        host = urlparse(url).netloc  # 提取主机名
        output_path = f"translated/zh-cn/{host}/{endFix}"  # 构建新路径
        os.makedirs(os.path.dirname(output_path), exist_ok=True)  # 确保目录存在
        for package in json_data:
            
            if "name" in package and IS_TRANSLATE_NAME:
                package["name"] = translatoor(package["name"])
            if "description" in package:
                package["description"] = translatoor(package["description"])
            if "section" in package and IS_TRANSLATE_SECTION:
                package["section"] = translatoor(package["section"])
            print(f"翻译处理: {package.get('name', '未知包名')}")

        with open(output_path, "w+", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)
        print(f"翻译完成: {url}")
    else:
        print(f"无数据处理: {url}")