import os
import json
from config import repository_url

def generate_package_json():
    # 配置参数
    base_dir = "translated/zh-cn/iPhoneDowngrade/Plugins"
    output_file = "translated/zh-cn/iPhoneDowngrade/trollpackages.json"
    
    # 仓库信息（可根据需要修改）
    repository_name = "艾锋降级插件"
    repository_icon = "https://c-ssl.dtstatic.com/uploads/item/201808/22/20180822102220_rfdqr.thumb.1000_0.png"
    default_author = "艾锋降级公众号"
    default_section = "Tools"
    
    # 基础URL（可根据需要修改）
    base_url = repository_url
    
    packages = []
    
    # 遍历目录下的所有文件
    for filename in os.listdir(base_dir):
        file_path = os.path.join(base_dir, filename)
        
        # 跳过目录，只处理文件
        if os.path.isfile(file_path):
            # 获取文件大小（字节）
            size_bytes = os.path.getsize(file_path)

            # 转换单位
            if size_bytes >= 1024 * 1024:
                size_str = f"{round(size_bytes / (1024 * 1024), 2):.2f} MB"
            else:
                size_str = f"{round(size_bytes / 1024, 2):.2f} KB"

            # 去除文件扩展名作为包名
            package_name = os.path.splitext(filename)[0]
            
            package = {
                "name": package_name,
                "version": "v1.0.0",
                "description": f'插件名：{package_name}\r\n所有内容均来自“艾锋降级"公众号',
                "app_url": "",  # 可选字段
                "icon_url": "",#f"https://c-ssl.duitang.com/uploads/blog/202103/09/20210309094204_5f164.thumb.1000_0.jpg",
                "dylib": f"{base_url}/Plugins/{filename}",
                "section": default_section,
                "size": size_str,
                "author": default_author,
                "screenshots": []
            }
            
            packages.append(package)
    
    # 创建最终JSON结构
    result = {
        "repository_name": repository_name,
        "repository_icon": repository_icon,
        "packages": packages
    }
    
    # 写入JSON文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"成功生成 {len(packages)} 个包信息到 {output_file}")

if __name__ == "__main__":
    generate_package_json()