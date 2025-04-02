# Python文本冒险RPG
# Pablo Rodríguez Martín - @rodmarkun

import sys
import random
import text, player, items, events
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

##### 标题画面 #####
def title_screen_selections():
    '''
    标题画面的选项，包括开始游戏、获取帮助或退出。
    '''
    options = {'1': play, '2': text.about_menu, '3': sys.exit}
    while True:
        text.title_screen()
        option = input("> ")
        if option in options:
            clear_screen()
            print(f"[DEBUG] 选择了选项: {option}")
            return options[option]()
        clear_screen()
        print("请输入有效的指令")

##### 背包菜单 #####
def inventory_selections(player):
    '''
    背包菜单，用于使用、丢弃或装备物品。

    Parameters:
    player: Player
        需要访问其背包的玩家。
    '''
    actions = {'u': lambda: player.use_item(player.inventory.use_item()),
               'd': player.inventory.drop_item,
               'e': lambda: player.equip_item(player.inventory.equip_item())}
    while (option := input("> ").lower()) != 'q':
        clear_screen()
        print(f"[DEBUG] 背包选项: {option}")
        print("u - 使用物品, d - 丢弃物品, e - 装备武具, q - 退出")
        actions.get(option, lambda: None)()

##### 初始化函数 #####
def play():
    '''
    主函数，用于进行游戏。

    Returns:
    alive: bool
        当游戏结束（玩家死亡）时返回False。
    '''
    print("[DEBUG] 游戏开始")
    myPlayer = player.Player("测试玩家")
    give_initial_items(myPlayer)
    event_chances = (65, 20, 15)  # 战斗、商店、治疗的概率
    while myPlayer.alive:
        text.play_menu()
        option = input("> ")
        if option == '1':
            clear_screen()
            generate_event(myPlayer, *event_chances)
        elif option == '2':
            clear_screen()
            text.showStats(myPlayer)
        elif option == '3':
            clear_screen()
            myPlayer.assign_aptitude_points()
        elif option == '4':
            clear_screen()
            text.inventory_menu()
            myPlayer.inventory.show_inventory()
            inventory_selections(myPlayer)
        elif option == '5':
            clear_screen()
            myPlayer.show_quests()
        else:
            clear_screen()
            print("请输入有效的指令")
    return False

def give_initial_items(myPlayer):
    '''
    根据选择给予玩家初始物品。

    Parameters:
    myPlayer: Player
        需要给予初始物品的玩家。
    '''
    print(text.initial_event_text)
    items_map = {'1': [items.rustySword, items.noviceArmor],
                 '2': [items.brokenDagger, items.noviceArmor],
                 '3': [items.oldStaff, items.oldRobes, items.grimoireFireball]}
    while (option := input("> ")) not in items_map:
        pass
    clear_screen()
    print(f"[DEBUG] 选择了初始装备: {option}")
    for item in items_map[option]:
        item.add_to_inventory_player(myPlayer.inventory)
    print('[ \033[31m请记得在背包中装备这些物品\033[0m ]')

def generate_event(myPlayer, combat_chance, shop_chance, heal_chance):
    '''
    根据指定几率生成随机事件。
    还处理任务完成。

    Parameters:
    myPlayer: Player
        受事件影响的玩家
    combat_chance: int
        生成战斗事件的几率（%）
    shop_chance: int
        生成商店事件的几率（%）
    heal_chance: int
        生成治疗事件的几率（%）
    '''
    event = random.choice(random.choices(events.event_type_list, weights=(combat_chance, shop_chance, heal_chance), k=1)[0])
    print(f"[DEBUG] 触发的事件: {event.name}")
    event.effect(myPlayer)
    if event.isUnique:
        for evList in events.event_type_list:
            if event in evList:
                for quest in myPlayer.activeQuests:
                    if quest.event == event:
                        quest.complete_quest(myPlayer)
                evList.remove(event)
                break

if __name__ == "__main__":
    title_screen_selections()