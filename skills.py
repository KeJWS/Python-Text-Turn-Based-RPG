import allies

class Skill():
    '''
    Skill 是法术（Spells）和连招（Combos）的父类。

    Attributes:
    name : str
        技能名称。
    description : str
        技能描述。
    cost : int
        技能消耗的 MP 或 CP。
    isTargeted : bool
        如果需要选择目标则为 True，否则为 False。
    defaultTarget : str
        如果技能没有目标时的默认目标。
    '''
    def __init__(self, name, description, cost, isTargeted, defaultTarget) -> None:
        self.name = name
        self.description = description
        self.cost = cost
        self.isTargeted = isTargeted
        self.defaultTarget = defaultTarget

    def check_already_has_buff(self, target):
        '''
        检查目标单位是否已经有来自此技能的增益效果。
        技能名称必须与增益效果的名称相同。

        Parameters:
        target : Battler
            要检查的目标单位。

        Returns:
        True/False : bool
            如果目标单位已经拥有该增益效果，返回 True；否则返回 False。
        '''
        for bd in target.buffsAndDebuffs:
            if bd.name == self.name:
                print(f'{target.name} 的 {self.name} 持续时间已重置')
                bd.restart()
                return True
        return False

class Spell(Skill):
    '''
    法术消耗 MP（魔法值），MP 可以通过升级、使用道具、事件等恢复。它们也会随着提升 WIS（智慧）能力或装备某些物品而增加。
    法术使用 MATK（魔法攻击力）和自身的力量来计算伤害。继承自 Skill 类。

    Attributes:
    power : int
        法术的伤害值。
    '''
    def __init__(self, name, description, power, cost, isTargeted, defaultTarget) -> None:
        super().__init__(name, description, cost, isTargeted, defaultTarget)
        self.power = power

    def check_mp(self, caster):
        '''
        检查施法者是否有足够的 MP 来施放此法术。

        Parameters:
        caster : Battler
            施放法术的单位。

        返回：
        True/False : bool
            如果法术成功施放，返回 True；否则返回 False。
        '''
        if caster.stats['mp'] < self.cost:
            print('MP 不足！')
            return False
        else:
            print(f'{caster.name} 施放了 {self.name}！')
            caster.stats['mp'] -= self.cost
            return True

class Combo(Skill):
    '''
    连招消耗 CP（连招点），每次战斗开始时，CP 默认为 0，并且随着战斗单位进行普通攻击而增加。
    使用某些技能也可以增加 CP。连招通常具有特殊效果，并且结合了普通攻击。继承自 Skill 类。
    '''
    def __init__(self, name, description, cost, isTargeted, defaultTarget) -> None:
        super().__init__(name, description, cost, isTargeted, defaultTarget)
    
    def check_cp(self, caster):
        '''
        检查施放者是否有足够的 CP 来执行连招。

        Parameters:
        caster : Battler
            执行连招的单位。

        返回：
        True/False : bool
            如果连招成功执行，返回 True；否则返回 False。
        '''
        if caster.comboPoints < self.cost:
            print('连招点不足！')
            return False
        else:
            print(f'{caster.name} 使用了 {self.name}！')
            caster.comboPoints -= self.cost
            return True

##### 法术类 #####

class DamageSpell(Spell):
    '''
    标准的伤害法术类，继承自 Spell。
    '''
    def __init__(self, name, description, power, mpCost, isTargeted, defaultTarget) -> None:
        super().__init__(name, description, power, mpCost, isTargeted, defaultTarget)

    # TODO: 修改目标，使其始终为列表。
    def effect(self, caster, target):
        '''
        根据法术的威力对目标造成伤害。

        Parameters:
        caster : Battler
            施法者。
        target : Battler/List
            法术的目标。
        '''
        if self.check_mp(caster):
            if self.isTargeted:
                dmg = self.power + (caster.stats['matk'] - target.stats['mdef'])
                target.take_dmg(dmg)
            else:
                if self.defaultTarget == 'all_enemies':
                    for enemy in target:
                        dmg = self.power + (caster.stats['matk'] - enemy.stats['mdef'])
                        enemy.take_dmg(dmg)

class RecoverySpell(Spell):
    '''
    标准的恢复法术类，继承自 Spell。

    Attributes:
    stat : str
        要恢复的属性（mp/hp）
    '''
    def __init__(self, name, description, power, mpCost, stat, isTargeted, defaultTarget) -> None:
        super().__init__(name, description, power, mpCost, isTargeted, defaultTarget)
        self.stat = stat
    
    def effect(self, caster, target):
        '''
        恢复目标的某项属性。

        Parameters:
        caster : Battler
            施法者。
        target : Battler/List
            法术的目标。
        '''
        amountToRecover = 0
        if self.check_mp(caster):
            amountToRecover = self.power + round(caster.stats['matk']/2)
        if self.stat == 'hp':
            target.heal(amountToRecover)
        elif self.stat == 'mp':
            target.recover_mp(amountToRecover)

class BuffDebuffSpell(Spell):
    '''
    标准的增益/减益法术，继承自 Spell。

    Attributes:
    statToChange : str
        要增益或减益的属性。
    amountToChange : float
        属性改变的百分比（范围 0 到 1）。
    turns : int
        增益或减益效果持续的回合数。
    '''
    def __init__(self, name, description, power, mpCost, isTargeted, defaultTarget, statToChange, amountToChange, turns) -> None:
        super().__init__(name, description, power, mpCost, isTargeted, defaultTarget)
        self.statToChange = statToChange
        self.amountToChange = amountToChange
        self.turns = turns

    def effect(self, caster, target):
        '''
        对目标施加增益或减益效果。
        
        Parameters:
        caster : Battler
            施法者。
        target : Battler/List
            法术的目标。
        '''
        if self.check_mp(caster) and not self.check_already_has_buff(target):
            buff = BuffDebuff(self.name, target, self.statToChange, self.amountToChange, self.turns)
            buff.activate()

class SummonSpell(Spell):
    '''
    标准召唤法术，召唤特定的盟友。

    Attributes:
    summoning : Battler
        召唤出的战斗者。
    '''
    def __init__(self, name, description, power, cost, isTargeted, defaultTarget, summoning) -> None:
        super().__init__(name, description, power, cost, isTargeted, defaultTarget)
        self.summoning = summoning

    def effect(self, caster, allies):
        '''
        召唤战斗者加入战斗。

        Parameters:
        caster : Battler
            施放法术的角色。
        target : Battler/List
            施法的目标。
        '''
        if self.check_mp(caster):
            summoningInst = self.summoning()
            allies.append(summoningInst)
            print(f'你召唤出了 {summoningInst.name}')

##### 连击技能 #####

class SlashCombo(Combo):
    '''
    标准斩击连击（执行 X 次普通攻击）。继承自 Combo。

    Attributes:
    timesToHit : int
        普通攻击的次数。
    '''
    def __init__(self, name, description, comboCost, isTargeted, defaultTarget, timesToHit) -> None:
        super().__init__(name, description, comboCost, isTargeted, defaultTarget)
        self.timesToHit = timesToHit

    def effect(self, caster, target):
        '''
        施术者对目标发动 X 次普通攻击。

        Parameters:
        caster : Battler
            施放连击的角色。
        target : Battler/List
            目标角色。
        '''
        if self.check_cp(caster):
            print(f'{caster.name} 对 {target.name} 发动 {self.timesToHit} 次攻击！')
            for _ in range(self.timesToHit):
                caster.normal_attack(target)

class ArmorBreakingCombo(Combo):
    '''
    标准护甲削弱连击。继承自 Combo。

    Attributes:
    armorDestroyed : float
        护甲削弱百分比（范围 -1 到 1，作为削弱效果应在 -1 < armorDestroyed < 0）。
    '''
    def __init__(self, name, description, cost, isTargeted, defaultTarget, armorDestroyed) -> None:
        super().__init__(name, description, cost, isTargeted, defaultTarget)
        self.armorDestroyed = armorDestroyed
    
    def effect(self, caster, target):
        '''
        施术者发动普通攻击并削弱目标的护甲。

        Parameters:
        caster : Battler
            施放连击的角色。
        target : Battler/List
            目标角色。
        '''
        if self.check_cp(caster):
            print(f'{caster.name} 撕裂了 {target.name} 的护甲！')
            if not self.check_already_has_buff(target):
                armorBreak = BuffDebuff('护甲破坏', target, 'def', self.armorDestroyed, 4)
                armorBreak.activate()
                caster.normal_attack(target)

class VampirismCombo(Combo):
    '''
    标准生命吸取连击。继承自 Combo。

    Attributes:
    percentHeal : float
        根据造成的伤害恢复生命值的百分比（范围 0 到 1）。
    '''
    def __init__(self, name, description, cost, isTargeted, defaultTarget, percentHeal) -> None:
        super().__init__(name, description, cost, isTargeted, defaultTarget)
        self.percentHeal = percentHeal

    def effect(self, caster, target):
        '''
        施术者发动普通攻击，并根据造成的伤害恢复生命值。

        Parameters:
        caster : Battler
            施放连击的角色。
        target : Battler/List
            目标角色。
        '''
        if self.check_cp(caster):
            amountToRecover = caster.normal_attack(target) * self.percentHeal
            caster.heal(round(amountToRecover))

class RecoveryCombo(Combo):
    '''
    标准恢复类连击。继承自 Combo。

    Attributes:
    stat : str
        恢复的属性（mp/hp）。
    '''
    def __init__(self, name, description, cost, stat, amountToChange, isTargeted, defaultTarget) -> None:
        super().__init__(name, description, cost, isTargeted, defaultTarget)
        self.stat = stat
        self.amountToChange = amountToChange
    
    def effect(self, caster, target):
        '''
        恢复目标的某项属性值。

        Parameters:
        caster : Battler
            施放连击的角色。
        target : Battler/List
            目标角色。
        '''
        if self.check_cp(caster):
            if self.stat == 'hp':
                target.heal(self.amountToChange)
            elif self.stat == 'mp':
                target.recover_mp(self.amountToChange)

##### 增益与减益状态 #####

class BuffDebuff():
    '''
    处理某项属性的增益和减益效果的类。

    Attributes:
    name : str
        增益/减益的名称（应与触发它的技能名称相同）。
    target : Battler
        受到增益/减益影响的战斗者。
    statToChange : str
        受到影响的属性。
    amountToChange : float
        属性变动的百分比（范围 -1 到 1）。
    turns : int
        剩余的回合数。
    maxTurns : int
        增益/减益的最大持续回合数（默认时长）。
    '''
    def __init__(self, name, target, statToChange, amountToChange, turns) -> None:
        self.name = name
        self.target = target
        self.statToChange = statToChange
        self.amountToChange = amountToChange
        self.turns = turns
        self.maxTurns = turns

    def activate(self):
        '''
        激活增益/减益效果。
        '''
        self.target.buffsAndDebuffs.append(self)
        if self.amountToChange < 0:
            print(f'{self.target.name} 的 {self.statToChange} 被削弱了 {self.amountToChange * 100}%，持续 {self.turns} 回合')
        else:
            print(f'{self.target.name} 的 {self.statToChange} 提升了 {self.amountToChange * 100}%，持续 {self.turns} 回合')
        self.difference = int(self.target.stats[self.statToChange] * self.amountToChange)
        self.target.stats[self.statToChange] += self.difference

    def restart(self):
        '''
        重置该增益/减益的持续回合数。
        '''
        self.turns = self.maxTurns

    def check_turns(self):
        '''
        每回合减少 1 点持续时间，并检查是否应该移除该效果。
        '''
        self.turns -= 1
        if self.turns <= 0:
            self.deactivate()

    def deactivate(self):
        '''
        移除增益/减益效果。
        '''
        print(f'{self.name} 的效果已结束')
        self.target.buffsAndDebuffs.remove(self)
        self.target.stats[self.statToChange] -= self.difference

##### 法术与连击技能实例 #####

spellFireball = DamageSpell('火球术', '', 15, 3, True, None)
spellDivineBlessing = RecoverySpell('神圣祝福', '', 8, 4, 'hp', True, None)
spellEnhanceWeapon = BuffDebuffSpell('强化武器', '', 0, 5, False, 'self', 'atk', 0.5, 3)
spellInferno = DamageSpell('烈焰风暴', '', 14, 7, False, 'all_enemies')
spellSkeletonSummoning = SummonSpell('召唤骷髅', '', 0, 4, False, 'allies', allies.SummonedSkeleton)
spellFireSpiritSummonning = SummonSpell('召唤火焰精灵', '', 0, 12, False, 'allies', allies.SummonedFireSpirit)

comboSlash1 = SlashCombo('斩击连击 I', '', 3, True, None, 3)
comboSlash2 = SlashCombo('斩击连击 II', '', 3, True, None, 4)
comboArmorBreaker1 = ArmorBreakingCombo('破甲斩 I', '', 2, True, None, -0.3)
comboVampireStab1 = VampirismCombo('吸血刺击 I', '', 2, True, None, 0.3)
comboVampireStab2 = VampirismCombo('吸血刺击 II', '', 2, True, None, 0.5)
comboMeditation1 = RecoveryCombo('冥想 I', '', 1, 'mp', 5, False, 'self')
comboMeditation2 = RecoveryCombo('冥想 II', '', 2, 'mp', 15, False, 'self')

quickSshooting = SlashCombo('快速连射 I', '', 1, True, None, 2)
quickSshooting2 = SlashCombo('快速连射 II', '', 2, True, None, 3)