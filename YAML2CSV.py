import yaml
import csv

# 1. 读取 YAML 文件
with open("items.yaml", "r", encoding="utf-8") as file:
    data = yaml.safe_load(file)

# 2. 提取 "Equipment" 数据
equipment_data = data.get("Equipment", [])

# 3. 写入 CSV 文件
with open("items.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    
    # 写入表头
    headers = ["id", "name", "description", "amount", "individual_value", "objectType", "combo", "statChangeList"]
    writer.writerow(headers)
    
    # 写入数据
    for item in equipment_data:
        writer.writerow([
            item["id"], item["name"], item["description"], item["amount"], 
            item["individual_value"], item["objectType"], item["combo"], item["statChangeList"]
        ])

print("✅ YAML 已成功转换为 CSV！")
