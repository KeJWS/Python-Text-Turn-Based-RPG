import inventory
import skills
import yaml

with open("items.yaml", "r", encoding="utf-8") as file:
    items = yaml.safe_load(file)

def get_equipment_by_id(equipment_list, item_id):
    for item in equipment_list:
        if item["id"] == item_id:
            # 动态查找该技能对象
            combo_object = getattr(skills, item["combo"], None)
            
            return (
                item["name"], 
                item["description"], 
                item["amount"], 
                item["individual_value"], 
                item["objectType"], 
                item["statChangeList"], 
                combo_object
            )
    return None

# 读取所有装备，使用 name 作为 key
equipment_objects = {
    item["name"]: inventory.Equipment(*get_equipment_by_id(items["Equipment"], item["id"]))
    for item in items["Equipment"]
}

# 初始物品
# -> 初始武器
rustySword = equipment_objects["🗡️ 生锈的剑"]
brokenDagger = equipment_objects["🔪 破损的匕首"]
oldStaff = equipment_objects["🏏 旧法杖"]
# -> 初始盔甲
noviceArmor = equipment_objects["🛡️ 新手盔甲"]
oldRobes = equipment_objects["🛡️ 旧长袍"]

# 基础物品
# -> 基础武器
# longsword = inventory.Equipment('长剑', '', 1, 19, 'Weapon', {'atk': 6, 'def': 2}, skills.comboSlash1)
longsword = equipment_objects["🗡️ 长剑"]
dagger = equipment_objects["🔪 匕首"]
staff = equipment_objects["🏏 法杖"]
# -> 基础盔甲
clothArmor = equipment_objects["🛡️ 布甲"]
bronzeArmor = equipment_objects["🛡️ 青铜盔甲"]
studentRobes = equipment_objects["🛡️ 学者长袍"]

# 高级物品
# -> 高级武器
warhammer = equipment_objects["🏏 战锤"]
zweihander = equipment_objects["⚔️ 双手剑"]
sageStaff = equipment_objects["🏏 智者法杖"]
sai = equipment_objects["🗡️ 三叉戟"]

# -> 高级盔甲
ironArmor = equipment_objects["🛡️ 铁甲"]
sageTunic = equipment_objects["🛡️ 智者上衣"]
thiefArmor = equipment_objects["🛡️ 盗贼盔甲"]

# 消耗品
hpPotion = inventory.Potion('治疗药水', 'a', 1, 10, 'Consumable', 'hp', 15)
mpPotion = inventory.Potion('法力药水', 'a', 1, 10, 'Consumable', 'mp', 15)

# 法典
grimoireFireball = inventory.Grimoire('法典：火球术', '', 1, 20, 'Consumable', skills.spellFireball)
grimoireDivineBlessing = inventory.Grimoire('法典：神圣祝福', '', 1, 20, 'Consumable', skills.spellDivineBlessing)
grimoireEnhanceWeapon = inventory.Grimoire('法典：增强武器', '', 1, 25, 'Consumable', skills.spellEnhanceWeapon)
grimoireInferno = inventory.Grimoire('法典：地狱火', '', 1, 50, 'Consumable', skills.spellInferno)
grimoireSummonSkeleton = inventory.Grimoire('法典：召唤骷髅', '', 1, 30, 'Consumable', skills.spellSkeletonSummoning)
grimoireSummonFireSpirit = inventory.Grimoire('法典：火焰精灵', '', 1, 60, 'Consumable', skills.spellFireSpiritSummonning)

# 商店商品套装

rik_armor_shop_item_set = [ longsword, 
                            dagger, 
                            warhammer, 
                            ironArmor,
                            zweihander,
                            clothArmor,
                            bronzeArmor,
                            sai, 
                            thiefArmor ]

itz_magic_item_set = [ staff,
                        clothArmor,
                        hpPotion,
                        mpPotion,
                        sageTunic,
                        sageStaff,
                        studentRobes,
                        grimoireFireball,
                        grimoireEnhanceWeapon,
                        grimoireDivineBlessing,
                        grimoireInferno,
                        grimoireSummonSkeleton,
                        grimoireSummonFireSpirit ]