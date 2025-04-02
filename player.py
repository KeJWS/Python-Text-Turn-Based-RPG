import inventory
import text
import combat

from test.constants import MONEY_MULTIPLIER, EXPERIENCE_RATE

class Player(combat.Battler):
    '''
    玩家主类，负责处理所有与玩家属性和游戏进程相关的信息。

    Attributes:
    lvl: int
        玩家当前等级，默认为 1。
    xp: int
        玩家当前经验值 (XP)。
    xpToNextLvl: int
        升级所需的经验值。
    comboPoints: int
        当前连击点数 (CP)。
    aptitudes: Dictionary
        负责管理能力系统的字典。每种能力可提供以下属性加成：
            STR -> ATK + 1 （力量影响攻击）
            DEX -> SPD + 1, CRIT + 1 （敏捷影响速度和暴击率）
            INT -> MATK + 1 （智力影响魔法攻击）
            WIS -> MP + 5 （智慧影响魔法值）
            CONST -> MAXHP + 5 （体质影响最大生命值）
    aptitudePoints: int
        可用于提升能力的点数。
    inventory: Inventory
        玩家物品栏。
    equipment: Dictionary
        存储当前玩家装备的字典。
    money: int
        当前金钱（金币）。
    combos: List
        玩家可使用的连击列表。
    spells: List
        玩家可使用的法术列表。
    activeQuests: List
        当前进行中的任务列表。
    completedQuests: List
        已完成的任务列表。
    '''

    XP_MULTIPLIER = 1.5 # 经验倍率
    XP_BASE = 10 # 基础经验
    STAT_INCREASE = 1 # 升级后可得能力点

    def __init__(self, name) -> None:
        stats = {
            'maxHp': 25,    'hp': 25,
            'maxMp': 10,    'mp': 10,
            'atk': 10,      'def': 10,
            'matk': 10,     'mdef': 10,
            'speed': 10,    'critCh': 10
        }

        super().__init__(name, stats)

        self.lvl = 1 # 玩家等级
        self.xp = 0 # 当前经验值

        # TODO: 需要更好的经验曲线
        self.xpToNextLvl = 35 # 升级所需经验值，每级乘以 1.5
        self.comboPoints = 0
        self.aptitudes = {
                    'str': 5,   'dex': 5,
                    'int': 5,   'wis': 5,
                    'const': 5
        }

        self.aptitudePoints = 0 # 可分配的能力点
        self.inventory = inventory.Inventory() # 玩家物品栏
        self.equipment = {'Weapon': None,
                            'Armor': None} # 玩家装备，可扩展
        self.money = 20 # 当前金钱
        self.combos = [] # 玩家可用连击（攻击 + CP）
        self.spells = [] # 玩家可用法术（魔攻 + MP）

        self.activeQuests = []
        self.completedQuests = []
        
        self.isAlly = True # 判断是否为友军
    
    def normal_attack(self, defender):
        self.addComboPoints(1)
        return super().normal_attack(defender)

    def equip_item(self, equipment):
        '''
        玩家装备指定物品，物品必须是“装备”类型。

        Parameters:
        equipment: Equipment
            需要装备的物品。
        '''
        if type(equipment) == inventory.Equipment:
            actualEquipment = self.equipment[equipment.objectType]
            if actualEquipment != None:
                print(f'{actualEquipment.name} 已卸下。')
                actualEquipment.add_to_inventory(self.inventory, 1)
                # 移除之前装备提供的连击
                if actualEquipment.combo != None:
                    self.combos.remove(actualEquipment.combo)
                    print(f'你无法再使用连击：{actualEquipment.combo.name}')
                # 移除旧装备提供的属性加成
                for stat in actualEquipment.statChangeList:
                    self.stats[stat] -= actualEquipment.statChangeList[stat]
            # 增加新装备提供的属性加成
            for stat in equipment.statChangeList:
                self.stats[stat] += equipment.statChangeList[stat]
            self.equipment[equipment.objectType] = equipment.create_item(1)
            # 添加新装备的连击
            if equipment.combo != None and equipment.combo not in self.combos:
                self.combos.append(equipment.combo)
                print(f'你现在可以使用连击：{equipment.combo.name}')
            self.inventory.decrease_item_amount(equipment, 1)
            print(f'{equipment.name} 已装备。')
            print(equipment.show_stats())
        else:
            if equipment != None:
                print('{} 无法装备。'.format(equipment.name))
        text.inventory_menu()
        self.inventory.show_inventory()

    def use_item(self, item):
        '''
        使用指定的物品。物品必须属于 "usable_items" 列表中的类型才能被使用。

        Parameters:
        item: Item
            要使用的物品。
        '''
        usable_items = [inventory.Potion, inventory.Grimoire]
        if type(item) in usable_items:
            item.activate(self)
        text.inventory_menu()
        self.inventory.show_inventory()

    def add_exp(self, exp):
        '''
        增加玩家的经验值，并处理升级逻辑。
        升级时，玩家的生命值和魔法值将完全恢复，并且所有属性 +1。

        Parameters:
        exp: int
            要增加的经验值。
        '''
        self.xp += exp * EXPERIENCE_RATE
        print(f"你获得了 \033[32m{exp*EXPERIENCE_RATE}\033[0m 经验值")
        # 处理升级
        while self.xp >= self.xpToNextLvl:
            self.xp -= self.xpToNextLvl
            self.lvl += 1
            # 经验需求计算公式，可调整
            self.xpToNextLvl = round(self.xpToNextLvl * self.XP_MULTIPLIER + self.XP_BASE * self.lvl * self.lvl)
            for stat in self.stats:
                self.stats[stat] += self.STAT_INCREASE
            self.aptitudePoints += 1
            combat.fully_heal(self)
            combat.fully_recover_mp(self)
            print(f"升级了！你现在是 {self.lvl} 级，剩余 {self.aptitudePoints} 个能力点。")

    def add_money(self, money):
        '''
        增加玩家的金钱。

        Parameters:
        money: int
            要增加的金币数量。
        '''
        self.money += money * MONEY_MULTIPLIER
        print(f"你获得了 \033[33m{money*MONEY_MULTIPLIER}\033[0m 枚金币! (💰: \033[33m{self.money}\033[0m)")

    def assign_aptitude_points(self):
        '''
        能力点分配菜单。
        '''
        options = {
                    '1': 'str', '2': 'dex',
                    '3': 'int', '4': 'wis',
                    '5': 'const'}
        text.showAptitudes(self)
        while (option := input("> ").lower()) != 'q':
            if self.aptitudePoints >= 1 and option in options:
                aptitude = options[option]
                self.aptitudes[aptitude] += 1
                print(f'{aptitude} 现在是 {self.aptitudes[aptitude]}!')
                self.update_stats_to_aptitudes(aptitude)
                self.aptitudePoints -= 1
            else:
                print('无效选项或能力点不足！')

    def update_stats_to_aptitudes(self, aptitude):
        '''
        根据所提升的能力点分配对应的属性加成。

        Parameters:
        aptitude: str
            要升级的能力。
        '''
        if aptitude == 'str':
            self.stats['atk'] += 1
        elif aptitude == 'dex':
            self.stats['speed'] += 1
            self.stats['critCh'] += 1
        elif aptitude == 'int':
            self.stats['matk'] += 1
        elif aptitude == 'wis':
            self.stats['maxMp'] += 3
        elif aptitude == 'const':
            self.stats['maxHp'] += 3

    def buy_from_vendor(self, vendor):
        '''
        从商店购买物品。

        Parameters:
        vendor: Shop
            玩家要购买物品的商店。
        '''
        text.shop_buy(self)
        vendor.inventory.show_inventory()
        while (i := int(input("> "))) != 0:
            if 0 < i <= len(vendor.inventory.items):
                vendor.inventory.items[i-1].buy(self)
                if vendor.inventory.items[i-1].amount <= 0:
                    vendor.inventory.items.pop(i - 1)
                vendor.inventory.show_inventory()
            else:
                print("无效选项")

    def show_quests(self):
        '''
        显示当前任务，包括进行中的任务和已完成的任务。
        '''
        print('/// 进行中 ///')
        for actq in self.activeQuests:
            actq.show_info()
        print('/// 已完成 ///')
        for cmpq in self.completedQuests:
            cmpq.show_info()

    def addComboPoints(self, points):
        '''
        增加一定数量的连击点数 (CP)。

        Parameters:
        points: int
            要增加的连击点数。
        '''
        self.comboPoints += points