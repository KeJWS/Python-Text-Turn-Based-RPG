
```python
##### 标题画面 #####
def title_screen_selections():
    '''
    标题画面的选项，包括开始游戏、获取帮助或退出。
    '''
    alive = True
    while alive:
    while option not in ['1', '2', '3']:
        print("请输入有效的指令")
        option = input("> ")
    if option == '1':
        alive = play()
    elif option == '2':
        text.about_menu()
    elif option == '3':
        sys.exit()
```

------------------------------------------------

```python
##### 初始化函数 #####
def play():
    '''
    运行游戏主循环。
    '''
    print("[DEBUG] 游戏开始")
    myPlayer = player.Player("测试玩家")
    give_initial_items(myPlayer)
    event_chances = (65, 20, 15)  # 战斗、商店、治疗的概率
    while myPlayer.alive:
        text.play_menu()
        options = {'1': lambda: generate_event(myPlayer, *event_chances),
                   '2': lambda: text.showStats(myPlayer),
                   '3': myPlayer.assign_aptitude_points,
                   '4': lambda: (text.inventory_menu(), myPlayer.inventory.show_inventory(), inventory_selections(myPlayer)),
                   '5': myPlayer.show_quests}
        options.get(input("> "), lambda: print("请输入有效的指令"))()
    return False
```
