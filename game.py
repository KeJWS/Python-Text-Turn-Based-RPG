# Python文本冒险RPG
# Pablo Rodríguez Martín - @rodmarkun

import sys
import random
import text, player, items, events

##### 标题画面 #####
def title_screen_selections():
    '''
    标题画面的选项，包括开始游戏、获取帮助或退出。
    '''
    alive = True
    while alive:
        text.title_screen()
        option = input("> ")
        while option not in ['1', '2', '3']:
            print("请输入有效的指令")
            option = input("> ")
        if option == '1':
            alive = play()
        elif option == '2':
            text.about_menu()
        elif option == '3':
            sys.exit()

##### 背包菜单 #####
def inventory_selections(player):
    '''
    背包菜单，用于使用、丢弃或装备物品。

    Parameters:
    player : Player
        需要访问其背包的玩家。
    '''
    option = input("> ")
    while option.lower() != 'q':
        if option.lower() == 'u':
            player.use_item(player.inventory.use_item())
        elif option.lower() == 'd':
            player.inventory.drop_item()
        elif option.lower() == 'e':
            player.equip_item(player.inventory.equip_item())
        else:
            pass
        option = input("> ")

##### 初始化函数 #####
def play():
    '''
    主函数，用于进行游戏。

    Returns:
    alive : bool
        当游戏结束（玩家死亡）时返回False。
    '''
    # 玩家实例化
    myPlayer = player.Player("测试玩家")

    give_initial_items(myPlayer)

    # 事件发生几率（以%计算）
    combat_chance = 65
    shop_chance = 20
    heal_chance = 15

    while myPlayer.alive:
        text.play_menu()
        option = input("> ")
        if option == '1':
            generate_event(myPlayer, combat_chance, shop_chance, heal_chance)
        elif option == '2':
            text.showStats(myPlayer)
        elif option == '3':
            myPlayer.assign_aptitude_points()
        elif option == '4':
            text.inventory_menu()
            myPlayer.inventory.show_inventory()
            inventory_selections(myPlayer)
        elif option == '5':
            myPlayer.show_quests()
        else:
            print("请输入有效的指令")
    return False

def give_initial_items(myPlayer):
    '''
    根据选择给予玩家初始物品。

    Parameters:
    myPlayer : Player
        需要给予初始物品的玩家。
    '''
    print(text.initial_event_text)
    option = str(input("> "))
    while option not in ['1', '2', '3']:
        option = str(input("> "))
    if option == '1':
        items.rustySword.add_to_inventory_player(myPlayer.inventory)
        items.noviceArmor.add_to_inventory_player(myPlayer.inventory)
    elif option == '2':
        items.brokenDagger.add_to_inventory_player(myPlayer.inventory)
        items.noviceArmor.add_to_inventory_player(myPlayer.inventory)
    elif option == '3':
        items.oldStaff.add_to_inventory_player(myPlayer.inventory)
        items.oldRobes.add_to_inventory_player(myPlayer.inventory)
        items.grimoireFireball.add_to_inventory_player(myPlayer.inventory)
    print('[ 请记得在背包中装备这些物品 > 装备物品 ]')

def generate_event(myPlayer, combat_chance, shop_chance, heal_chance):
    '''
    根据指定几率生成随机事件。
    还处理任务完成。

    Parameters:
    myPlayer : Player
        受事件影响的玩家
    combat_chance : int
        生成战斗事件的几率（%）
    shop_chance : int
        生成商店事件的几率（%）
    heal_chance : int
        生成治疗事件的几率（%）
    '''
    eventList = random.choices(events.event_type_list, weights=(combat_chance, shop_chance, heal_chance), k=1)
    # random.choices 返回一个列表，因此需要使用 eventList[0]
    event = random.choice(eventList[0])
    event.effect(myPlayer)
    # TODO: 可能有更简单的方法处理此逻辑。
    if event.isUnique:
        for evList in events.event_type_list:
            for e in evList:
                if e.name == event.name:
                    for quest in myPlayer.activeQuests:
                        if quest.event == event:
                            quest.complete_quest(myPlayer)
                    evList.remove(event)
                    break


if __name__ == "__main__":
    title_screen_selections()