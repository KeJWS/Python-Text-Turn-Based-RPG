class Inventory():
    '''
    管理玩家的背包和物品。可以修改容量限制。
    该类也用于商店。

    Attributes:
    items : List
        当前背包中的物品列表
    '''
    def __init__(self) -> None:
        self.items = []

    def show_inventory(self):
        '''
        显示背包中的所有物品（带索引）。
        '''
        index = 1
        for item in self.items:
            print(str(f'{index} - {item.show_info()}'))
            index += 1

    def drop_item(self):
        '''
        从背包中选择并丢弃一个物品。
        '''
        print('\n你想丢弃哪个物品？["0"退出]')
        self.show_inventory()
        i = int(input("> "))
        if i == 0:
            print('关闭背包...')
        elif i <= len(self.items):
            item = self.items[i-1]
            item.drop()
            if item.amount <= 0:
                self.items.pop(i - 1)
            print('现在你的背包如下：')
            self.show_inventory()

    def sell_item(self):
        '''
        从背包中选择并出售一个物品。

        Returns:
        moneyForItem : int
            出售物品所得的金额。
        '''
        print('\n你想出售哪个物品？["0"退出]')
        self.show_inventory()
        i = int(input("> "))
        if i == 0:
            print('关闭背包...')
            return 0
        elif i <= len(self.items):
            item = self.items[i-1]
            moneyForItem, amountToSell = item.sell()
            self.decrease_item_amount(item, amountToSell)
            return moneyForItem

    def equip_item(self):
        '''
        从背包中选择并装备某个物品（必须是“装备”类型）。

        Returns:
        item : Item
            返回给玩家装备的物品。如果选择了一个不可装备的对象，则返回None。
        '''
        print('\n你想装备哪个物品？["0"退出]')
        self.show_inventory()
        i = int(input("> "))
        if i == 0:
            print('关闭背包...')
            return None
        elif i <= len(self.items):
            item = self.items[i-1]
            if type(item) == Equipment:
                return item
            else:
                print('请选一个可装备的物品。')
                return None

    def use_item(self):
        '''
        从背包中选择并使用某个物品（必须是“消耗品”类型）。

        Returns:
        item : Item
            返回给玩家使用的物品。如果选择了一个不可消耗的对象，则返回None。
        '''
        print('\n你想使用哪个物品？["0"退出]')
        self.show_inventory()
        i = int(input("> "))
        if i == 0:
            print('关闭背包...')
            return None
        elif i <= len(self.items):
            item = self.items[i-1]
            if item.objectType == 'Consumable':
                item.amount -= 1
                if item.amount <= 0:
                    self.items.pop(i - 1)
                return item
            else:
                print('请选一个可消耗的物品。')
                return None

    def decrease_item_amount(self, item, amount):
        '''
        在背包中减少某个物品的数量。
        这是为了商店系统而设定的。

        Parameters:
        item : Item
            要减少数量的物品
        amount : int
            要减少的数量
        '''
        for actualItem in self.items:
            if item.name == actualItem.name:
                actualItem.amount -= amount
                if actualItem.amount <= 0:
                    self.items.remove(actualItem)
            
class Item():
    '''
    物品始终存储在特定的背包中。它们可以是：
    - 装备（武器和盔甲）
    - 消耗品（药水和法典）

    Attributes:
    name : str
        物品名称
    description : str
        物品描述
    amount : int
        该物品在背包中的数量
    individualValue : int
        单个物品的价值（以金币计算）
    objectType : str
        物品类型
    '''
    # TODO: 将物品类型改为继承
    def __init__(self, name, description, amount, individualValue, objectType) -> None:
        self.name = name
        self.description = description
        self.amount = amount
        self.individualValue = individualValue
        self.objectType = objectType

    def drop(self):
        '''
        丢弃一定数量的该物品。丢弃的物品无法恢复。
        '''
        if self.amount == 1:
            print(f'你丢弃了1个{self.name}。')
            self.amount -= 1
        else:
            print(f'你有{self.amount}个此物品，你想丢弃多少？')
            amountToDrop = int(input("> "))
            if amountToDrop > self.amount:
                print('你没有那么多！')
            else:
                self.amount -= amountToDrop
                print(f'你丢弃了{amountToDrop}个{self.name}。')

    def sell(self):
        '''
        出售一定数量的该物品。出售的物品无法恢复。

        Returns:
        moneyToReceive : int
            出售X数量该物品所获得的金币。
        amountToSell : int
            要出售的该物品数量。
        '''
        if self.amount >= 1:
            print('你想出售多少？')
            amountToSell = int(input("> "))
            if amountToSell <= self.amount and amountToSell > 0:
                # 物品以其价值的50%出售
                moneyToReceive = int(round(self.individualValue * 0.5 * amountToSell))
                print(f'你确定要以{moneyToReceive}G出售{amountToSell}个{self.name}吗？[y/n]')
                confirmation = input("> ")
                if confirmation == 'y':
                    print(f'{amountToSell}个{self.name}以{moneyToReceive}出售')
                    return moneyToReceive, amountToSell
                else:
                    pass
            else:
                print(f'你没有那么多{self.name}！')
        return 0, 0

    def buy(self, player):
        '''
        购买一定数量的该物品。

        Parameters:
        player : Player
            购买物品的玩家。
        '''
        if self.amount > 1:
            print('你想购买多少？')
            amountToBuy = int(input("> "))
            price = self.individualValue * amountToBuy
            if amountToBuy > self.amount:
                print(f'商人没有那么多{self.name}。')
            elif price > player.money:
                print('钱不够！')
            else:
                itemForPlayer = self.create_item(amountToBuy)
                self.amount -= amountToBuy
                itemForPlayer.add_to_inventory_player(player.inventory)
                player.money -= price
        elif self.amount == 1 and self.individualValue <= player.money:
            itemForPlayer = self.create_item(1)
            itemForPlayer.add_to_inventory_player(player.inventory)
            player.money -= self.individualValue
            self.amount = 0

    def create_item(self, amount):
        '''
        创建一个该物品的副本，并指定自定义的“数量”。
        这是为商店系统添加的功能。

        Parameters:
        amount : int
            创建的物品数量。
        '''
        return Item(self.name, self.description, amount, self.individualValue, self.objectType)

    def add_to_inventory_player(self, inventory):
        '''
        将物品添加到玩家的背包中。

        Parameters:
        inventory : Inventory
            玩家背包。
        '''
        amountAdded = self.amount
        self.add_to_inventory(inventory, amountAdded)
        print(f'{amountAdded}个 \033[33m{self.name}\033[0m 已添加到你的背包！')

    def add_to_inventory(self, inventory, amount):
        '''
        将一定数量的该物品添加到背包中。
        专门为商店系统设计。

        Parameters:
        inventory : Inventory
            物品将被添加到的背包。
        amount : int
            要添加的物品数量
        '''
        alreadyInInventory = False
        for item in inventory.items:
            if self.name == item.name:
                item.amount += amount
                alreadyInInventory = True
                break
        if not alreadyInInventory:
            self.amount = amount
            inventory.items.append(self)

    def show_info(self):
        '''
        显示该特定物品的信息。

        Returns:
        info : str
            包含数量、名称、物品类型和单个价值的字符串。
        '''
        return f'[x{self.amount}] {self.name} ({self.objectType}) - {self.individualValue}G'


class Equipment(Item):
    '''
    玩家可以装备的物品，以提高属性和获得独特的能力（组合技能）。

    Parameters:
    statChangeList : Dictionary
        定义装备此物品后属性变化的字典。
        Example:
        {'hp' : 3,
        'atk' : 2,
        'speed' : -2
        }
        这将使hp增加3，atk增加2，并减少speed 2。
    combo : Combo
        此装备提供的组合技能。
    '''
    def __init__(self, name, description, amount, individual_value, objectType, statChangeList, combo) -> None:
        super().__init__(name, description, amount, individual_value, objectType)
        self.statChangeList = statChangeList
        self.combo = combo
    
    def show_info(self):
        return f'[x{self.amount}] {self.name} ({self.objectType}) [{self.show_stats()}] - {self.individualValue}G'

    def show_stats(self):
        '''
        显示该装备的属性。

        Returns:
        statsString : str
            包含该装备所有属性变化的字符串。
        '''
        statsString = ' '
        for stat in self.statChangeList:
            sign = '+'
            if self.statChangeList[stat] < 0:
                sign = ''
            statsString += f'{stat} {sign}{self.statChangeList[stat]} '
        return statsString
    
    def create_item(self, amount):
        return Equipment(self.name, self.description, amount, self.individualValue, self.objectType, self.statChangeList, self.combo)

class Potion(Item):
    '''
    玩家使用药水恢复MP或HP。

    Attributes:
    stat : str
        要恢复的属性
    amountToChange : int
        恢复的数量
    '''
    def __init__(self, name, description, amount, individual_value, objectType, stat, amountToChange) -> None:
        super().__init__(name, description, amount, individual_value, objectType)
        self.stat = stat
        self.amountToChange = amountToChange

    def activate(self, caster):
        '''
        激活使用该物品的效果。（恢复HP/MP）

        Parameters:
        caster : Player
            需要恢复的玩家。
        '''
        print('{} 使用了一个 {}！'.format(caster.name, self.name))
        if self.stat == 'hp':
            caster.heal(self.amountToChange)
        elif self.stat == 'mp':
            caster.recover_mp(self.amountToChange)
    
    def create_item(self, amount):
        return Potion(self.name, self.description, amount, self.individualValue, self.objectType, self.stat, self.amountToChange)

class Grimoire(Item):
    '''
    法典是玩家可以用来学习新法术的物品。

    Attributes:
    spell : Spell
        玩家将学习的法术。
    '''
    def __init__(self, name, description, amount, individual_value, objectType, spell) -> None:
        super().__init__(name, description, amount, individual_value, objectType)
        self.spell = spell

    def activate(self, caster):
        '''
        激活使用该物品的效果。（学习新法术）

        Parameters:
        caster : Player
            学习法术的玩家。
        '''
        alreadyLearnt = False
        for skill in caster.spells:
            if skill.name == self.spell.name:
                alreadyLearnt = True
                break
        if alreadyLearnt:
            print('你已经会这个法术了。')
        else:
            print(f'使用“{self.name}”，你学会了施放：“{self.spell.name}”！')
            caster.spells.append(self.spell)

    def create_item(self, amount):
        return Grimoire(self.name, self.description, amount, self.individualValue, self.objectType, self.spell)