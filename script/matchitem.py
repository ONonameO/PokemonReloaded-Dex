import json

# 加载两个JSON文件的内容
with open('temp/itemList.json', 'r', encoding='utf-8') as f1:
    item_data = json.load(f1)

with open('temp/Zcrystals.json', 'r', encoding='utf-8') as f2:
    pokeballs_data = json.load(f2)

# 创建一个字典，以item.json中的cName为键，explain和ceffect为值
item_dict = {item['cname']: {'explain': item['explain'], 'ceffect': item['ceffect']} for item in item_data['item']}

# 遍历PokeBalls.json中的每个精灵球，匹配并更新字段
unmatched_cnames = []  # 用于存储未匹配的cName
for pokeball in pokeballs_data:
    cName = pokeball['cName']
    if cName in item_dict:
        # 如果匹配成功，更新explain和ceffect字段
        pokeball['explain'] = item_dict[cName]['explain']
        pokeball['effect'] = item_dict[cName]['ceffect']
    else:
        # 如果未匹配，设置为空字符串
        pokeball['explain'] = ""
        pokeball['effect'] = ""
        unmatched_cnames.append(cName)  # 记录未匹配的cName

# 输出未匹配的cName
print("未匹配的cName列表：")
print(unmatched_cnames)

# 将更新后的PokeBalls.json内容写回到文件
with open('output/Zcrystals.json', 'w', encoding='utf-8') as f3:
    json.dump(pokeballs_data, f3, ensure_ascii=False, indent=4)

print("处理完成，已将更新后的数据写入到PokeBalls_updated.json文件中。")