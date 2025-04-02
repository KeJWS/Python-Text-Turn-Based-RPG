class Quest():
    '''
    定义任务，并处理任务的激活、完成和奖励发放。

    Attributes:
    name : str
        任务名称。
    description : str
        任务描述。
    proposalText : str
        任务发布时的文本信息。
    xpReward : int
        任务完成后获得的经验值奖励。
    goldReward : int
        任务完成后获得的金币奖励。
    itemReward : Item
        任务完成后获得的物品奖励。
    status : str
        当前任务的状态。
    event : Event
        任务触发的事件。
    recommendedLvl : int
        建议完成该任务的等级。
    '''
    def __init__(self, name, description, proposalText, xpReward, goldReward, itemReward, event, recommendedLvl) -> None:
        self.name = name
        self.description = description
        self.xpReward = xpReward
        self.goldReward = goldReward
        self.itemReward = itemReward
        # TODO: 修改任务状态的处理方式
        self.status = 'Not Active'
        self.event = event
        self.proposalText = proposalText
        self.recommendedLvl = recommendedLvl

    def activate_quest(self, player):
        '''
        激活任务，并将其添加到玩家的进行中任务列表。

        player : Player
            触发该任务的玩家。
        '''
        if self.status == 'Not Active':
            self.status = 'Active'
            self.event.add_event_to_event_list()
            player.activeQuests.append(self)

    def complete_quest(self, player):
        '''
        完成任务，将其从进行中任务列表移除，并加入已完成任务列表。同时给予奖励。

        player : Player
            完成任务的玩家。
        '''
        if self.status == 'Active':
            self.status = 'Completed'
            player.activeQuests.remove(self)
            player.completedQuests.append(self)
            self.give_rewards(player)

    def show_info(self):
        '''
        显示该任务的详细信息。
        '''
        print(f'\n - {self.name} - ')
        print(f'建议等级: {self.recommendedLvl}')
        print(self.description)
        print('奖励:')
        if self.xpReward > 0:
            print(f'XP: {self.xpReward}')
        if self.goldReward > 0:
            print(f'G: {self.goldReward}')
        if self.itemReward != None:
            print(f'Item: {self.itemReward.name}')
        print('')

    def give_rewards(self, player):
        '''
        给予玩家任务奖励。

        Parameters:
        player : Player
            领取奖励的玩家。
        '''
        print(f'任务 \"{self.name}\" 已完成。你获得 {self.xpReward} 经验值 和 {self.goldReward} 金币')
        if self.xpReward > 0:
            player.add_exp(self.xpReward)
        if self.goldReward > 0:
            player.money += self.goldReward
        if self.itemReward != None:
            self.itemReward.add_to_inventory(player.inventory())
    
    def propose_quest(self, player):
        '''
        向玩家发布任务，玩家可以选择接受或拒绝。

        Parameters:
        player : Player
            被提议任务的玩家。
        '''
        print(self.proposalText)
        print(f'是否接受？ [y/n] (建议等级: {self.recommendedLvl})')
        option = input("> ").lower()
        while option not in ['y', 'n']:
            option = input("> ").lower()
        if option == 'y':
            self.activate_quest(player)