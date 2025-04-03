import math
import random
import player
import text

class Battler():
    '''
    所有可以参与战斗的实例的父类。
    Battler 将始终是敌人、玩家的盟友或玩家本人。

    Attributes:
    name : str
        战斗者的名称。
    stats : dict
        战斗者的属性，字典格式，例如：{'atk' : 3}。
    alive : bool              
        表示战斗者是否存活的布尔值。
    buffsAndDebuffs : list     
        战斗者当前拥有的增益和减益列表。
    isAlly : bool             
        表示战斗者是否为玩家的盟友的布尔值。
    '''
    def __init__(self, name, stats) -> None:
        self.name = name
        self.stats = stats
        self.alive = True
        self.buffsAndDebuffs = []
        self.isAlly = False

    def take_dmg(self, dmg):
        '''
        战斗者受到来自任何来源的伤害的函数。
        从其生命值中减去伤害量，同时检查是否死亡。

        Parameters:
        dmg : int     
            造成的伤害数量
        '''
        if dmg < 0: dmg = 0
        self.stats['hp'] -= dmg
        print(f'{self.name} 受到 \033[33m{dmg}\033[0m 点伤害！')
        # 防御者死亡
        if self.stats['hp'] <= 0:
            print(f'\033[31m{self.name} 被击杀了。\033[0m')
            self.alive = False

    def normal_attack(self, defender):
        '''
        所有战斗者都有的普通攻击。

        伤害计算如下：
        attacker_atk * (100 / (100 + defender_def * 1.5))

        Parameters:
        defender : Battler
            防御的战斗者

        Returns:
        dmg : int        
            对防御者造成的伤害
        '''
        print(f'{self.name} 发动攻击！')

        # TODO: 需要更好的伤害计算公式
        dmg = round(self.stats['atk'] * (100 / (100 + defender.stats['def'] * 1.5)))
        # 检查是否为暴击
        dmg = self.check_critical(dmg)
        # 检查是否攻击未命中
        if not check_miss(self, defender):
            defender.take_dmg(dmg)
        else:
            dmg = 0
        return dmg

    def check_critical(self, dmg):
        '''
        检查攻击是否为暴击。如果是，则伤害翻倍。

        暴击几率来源于战斗者的属性：'critCh'

        Parameters:
        dmg : int     
            基础伤害

        Returns:
        dmg : int 
            经过检查和处理后的伤害
        '''
        if self.stats['critCh'] >= 100 or self.stats['critCh'] > random.randint(1, 100):
            # 暴击倍率 : 概率
            critical_rates = {
            1.5: 50,
            2.0: 30,
            2.5: 15,
            3.0: 5
            }
            # 使用加权随机选择暴击倍率
            rate = random.choices(list(critical_rates.keys()), weights=critical_rates.values())[0]
            print(f'\033[1;33m暴击！x{rate}\033[0m')
            return round(dmg * rate)
        else:
            return dmg

    def recover_mp(self, amount):
        '''
        战斗者恢复一定量的 'mp'（法力值）。

        Parameters:
        amount : int      
            恢复的法力值
        '''
        if self.stats['mp'] + amount > self.stats['maxMp']:
            fully_recover_mp(self)
        else:
            self.stats['mp'] += amount
        print(f'{self.name} 恢复了 \033[34m{amount}\033[0m 点法力值！')

    def heal(self, amount):
        '''
        战斗者恢复一定量的 'hp'（生命值）。

        Parameters:
        amount : int     
            恢复的生命值
        '''
        if self.stats['hp'] + amount > self.stats['maxHp']:
            fully_heal(self)
        else:
            self.stats['hp'] += amount
        print(f'{self.name} 恢复了 \033[31m{amount}\033[0m 点生命值！')

class Enemy(Battler):
    '''
    所有敌人的基类。继承自 'Battler' 类。

    Attributes:
    xpReward : int    
        被击杀时给予的经验值（XP）数量
    goldReward : int 
        被击杀时给予的金币数量
    '''
    def __init__(self, name, stats, xpReward, goldReward) -> None:
        super().__init__(name, stats)
        self.xpReward = xpReward
        self.goldReward = goldReward


'''
主战斗循环
'''

def combat(myPlayer, enemies):
    '''
    处理玩家与敌人之间的主要战斗循环。

    Parameters:
    myPlayer : Player
        当前玩家对象
    enemies : list     
        需要战斗的敌人列表

    备注:
    如果战斗支持多个盟友，应将 myPlayer 替换为名为 'allies' 的列表。
    目前，只有通过召唤技能才能获得盟友，因此暂未做此修改。
    '''
    # 所有战斗单位（包括玩家和敌人）按速度排序，决定回合顺序
    allies = [myPlayer] # 当前盟友列表
    battlers = define_battlers(allies, enemies) # 参与战斗的单位（盟友 + 敌人）

    # 统计敌人掉落的经验值和金钱
    enemy_exp = 0 
    enemy_money = 0

    print('############################')
    for enemy in enemies:
        print(f'野生的 {enemy.name} 出现了！')
        enemy_exp += enemy.xpReward
        enemy_money += enemy.goldReward

    # 只要玩家存活且仍有敌人，战斗就会持续
    while myPlayer.alive and len(enemies) > 0:
        # 由于速度可能因增益/减益效果改变，需要更新战斗顺序
        battlers = define_battlers(allies, enemies)

        # 每个战斗单位轮流行动
        for battler in battlers:
            # 玩家回合：选择行动
            if type(battler) == player.Player:
                text.combat_menu(myPlayer, allies, enemies)
                cmd = input('> ').lower()
                while cmd not in ['a', 'c', 's']:
                    print('请输入有效指令')
                    cmd = input('> ').lower()
                # 普通攻击
                if 'a' in cmd:
                    targeted_enemy = select_target(enemies)
                    battler.normal_attack(targeted_enemy)
                    check_if_dead(allies, enemies, battlers)
                # 施放技能
                elif 's' in cmd:
                    spell_menu(myPlayer, battlers, allies, enemies)
                # 使用连招
                elif 'c' in cmd:
                    combo_menu(myPlayer, battlers, allies, enemies)
            else:
                # 盟友自动攻击随机敌人
                if battler.isAlly:
                    if len(enemies) > 0:
                        randomEnemy = random.choice(enemies)
                        battler.normal_attack(randomEnemy)
                        check_if_dead(allies, enemies, battlers)
                else:
                    # 目前敌人只会进行普通攻击，未来可扩展为完整的AI逻辑
                    randomAlly = random.choice(allies)
                    battler.normal_attack(randomAlly)
                    check_if_dead(allies, enemies, battlers)
        # 回合结束，检查增益和减益的持续时间
        for battler in battlers:
            check_turns_buffs_and_debuffs(battler, False)

    if myPlayer.alive:
        # 移除所有增益和减益效果
        check_turns_buffs_and_debuffs(myPlayer, True)
        # 给予玩家经验值和金钱奖励
        myPlayer.add_exp(enemy_exp)
        myPlayer.add_money(enemy_money)
        # 重置连招点数
        myPlayer.comboPoints = 0

def define_battlers(allies, enemies):
    '''
    返回战斗单位列表，并按速度排序（决定回合顺序）。

    Parameters:
    allies : List
        盟友单位列表
    enemies : List
        敌方单位列表

    Returns:
    battlers : List
        包含敌人和盟友的战斗单位列表，按速度排序
    '''
    battlers = enemies.copy()
    for ally in allies:
        battlers.append(ally)
    battlers.sort(key=lambda b: b.stats['speed'], reverse=True)
    return battlers

# 选择战斗目标
def select_target(targets):
    '''
    从战场中选择一个目标。

    Parameters:
    targets : list
        可选目标单位列表

    Return:
    target : Battler
        选中的目标
    '''
    text.select_objective(targets)
    # TODO：必须有一种更简单的方法来做到这一点
    valid_target = False
    while not valid_target:
        valid_int = False
        while not valid_int:
            i = input("> ")
            try:
                i = int(i)
                valid_int = True
            except:
                print('请输入数字')
        if i not in range(len(targets)+1):
            print('请选择一个有效目标')
            valid_target = False
        else:
            valid_target = True
    target = targets[i-1]
    return target

def spell_menu(myPlayer, battlers, allies, enemies):
    '''
    让玩家选择一个目标施放法术。

    Parameters:
    myPlayer : Player
        施放法术的玩家。
    battlers : List
        战斗中的所有参战者列表。
    allies : List
        友方单位列表。
    enemies : List
        敌方单位列表。
    '''
    text.spell_menu(myPlayer)
    option = int(input("> "))
    while option not in range(len(myPlayer.spells)+1):
        print('请输入有效的数字')
        option = int(input("> "))
    if option != 0:
        spellChosen = myPlayer.spells[option - 1]
        if spellChosen.isTargeted:
            target = select_target(battlers)
            spellChosen.effect(myPlayer, target)
            check_if_dead(allies, enemies, battlers)
        else:
            if spellChosen.defaultTarget == 'self':
                spellChosen.effect(myPlayer, myPlayer)
            elif spellChosen.defaultTarget == 'all_enemies':
                spellChosen.effect(myPlayer, enemies)
                check_if_dead(allies, enemies, battlers)
            elif spellChosen.defaultTarget == 'allies':
                spellChosen.effect(myPlayer, allies)

def combo_menu(myPlayer, battlers, allies, enemies):
    '''
    让玩家选择一个目标执行连招。

    Parameters:
    myPlayer : Player
        进行连招的玩家。
    battlers : List
        战斗中的所有参战者列表。
    allies : List
        友方单位列表。
    enemies : List
        敌方单位列表。
    '''
    text.combo_menu(myPlayer)
    option = int(input("> "))
    while option not in range(len(myPlayer.combos)+1):
        print('请输入有效的数字')
        option = int(input("> "))
    if option != 0:
        comboChosen = myPlayer.combos[option - 1]
        if comboChosen.isTargeted:
            target = select_target(battlers)
            comboChosen.effect(myPlayer, target)
            check_if_dead(allies, enemies, battlers)
        else:
            if comboChosen.defaultTarget == 'self':
                comboChosen.effect(myPlayer, myPlayer)
            elif comboChosen.defaultTarget == 'all_enemies':
                comboChosen.effect(myPlayer, enemies)
                check_if_dead(allies, enemies, battlers)

# 返回 True 代表攻击未命中，返回 False 代表攻击命中
def check_miss(attacker, defender):
    '''
    检查攻击是否命中，命中率由以下公式决定：

    chance = math.floor(math.sqrt(max(0, (5 * defender.stats['speed'] - attacker.stats['speed'] * 2))))

    经过多次尝试，这个公式表现得相对合理。当然，你可以根据需要进行调整。

    Parameters:
    attacker : Battler
        发起攻击的单位。
    defender : Battler
        受到攻击的单位。

    Returns:
    True/False : Bool
        True 代表攻击未命中，False 代表攻击命中。
    '''
    chance = math.floor(math.sqrt(max(0, (5 * defender.stats['speed'] - attacker.stats['speed'] * 2))))
    if chance > random.randint(0, 100):
        print(f'{attacker.name}的攻击未命中！')
        return True
    return False

def check_turns_buffs_and_debuffs(target, deactivate):
    '''
    检查目标的增益和减益状态是否仍然有效（基于回合数判断）。

    Parameters:
    target : Battler
        需要检查状态的单位。
    deactivate : bool
        若为 True，则立即清除所有增益和减益状态（适用于战斗结束等情况）。
        若为 False，则正常检测状态回合数。
    '''
    if deactivate:
        for bd in target.buffsAndDebuffs:
            bd.deactivate()
    else:
        for bd in target.buffsAndDebuffs:
            bd.check_turns()

# 检查参战者是否阵亡，并从相应列表中移除
def check_if_dead(allies, enemies, battlers):
    '''
    检查战斗单位是否阵亡，如果阵亡，则从相应列表中移除。

    Parameters:
    allies : List
        友方单位列表。
    enemies : List
        敌方单位列表。
    battlers : List
        参战单位总列表。
    '''
    # TODO：这可能以更简单的方式完成，但要迭代
    # 删除对象会导致发生奇怪的事情。
    dead_bodies = []
    for ally in allies:
        if ally.alive == False:
            dead_bodies.append(ally)
    for target in enemies:
        if target.alive == False:
            dead_bodies.append(target)
    for dead in dead_bodies:
        if dead in battlers:
            battlers.remove(dead)
        if dead in enemies:
            enemies.remove(dead)
        elif dead in allies:
            allies.remove(dead)

def fully_heal(target):
    '''
    完全恢复目标的生命值。

    Parameters:
    target : Battler
        需要恢复的单位。
    '''
    target.stats['hp'] = target.stats['maxHp']

def fully_recover_mp(target):
    '''
    完全恢复目标的魔法值。

    Parameters:
    target : Battler
        需要恢复的单位。
    '''
    target.stats['mp'] = target.stats['maxMp']

def create_enemy_group(lvl, possible_enemies, enemy_quantity_for_level):
    '''
    根据玩家等级创建敌人小队。

    Parameters:
    lvl : int
        玩家当前等级。
    possible_enemies : Dictionary
        可能出现的敌人及其对应的等级范围，
        采用以下格式：{enemyClass : (最低等级, 最高等级)}
    enemy_quantity_for_level : Dictionary
        根据玩家等级决定敌人数量，
        格式示例：{等级上限 : 敌人数量}，
        例如 {3: 1} 表示 3 级及以下最多出现 1 名敌人。

    Returns:
    enemy_group : List
        生成的敌人单位列表。
    '''

    enemies_to_appear = []
    for enemy in possible_enemies:
        lowlvl, highlvl = possible_enemies[enemy]
        if lowlvl <= lvl <= highlvl:
            enemies_to_appear.append(enemy)
    
    max_enemies = 1
    for max_level in enemy_quantity_for_level:
        if lvl < max_level:
            max_enemies = enemy_quantity_for_level[max_level]
            break

    enemy_group = []
    # 随机选择 x 名敌人，其中 x 为 1 到 max_enemies 之间的随机数
    for i in range(random.randint(1, max_enemies)):
        enemy_instance = random.choice(enemies_to_appear)()
        enemy_group.append(enemy_instance)
    return enemy_group