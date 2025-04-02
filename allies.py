import combat
# 导入战斗以继承战者的数据

'''
盟友在战斗中帮助玩家。目前，这里详述的所有盟友都是通过法术召唤的，
但也可以在此处定义由事件或任何其他原因授予的盟友。
主要有他们的统计数据。
'''

class SummonedSkeleton(combat.Battler):
    def __init__(self) -> None:
        stats = {'maxHp': 15,
                    'hp': 15,
                    'maxMp': 10,
                    'mp': 10,
                    'atk': 5,
                    'def': 3,
                    'matk': 1,
                    'mdef': 2,
                    'speed': 7,
                    'critCh': 5
        }
        super().__init__('小骨', stats)
        self.isAlly = True

class SummonedFireSpirit(combat.Battler):
    def __init__(self) -> None:
        stats = {'maxHp': 20,
                    'hp': 20,
                    'maxMp': 10,
                    'mp': 10,
                    'atk': 12,
                    'def': 3,
                    'matk': 4,
                    'mdef': 5,
                    'speed': 9,
                    'critCh': 5
        }
        super().__init__('火精灵', stats)
        self.isAlly = True