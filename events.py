import combat
import random
import text
import shops
import items
import enemies
import quest

class Event():
    '''
    处理各种事件（敌人遭遇战、商店、治疗地点等）

    Attributes: 
    name: str
        事件名称
    successChance: int
        事件成功的概率
    isUnique: bool
        是否为唯一事件，若为 True，则该事件只能触发一次；若为 False，则可重复触发。
    '''
    def __init__(self, name, successChance, isUnique) -> None:
        self.name = name
        self.successChance = successChance
        self.isUnique = isUnique

    def check_success(self):
        '''
        检查事件是否成功触发

        Returns:
        True/False: bool
            若事件成功触发，则返回 True，否则返回 False。
        '''
        if self.successChance < random.randint(0, 100):
            return False
        return True

    def add_event_to_event_list(self):
        '''
        将事件加入相应的事件类型列表
        '''
        if type(self) == FixedCombatEvent:
            event_type_list[0].append(self)
        elif type(self) == ShopEvent:
            event_type_list[1].append(self)
        elif type(self) == HealingEvent:
            event_type_list[2].append(self)

class RandomCombatEvent(Event):
    '''
    继承 Event 类。用于随机遭遇战。

    Attributes:
    enemy_quantity_for_level: dict
        记录不同等级对应的敌人数量，
        格式如下：{等级上限: 敌人数量}
        例如 {3: 1} 表示等级在 3 级及以下时，仅出现 1 个敌人。
    '''
    def __init__(self, name) -> None:
        super().__init__(name, 100, False)
        self.enemy_quantity_for_level = {3: 1,
                                        5: 2, 
                                        10: 3, 
                                        100: 4}
    
    def effect(self, player):
        '''
        触发事件效果

        Parameters:
        player: Player
            事件作用的玩家对象
        '''
        enemy_group = combat.create_enemy_group(player.lvl, enemies.possible_enemies, self.enemy_quantity_for_level)
        combat.combat(player, enemy_group)

class FixedCombatEvent(Event):
    '''
    继承 Event 类。用于固定战斗（BOSS 战、任务战斗等）。

    Attributes:
    enemyList: list
        需要战斗的敌人列表
    '''
    def __init__(self, name, enemyList) -> None:
        super().__init__(name, 10, True)
        self.enemyList = enemyList

    def effect(self, player):
        '''
        触发事件效果

        Parameters:
        player: Player
            事件作用的玩家对象
        '''
        combat.combat(player, self.enemyList)


class ShopEvent(Event):
    '''
    继承 Event 类。用于商店事件。

    Attributes:
    encounter: str
        遇到商店时的描述文本
    enter: str
        进入商店时的描述文本
    talk: str
        与店主交谈时的描述文本
    exit: str
        离开商店时的描述文本
    itemSet: list
        商店内可售卖的物品类别列表
    quest: Quest
        交谈时可接受的任务
    '''
    def __init__(self, name, isUnique, encounterText, enterText, talkText, exitText, itemSet, quest) -> None:
        super().__init__(name, 100, isUnique)
        self.encounter = encounterText
        self.enter = enterText
        self.exit = exitText
        self.talk = talkText
        self.itemSet = itemSet
        self.quest = quest
    
    def effect(self, player):
        '''
        触发事件效果

        Parameters:
        player: Player
            事件作用的玩家对象
        '''
        print(self.encounter)
        enter = input("> ").lower()
        while enter not in ['y', 'n']:
            enter = input("> ").lower()
        if enter == 'y':
            print(self.enter)
            vendor = shops.Shop(self.itemSet)
            text.shop_menu(player)
            option = input("> ").lower()
            while option != 'e':
                if option == 'b':
                    player.buy_from_vendor(vendor)
                elif option == 's':
                    player.money += player.inventory.sell_item()
                elif option == 't':
                    if self.quest != None and self.quest.status == 'Not Active':
                        self.quest.propose_quest(player)
                    else:
                        print(self.talk)
                text.shop_menu(player)
                option = input("> ").lower()
        print(self.exit)

class HealingEvent(Event):
    '''
    继承 Event 类。用于治疗类事件。

    Attributes:
    encounter: str
        遭遇事件时的描述文本
    success: str
        事件成功时的描述文本
    fail: str
        事件失败时的描述文本
    refuse: str
        玩家拒绝参与事件时的描述文本
    healingAmount: int
        事件成功时恢复的生命值
    '''
    def __init__(self, name, encounterText, successText, failText, refuseText, successChance, isUnique, healingAmount) -> None:
        super().__init__(name, successChance, isUnique)
        self.encounter = encounterText
        self.success = successText
        self.fail = failText
        self.refuse = refuseText
        self.healingAmount = healingAmount

    def effect(self, player):
        '''
        触发事件效果。

        Parameters:
        player: Player
            事件作用的玩家对象
        '''
        print(self.encounter)
        accept = input("> ").lower()
        while accept not in ['y', 'n']:
            accept = input("> ").lower()
        if accept == 'y':
            if self.check_success():
                print(self.success)
                player.heal(self.healingAmount)
            else:
                print(self.fail)
        elif accept == 'n':
            print(self.refuse)

class InnEvent(HealingEvent):
    '''
    继承 HealingEvent 类。该事件总是成功，但需要支付一定费用。

    Attributes:
    cost: int
        治疗的费用
    '''
    def __init__(self, name, encounterText, successText, failText, refuseText, healingAmount, cost) -> None:
        super().__init__(name, encounterText, successText, failText, refuseText, 100, False, healingAmount)
        self.cost = cost

    def effect(self, player):
        '''
        触发事件效果。

        Parameters:
        player: Player
            事件作用的玩家对象
        '''
        print(self.encounter)
        accept = input("> ").lower()
        while accept not in ['y', 'n']:
            accept = input("> ").lower()
        if accept == 'y':
            if player.money >= self.cost:
                print(self.success)
                player.heal(self.healingAmount)
                player.money -= self.cost
            else:
                print(self.fail)
        elif accept == 'n':
            print(self.refuse)

# 任务
# -> 凯撒鲁斯
caesarus_bandit_combat = FixedCombatEvent('凯撒鲁斯与他的强盗', enemies.enemy_list_caesarus_bandit)
quest_caesarus_bandit = quest.Quest('凯撒鲁斯与他的强盗', text.quest_caesarus_bandit_text, text.shop_quest_caesarus_bandits, 100, 100, None, caesarus_bandit_combat, 5)

# 事件实例
random_combat = RandomCombatEvent('随机战斗')
shop_rik_armor = ShopEvent('里克的护甲店', False, text.rik_armor_shop_encounter, text.rik_armor_shop_enter, 
                           text.rik_armor_shop_talk, text.rik_armor_shop_exit, items.rik_armor_shop_item_set, quest_caesarus_bandit)
shop_itz_magic = ShopEvent('伊兹魔法店', False, text.itz_magic_encounter, text.itz_magic_enter, 
                           text.itz_magic_talk, text.itz_magic_exit, items.itz_magic_item_set, None)
heal_medussa_statue = HealingEvent('美杜莎雕像', text.medussa_statue_encounter, text.medussa_statue_success,
                                   text.medussa_statue_fail, text.medussa_statue_refuse, 70, False, 20)
inn_event = InnEvent('旅馆', text.inn_event_encounter, text.inn_event_success, text.inn_event_fail, 
                     text.inn_event_refuse, 50, 15)

# 事件分类
combat_event_list = [random_combat]
shop_event_list = [shop_itz_magic, shop_rik_armor]
heal_event_list = [heal_medussa_statue, inn_event]

# 按类型分类的事件列表
event_type_list = [combat_event_list, shop_event_list, heal_event_list]