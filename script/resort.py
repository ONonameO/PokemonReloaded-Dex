import json

# 读取 JSON 文件
with open('data/Item_List.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

data = data["item"]

# 按照 id 排序
# data.sort(key=lambda x: x['id'])

# 重新设置 id
for i, item in enumerate(data, 1):
    item['id'] = i

# 输出处理后的 JSON 数据
# print(json.dumps(data, ensure_ascii=False, indent=2))

output_data = {
    "item": data
}

# 将处理后的数据保存回文件
with open('data/Item_List.json', 'w', encoding='utf-8') as f:
    json.dump(output_data, f, ensure_ascii=False, indent=4)