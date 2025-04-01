import csv
import yaml
import ast  # 解析字符串字典

# **1️⃣ 读取 CSV 文件并转换为 YAML 格式**
with open("items.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    equipment_list = []

    for row in reader:
        # 解析 statChangeList（转换字符串为字典）
        try:
            statChangeList = ast.literal_eval(row["statChangeList"])
            if not isinstance(statChangeList, dict):  
                statChangeList = {}  
        except (SyntaxError, ValueError):
            statChangeList = {}

        # 组装物品数据
        item = {
            "id": int(row["id"]),
            "name": row["name"],
            "description": row["description"],
            "amount": int(row["amount"]),
            "individual_value": int(row["individual_value"]),
            "objectType": row["objectType"],
            "statChangeList": statChangeList if statChangeList else None,
            "combo": row["combo"] if row["combo"] != "None" else "None"  # 处理 "None" 字符串
        }
        equipment_list.append(item)

# **2️⃣ 设定 YAML 统一的字段顺序**
field_order = ["id", "name", "description", "amount", "individual_value", "objectType", "statChangeList", "combo"]
sorted_equipment = [{key: item.get(key, None) for key in field_order} for item in equipment_list]

# **3️⃣ 生成最终的 YAML 数据**
yaml_data = {"Equipment": sorted_equipment}

# **4️⃣ 写入 YAML 文件**
with open("items.yaml", "w", encoding="utf-8") as file:
    yaml.dump(yaml_data, file, allow_unicode=True, default_flow_style=False, sort_keys=False)

print("✅ CSV 已成功转换并整理为 YAML！")
