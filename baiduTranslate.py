import json
import requests


def langDetect(text):
    url = "https://fanyi.baidu.com/langdetect"

    payload = {
    'query': text[:150]
    }

    headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.7103.48 Safari/537.36",
    'Accept-Encoding': "gzip, deflate, br, zstd",
    'sec-ch-ua-platform': "\"Windows\"",
    'sec-ch-ua': "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"136\", \"Google Chrome\";v=\"136\"",
    'sec-ch-ua-mobile': "?0",
    'Origin': "https://fanyi.baidu.com",
    'Sec-Fetch-Site': "same-origin",
    'Sec-Fetch-Mode': "cors",
    'Sec-Fetch-Dest': "empty",
    'Referer': "https://fanyi.baidu.com/mtpe-individual/multimodal?ext_channel=DuSearch",
    'Accept-Language': "zh-CN,zh;q=0.9"
    }

    response = requests.post(url, data=payload, headers=headers)

    resp = response.json()
    if resp.get("error") == 0:
        lang = resp.get("lan")
        return lang
    else:
        print(f"语言检测错误: {resp.get('error')}")
        return None

def translate(text):
    lang = langDetect(text)
    if lang == "zh":
        return text
    else:
        url = "https://fanyi.baidu.com/transapi"

        payload = {
        'from': lang,
        'query': text,
        'source': "txt",
        'to': "zh"
        }

        headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.7103.48 Safari/537.36",
        'Accept-Encoding': "gzip, deflate, br, zstd",
        'sec-ch-ua-platform': "\"Windows\"",
        'sec-ch-ua': "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"136\", \"Google Chrome\";v=\"136\"",
        'sec-ch-ua-mobile': "?0",
        'Origin': "https://fanyi.baidu.com",
        'Sec-Fetch-Site': "same-origin",
        'Sec-Fetch-Mode': "cors",
        'Sec-Fetch-Dest': "empty",
        'Referer': "https://fanyi.baidu.com/mtpe-individual/multimodal?query=I%20think%20that%2C%20from%20a%20biological%20standpoint%2C%20human%20life%20almost%20reads%20like%20a%20poem.%20It%20has%20its%20own%20rhythm%20and%20beat%2C%20its%20internal%20cycles%20of%20growth%20and%20decay.%20It%20begins%20with%20innocent%20childhood%2C%20followed%20by%20awkward%20adolescence%20trying%20awkwardly%20to%20adapt%20itself%20to%20mature%20society%2C%20with%20its%20young%20passions%20and%20follies%2C%20its%20ideals%20and%20ambitions%3B%20then%20it%20reaches%20a%20manhood%20of%20intense%20activities%2C%20profiting%20from%20experience%20and%20learning%20more%20about%20society%20and%20human%20nature%3B%20at%20middle%20age%2C%20there%20is%20a%20slight%20easing%20of%20tension%2C%20a%20mellowing%20of%20character%20like%20the%20ripening%20of%20fruit%20or%20the%20mellowing%20of%20good%20wine%2C%20and%20the%20gradual%20acquiring%20of%20a%20more%20tolerant%2C%20more%20cynical%20and%20at%20the%20same%20time%20a%20kindlier%20view%20of%20life%3B&lang=en2zh&ext_channel=DuSearch",
        'Accept-Language': "zh-CN,zh;q=0.9"
        }

        response = requests.post(url, data=payload, headers=headers)

        resp = response.json()
        if resp['status'] == 0:
            try:
                data = resp['data']
                translation = ''
                for i in data:
                    result_dict = i
                    result_dict = result_dict['dst']
                    translation += result_dict
                return translation
            except json.JSONDecodeError:
                print(f"翻译结果解析错误: {resp['result']}")
                return None

            except:
                result_dict = json.loads(resp['result'])
    
                # 逐步访问嵌套结构
                content = result_dict['content'][0]  # 'content' 是一个列表
                mean = content['mean'][0]           # 'mean' 是一个列表
                cont_dict = mean['cont']            # 'cont' 是一个字典
                
                # 获取字典的第一个键
                first_key = next(iter(cont_dict.keys()))
                
                return first_key

        else:
            print(f"翻译错误: {resp.get('status')}")
            return None