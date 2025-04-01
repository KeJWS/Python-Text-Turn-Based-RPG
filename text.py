from constants import VERSION

def title_screen():
    print('############################')
    print('# Welcome to the text RPG! #')
    print('############################')
    print('#         1 - Play         #')
    print('#         2 - About        #')
    print('#         3 - Quit         #')
    print('############################')

def about_menu():
    print(f'Python 文字回合制 RPG 系统 v{VERSION}')
    print('作者：Pablo Rodríguez Martín (@rodmarkun)')
    print('\n你好！你眼前所见的是一个使用 Python 语言构建的回合制 RPG 系统。\
\n请注意，这更侧重于构建一个系统，而非完整的游戏。')
    print('你可以与敌人战斗，从商店购买道具，完成任务，学习法术和连招……')
    print('\n强烈推荐你查看代码，并根据需要进行修改。祝你玩得开心！')


def play_menu():
    print('############################')   
    print('#        1 - Walk          #')
    print('#      2 - See stats       #')
    print('#      3 - Aptitudes       #')
    print('#      4 - Inventory       #')
    print('#        5 - Quests        #')
    print('############################')

def showStats(player):
    print('############################')
    print('#          STATS           #')
    print('############################')
    print('HP: {}/{}'.format(player.stats['hp'], player.stats['maxHp']))
    print('MP: {}/{}'.format(player.stats['mp'],  player.stats['maxMp']))
    print('ATK: {}'.format(player.stats['atk']))
    print('DEF: {}'.format(player.stats['def']))
    print('MATK: {}'.format(player.stats['matk']))
    print('MDEF: {}'.format(player.stats['mdef']))
    print('SPD: {}'.format(player.stats['speed']))
    print('CRIT: {}'.format(player.stats['critCh']))
    print('############################')
    print('#        APTITUDES         #')
    print('############################')
    print('STR: {}'.format(player.aptitudes['str']))
    print('DEX: {}'.format(player.aptitudes['dex']))
    print('INT: {}'.format(player.aptitudes['int']))
    print('WIS: {}'.format(player.aptitudes['wis']))
    print('CONST: {}'.format(player.aptitudes['const']))
    print('############################')
    print('MONEY: {}'.format(player.money))
    print('############################')
    print('#        EQUIPMENT         #')
    print('############################')
    for equipment in player.equipment:
        if player.equipment[equipment] is not None:
            print('{}: {}'.format(equipment, player.equipment[equipment].name))
        else:
            print('{}:'.format(equipment))

def showAptitudes(player):
    print('############################')
    print('#        POINTS: {}        #'.format(player.aptitudePoints))
    print('#    SELECT AN APTITUDE    #')
    print('############################')
    print('1 - STR (Current: {})'.format(player.aptitudes['str']))
    print('2 - DEX (Current: {})'.format(player.aptitudes['dex']))
    print('3 - INT (Current: {})'.format(player.aptitudes['int']))
    print('4 - WIS (Current: {})'.format(player.aptitudes['wis']))
    print('5 - CONST (Current: {})'.format(player.aptitudes['const']))
    print('Q - Quit menu')
    print('############################')

def inventory_menu():
    print('############################')
    print('#    U - Use an item       #')
    print('#    D - Drop an item      #')
    print('#    E - Equip an item     #')
    print('#        Q - Quit          #')
    print('############################')

def combat_menu(player, allies, enemies):
    print('############################')
    print('{} - HP: {}/{} - MP: {}/{} - CP: {}'.format(player.name, player.stats['hp'], player.stats['maxHp'],
                                                player.stats['mp'], player.stats['maxMp'], player.comboPoints))
    for ally in allies:
        if ally != player:
            print('{} - HP: {}/{}'.format(ally.name, ally.stats['hp'], ally.stats['maxHp']))
    print('-----------------------------')
    for enemy in enemies:
        print('{} - HP: {}/{}'.format(enemy.name, enemy.stats['hp'], enemy.stats['maxHp']))
    print('############################')
    print('#       A - Attack         #')
    print('#       C - Combos         #')
    print('#       S - Spells         #')
    print('############################')

def spell_menu(player):
    print('############################')
    print('     SPELLS ["0" to Quit]   ')
    print('############################')
    index = 1
    for s in player.spells:
            print(str('{} - {} - {}MP'.format(index, s.name, s.cost)))
            index += 1

def combo_menu(player):
    print('############################')
    print('     COMBOS ["0" to Quit]   ')
    print('############################')
    index = 1
    for c in player.combos:
            print(str('{} - {} - {}CP'.format(index, c.name, c.cost)))
            index += 1

def select_objective(targets):
    print('############################')
    print('    Select an objective:    ')
    print('############################')
    index = 1
    for t in targets:
        print('{} - {} - HP: {}/{}'.format(index, t.name, t.stats['hp'], t.stats['maxHp']))
        index += 1
    print('############################')

def shop_menu(player):
    print('############################')
    print('      SHOP - Money: {}      '.format(player.money))
    print('############################')
    print('       B - Buy Items        ')
    print('       S - Sell Items       ')
    print('         T - Talk           ')
    print('         E - Exit           ')
    print('############################')

def shop_buy(player):
    print('############################')
    print('      SHOP - Money: {}      '.format(player.money))
    print('       ["0" to Quit]        ')
    print('############################')

def enter_shop(name):
    if name == 'Rik\'s Armor Shop':
        print(rik_armor_shop_encounter)
    elif name == 'Itz Magic':
        print(itz_magic_encounter)
    
### 事件文本

# 初始事件
initial_event_text = '这一天终于到来了。你已在冒险者公会登记了自己的姓名。\n\
作为礼物，他们允许你从三套装备中选择一套。你会选择哪一套？\n\
1 - 战士套装\n\
2 - 盗贼套装\n\
3 - 魔法师套装'

## 商店

# Rik 的护甲店
rik_armor_shop_encounter = '在一个小村庄四处游荡时，你发现自己站在一家店铺前。\n\
门上挂着一块招牌，上面写着：<Rik 的护甲店>。\n\
要进入吗？[y/n]'
rik_armor_shop_enter = '“你好，朋友！你需要点什么？” 一个身材魁梧的男子问道。'
rik_armor_shop_talk = '' # 交谈内容
rik_armor_shop_exit = '你离开了村庄，继续踏上冒险之旅。'

# Itz 的魔法店
itz_magic_encounter = '你误入了一片沼泽。环顾四周，你发现一座小屋。\n\
门上挂着一块招牌，上面写着：<Itz 的魔法店>。\n\
要进入吗？[y/n]'
itz_magic_enter = '屋内站着一位戴着厚重眼镜的矮小女子，她看上去像是一位女巫。\n\
她低声呢喃道：“哦？看看是谁来了……来吧，随意看看！”'
itz_magic_talk = '' # 交谈内容
itz_magic_exit = '你离开了沼泽，继续踏上旅程。'


## 治疗

# 美杜莎神像
medussa_statue_encounter = '在一座山丘的顶端，你发现了一座小型神殿。\n\
这里矗立着一尊古老而被遗忘的女神雕像。\n\
不知为何，你心生敬意，想要向它致敬。\n\
要跪拜吗？[y/n]'
medussa_statue_success = '你感受到一股温暖的力量流遍全身。'
medussa_statue_fail = '什么也没有发生，或许只是你的错觉。'
medussa_statue_refuse = '你决定不跪拜。'

# 客栈事件
inn_event_encounter = '在穿越森林的途中，你发现了一家客栈。\n\
你可以在这里休息，但需要支付一定的费用。\n\
支付 15G 住一晚吗？[y/n]'
inn_event_success = '你在柔软舒适的床上安然入睡。'
inn_event_fail = '你的钱不够。'
inn_event_refuse = '你决定不支付住宿费。'

## 任务
quest_caesarus_bandit_text = '凯撒鲁斯和他的匪徒一直在\n\
骚扰附近的村庄。去解决他们吧。'
shop_quest_caesarus_bandits = '听说过那群强盗吗？他们一直在恐吓\n\
这一带的村庄。一个叫凯撒鲁斯的家伙是他们的首领。\n\
如果你能解决他们，也许村民会给你一些报酬。'
