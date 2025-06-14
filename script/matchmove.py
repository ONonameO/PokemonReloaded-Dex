import json

# 读取TM.json文件
with open('TM.json', 'r', encoding='utf-8') as tm_file:
    tm_data = json.load(tm_file)

# 读取move.json文件
with open('data/Move_List.json', 'r', encoding='utf-8') as move_file:
    move_data = json.load(move_file)

# 创建一个字典，以skill为键，cName和eName为值
move_dict = {move['id']: {'cName': move['cName'], 'eName': move['eName'], 'type':move['type'], 'explain': move['explain'], 'power': move['power'], 'pp': move['pp']} for move in move_data['skill']}

# 初始化结果列表
result = []

# 遍历TM.json中的每一项
for item in tm_data:
    condition = item['condition']
    skill = item['skill']
    
    # 检查当前的skill是否在move_dict中
    if skill in move_dict:
        move_info = move_dict[skill]
        result.append({
            "id": int(skill),
            "type": "招式学习器",
            "cName": f"{condition} {move_info['cName']}",
            "eName": f"{condition} {move_info['eName']}",
            "moveType": move_info['type'],
            "explain": move_info['explain'],
            "effect": f"威力：{move_info['power']}\nＰＰ：{move_info['pp']}"
        })

# 将结果输出为JSON格式
output_json = json.dumps(result, ensure_ascii=False, indent=4)
# print(output_json)

# 如果需要将结果保存到文件，可以取消以下注释
with open('output.json', 'w', encoding='utf-8') as output_file:
    output_file.write(output_json)