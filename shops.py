import inventory
import random

class Shop():
    '''
    处理商店管理。

    Attributes:
    itemSet: List
        商店可以拥有的物品池。
    inventory: Inventory
        商店的库存
    '''
    def __init__(self, itemSet) -> None:
        self.itemSet = itemSet
        self.inventory = inventory.Inventory()
        self.add_items_to_inventory_shop()

    def add_items_to_inventory_shop(self):
        '''
        将新物品添加到商店的库存中。
        '''
        itemQuantity = random.randint(len(self.itemSet)//2, len(self.itemSet))
        for _ in range(itemQuantity):
            random.choice(self.itemSet).add_to_inventory(self.inventory, 1)