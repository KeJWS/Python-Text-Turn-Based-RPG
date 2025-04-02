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
            return dmg * rate
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
Main combat loop
'''

def combat(myPlayer, enemies):
    '''
    Handles the main combat loop between allies and enemies.

    Parameters:
    myPlayer : Player
        Actual player
    enemies : list     
        List of enemies to combat

    Note:
    myPlayer should be changed to be a list named 'allies' if you can begin
    the combat with multiple allies. Currently, you can only get allies
    via summoning spells so this was not necessary.
    '''
    # All battlers are inserted into the Battlers list and ordered by speed (turn order)
    allies = [myPlayer] # List of current allies
    battlers = define_battlers(allies, enemies) # List of current Battlers (Allies + Enemies)

    # Sum of all exp and money the enemies drop when defeated
    enemy_exp = 0 
    enemy_money = 0

    print('############################')
    for enemy in enemies:
        print(f'A wild {enemy.name} has appeared!')
        enemy_exp += enemy.xpReward
        enemy_money += enemy.goldReward
    # The battle will go on while the player is still alive and there are still enemies to defeat
    while myPlayer.alive and len(enemies) > 0:
        # Battlers should be updated for speed changes (buffs/debuffs)
        battlers = define_battlers(allies, enemies)
        # Each battler has its turn
        for battler in battlers:
            # Player can choose its actions
            if type(battler) == player.Player:
                text.combat_menu(myPlayer, allies, enemies)
                cmd = input('> ').lower()
                while cmd not in ['a', 'c', 's']:
                    print('Please enter a valid command')
                    cmd = input('> ').lower()
                # Perform a normal attack
                if 'a' in cmd:
                    targeted_enemy = select_target(enemies)
                    battler.normal_attack(targeted_enemy)
                    check_if_dead(allies, enemies, battlers)
                # Cast a spell
                elif 's' in cmd:
                    spell_menu(myPlayer, battlers, allies, enemies)
                # Use a combo
                elif 'c' in cmd:
                    combo_menu(myPlayer, battlers, allies, enemies)
            else:
                # Allies attack a random enemy
                if battler.isAlly:
                    if len(enemies) > 0:
                        randomEnemy = random.choice(enemies)
                        battler.normal_attack(randomEnemy)
                        check_if_dead(allies, enemies, battlers)
                else:
                    # For now, enemies will just perform a normal attack against the player.
                    # This can be expanded to work as a functional AI
                    randomAlly = random.choice(allies)
                    battler.normal_attack(randomAlly)
                    check_if_dead(allies, enemies, battlers)

        # A turn has passed
        # Check turns for buffs and debuffs
        for battler in battlers:
            check_turns_buffs_and_debuffs(battler, False)
    if myPlayer.alive:
        # Deactivate all existent buffs and debuffs
        check_turns_buffs_and_debuffs(myPlayer, True)
        # Add experience to players
        myPlayer.add_exp(enemy_exp)
        myPlayer.add_money(enemy_money)
        # Restart Combo Points
        myPlayer.comboPoints = 0

def define_battlers(allies, enemies):
    '''
    Returns the battlers list, ordered by speed (turn order).

    Parameters:
    allies : List
        List of ally Battlers
    enemies : List
        List of enemy Battlers

    Returns:
    battlers : List
        List of enemies + allies, ordered by speed
    '''
    battlers = enemies.copy()
    for ally in allies:
        battlers.append(ally)
    battlers.sort(key=lambda b: b.stats['speed'], reverse=True)
    return battlers

# Select a certain target from the battlefield
def select_target(targets):
    '''
    Selects a certain target from the battlefield.

    Parameters:
    targets : list
        List of all possible target Battlers

    Return:
    target : Battler
        Selected target
    '''
    text.select_objective(targets)
    # TODO: There must be an easier way to do this
    valid_target = False
    while not valid_target:
        valid_int = False
        while not valid_int:
            i = input("> ")
            try:
                i = int(i)
                valid_int = True
            except:
                print('Please enter a number')
        if i not in range(len(targets)+1):
            print('Select a valid target')
            valid_target = False
        else:
            valid_target = True
    target = targets[i-1]
    return target

def spell_menu(myPlayer, battlers, allies, enemies):
    '''
    Player selects a target spell to cast.

    Parameters:
    myPlayer : Player
        Player caster of the spell.
    battlers : List
        List of Battlers in the combat.
    allies : List
        List of allies in the combat.
    enemies : List
        List of enemies in the combat.
    '''
    text.spell_menu(myPlayer)
    option = int(input("> "))
    while option not in range(len(myPlayer.spells)+1):
        print('Please enter a valid number')
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
    Player selects a target combo to perform.

    Parameters:
    myPlayer : Player
        Player that performs the combo.
    battlers : List
        List of Battlers in the combat.
    allies : List
        List of allies in the combat.
    enemies : List
        List of enemies in the combat.
    '''
    text.combo_menu(myPlayer)
    option = int(input("> "))
    while option not in range(len(myPlayer.combos)+1):
        print('Please enter a valid number')
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

# Returns True if attack misses, False if it doesn't
def check_miss(attacker, defender):
    '''
    Checks if an attack misses or not. Miss chance is determined by the following formula:

    chance = math.floor(math.sqrt(max(0, (5 * defender.stats['speed'] - attacker.stats['speed'] * 2))))

    I tried different formulas and this one ended up being pretty competent. Check if
    it fits you anyway.

    Parameters:
    attacker : Battler
        Battler that performs the attack
    defender : Battler
        Defending battler

    Returns:
    True/False : Bool
        True if the attack missed. False if it doesn't.
    '''
    chance = math.floor(math.sqrt(max(0, (5 * defender.stats['speed'] - attacker.stats['speed'] * 2))))
    if chance > random.randint(0, 100):
        print(f'{attacker.name}\'s attack missed!')
        return True
    return False

def check_turns_buffs_and_debuffs(target, deactivate):
    '''
    Checks if buffs and debuffs should still be active (checks its turn count).

    Parameters:
    target : Battler
        Battler whose buffs and debuffs should be checked
    deactivate : bool
        If true, buffs and debuffs deactivate instantly regardless of turn count
        (useful when ending a combat or any similar situation). If false, acts
        normally.
    '''
    if deactivate:
        for bd in target.buffsAndDebuffs:
            bd.deactivate()
    else:
        for bd in target.buffsAndDebuffs:
            bd.check_turns()

# Checks if a battler is dead and removes it from the appropiate lists
def check_if_dead(allies, enemies, battlers):
    '''
    Checks if current battlers are dead and if they are, removes them from
    the corresponding lists.

    Parameters:
    allies : List
        List of ally Battlers
    enemies : List
        List of enemy Battlers
    battlers : List
        List of all battlers
    '''
    # TODO: This can probably be done in an easier way, but iterating
    # while deleting objects leads to weird stuff happening.
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
    Fully heals a target.

    Parameters:
    target : Battler
        Battler to fully heal
    '''
    target.stats['hp'] = target.stats['maxHp']

def fully_recover_mp(target):
    '''
    Fully recovers target's mp.

    Parameters:
    target : Battler
        Battler to fully recover
    '''
    target.stats['mp'] = target.stats['maxMp']

def create_enemy_group(lvl, possible_enemies, enemy_quantity_for_level):
    '''
    Creates a corresponding group of enemies depending on player's lvl

    Parameters:
    lvl : int
        Player's lvl
    possible_enemies : Dictionary
        Dictionary of enemies to appear and their respective lvl range,
        follows this syntax: {enemyClass : (lowestLvlToAppear, highestLvlToAppear)}
    enemy_quantity_for_level : Dictionary
        Dictionary of number of enemies to appear based on level,
        follows this syntax: {levelUpToThisQuantityToAppear, Quantity}
        for example, {3 : 1} means that up to level 3, only 1 enemy will appear.

    Returns:
    enemy_group : List
        List of enemy Battlers to appear
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
    # Select x enemies, being x a random number between 1 and max_enemies
    for i in range(random.randint(1, max_enemies)):
        enemy_instance = random.choice(enemies_to_appear)()
        enemy_group.append(enemy_instance)
    return enemy_group