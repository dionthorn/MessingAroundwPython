'''
Very Simple D20 Based Text RPG
Perma Death
Stats = str,dex,int,con
hp/mp/xp/level/gold/ac
spells not yet implemented
'''

import random

def dice_roll(amt, faces, bonus=0):
    '''
    Takes DnD style input aka 1,20+0 is one twenty sided die with no bonus,
    3,6+2 is three six sided dice with two bonus.

    Returns the value of the dice roll
    '''
    return random.randint(amt, amt*faces) + bonus

def dice_best_of(roll, n):
    '''
    Returns best roll of n rolls
    ex: dice_best_of([3,6],3)
    would return the best roll of
    3, 6 sided dice done 3 times.
    '''
    array = []
    for steps in range(n):
        array.append(dice_roll(roll[0],roll[1]))
        
    return max(array)

def modifier(stat):
    '''
    Fairly accurate to DnD style

    Returns attribute modifier
    '''
    return (stat-10)//2


class PC:
    '''
    The Player Character
    '''
    def __init__(self):
        self.level = 1
        self.xp = 1
        self.str = dice_roll(3,6)
        self.dex = dice_roll(3,6)
        self.int = dice_roll(3,6)
        self.con = dice_roll(3,6)
        self.hp = 10 + dice_roll(1,12,
                            bonus=modifier(self.con))
        self.hp_max = self.hp
        self.mp = 10 + dice_roll(1,12,
                            bonus=modifier(self.int))
        self.gold = dice_roll(1,20)
        self.spells = []
        self.ac = 8 + dice_roll(1,8,bonus=modifier(self.dex))

    def display_stats(self):
        print()
        print(format(' Player Stats  LV: {} '.format(self.level), '#^40'))
        print(format('HP: {}/{}'.format(self.hp,self.hp_max),' >10'),
              format('MP: {}'.format(self.mp),' >8'),
              format('Gold: {}'.format(self.gold),' >8'),
              format('XP: {}'.format(self.xp),' >8'),
              format('AC: {}'.format(self.ac),' >8'),
              format('\nStr: {}\nDex: {}\nCon: {}\nInt: {}'.format(
                  self.str,self.dex,self.con,self.int), ' >25'),
              )
        
    def attack_roll(self):
        return dice_roll(1, 20, bonus=modifier(self.dex))

    def dmg_roll(self):
        dmg = dice_roll(1, 8, bonus=modifier(self.str))
        if dmg <= 0:
            dmg = 1
        return dmg
        
class NPC:
    '''
    The Enemy/NPC
    '''
    def __init__(self, level):
        self.level = level
        self.xp = level * (level - 1) * 500
        if self.xp <= 1:
            self.xp = dice_roll(2,100,bonus=15)
        self.str = dice_roll(3,6)
        self.dex = dice_roll(3,6)
        self.int = dice_roll(3,6)
        self.con = dice_roll(3,6)
        for steps in range(0, level, 4):
            choice = dice_roll(1,4)
            if choice == 1:
                self.str += 1
            elif choice == 2:
                self.dex += 1
            elif choice == 3:
                self.int += 1
            elif choice == 4:
                self.con += 1
        self.hp = 10 + dice_roll(1,8,
                            bonus=modifier(self.con))
        for steps in range(level):
            self.hp += dice_roll(1,8,bonus=modifier(self.con))
        self.hp_max = self.hp
        self.mp = 10 + dice_roll(1,8,
                            bonus=modifier(self.int))
        if self.mp < 1:
            self.mp = 1
        self.gold = dice_roll(level,level*10)
        self.spells = []
        self.ac = 8 + dice_roll(1,8,bonus=modifier(self.dex))

    def display_stats(self):
        print()
        print(format('    Enemy Stats    ', '#^40'))
        print(format('HP: {}/{}'.format(self.hp,self.hp_max),' >10'),
              format('MP: {}'.format(self.mp),' >10'),
              format('Gold: {}'.format(self.gold),' >10'),
              format('XP: {}'.format(self.xp),' >10'),
              format('AC: {}'.format(self.ac),' >10'),
              format('\nStr: {}\nDex: {}\nCon: {}\nInt: {}'.format(
                  self.str,self.dex,self.con,self.int), ' >25'),
              )
        
    def attack_roll(self):
        return dice_roll(1, 20, bonus=modifier(self.dex))

    def dmg_roll(self):
        dmg = dice_roll(1, 8, bonus=modifier(self.str))
        if dmg <= 0:
            dmg = 1
        return dmg

player = PC()
enemy = NPC(1)
game = True

def fight(level, player):
    enemy = NPC(level)
    while player.hp > 0:
        if dice_roll(1, 20, bonus=player.dex) >= dice_roll(1, 20, bonus=enemy.dex):
            if player.attack_roll() > enemy.ac:
                dmg = player.dmg_roll()
                enemy.hp -= dmg
                print('    Player Hit! for {} damage.'.format(dmg))
            else:
                print('  Player Missed!')
        else:
            if enemy.attack_roll() > player.ac:
                dmg = enemy.dmg_roll()
                player.hp -= dmg
                print('    Enemy Hit! for {} damage.'.format(dmg))
            else:
                print('  Enemy Missed!')
        if enemy.hp <= 0:
            player.gold += enemy.gold
            if enemy.xp <= 0:
                player.xp += 1
            else:
                player.xp += (enemy.xp//10)+(enemy.level*10)
            print(format('    Enemy Died    ', '#^40'))
            print('Your Current HP: {}/{} MP: {} XP:{} Gold:{}'.format(player.hp,
                                                               player.hp_max,
                                                               player.mp,
                                                               player.xp,
                                                               player.gold))             
            return True
    else:
        print(format('#', '#^40'))
        print(format('    You have Died.    ', '#^40'))
        print(format('    A New Player Has Been Made    ', '#^40'))
        print(format('#', '#^40'))
        return False

player.display_stats()
while game:
    choice = input('\nPlease input a command or help:\n').lower()
    if choice == 'stats':
        player.display_stats()
    elif choice == 'fight':
        try:
            whowon = fight(int(input('Enter a Level of Enemy to Fight:\n')), player)
        except:
            whowon = True
            print(format('!!!Invalid Input!!!',' ^40'))
        if whowon == False:
            player = PC()
            player.display_stats()
        else:
            temp = player.level + 1
            needxp = temp * (temp - 1) * 500
            if player.xp >= needxp:
                print(' !LEVEL UP! ')
                player.hp += dice_roll(1,4,bonus=modifier(player.con))
                player.level += 1
                player.display_stats()
    elif choice == 'goto':
        choice = input('Where would you like to go?\n').lower()
        if choice == 'inn':
            cost = dice_roll(1,20)
            print('Cost: {}'.format(cost))
            if player.gold >= cost:
                player.gold -= cost
                player.hp = player.hp_max
                print('  You Stayed the Night  ')
            else:
                print('  You Could Not Afford It  ')
        else:
            pass
    elif choice == 'new':
        choice = int(input('Set Minimum Score'))
        generations = 0
        player = PC()
        while True:
            if player.str < choice:
                player = PC()
            elif player.int < choice:
                player = PC()
            elif player.dex < choice:
                player = PC()
            elif player.con < choice:
                player = PC()
            else:
                break
            generations += 1
        print('Took {} Generations to Reach that minimum'.format(generations))
        player.display_stats()
    elif choice == 'help':
        print('Avaliable Commands Are:')
        print('  stats')
        print('  fight')
        print('  goto')
        print('    inn')
        print('  new')
        print('  quit')
    elif choice == 'debug':
        try:
            exec(input('DEBUG CONTROL: '))
        except:
            print(format('!!!DEBUG ERROR!!!', ' ^40'))
    elif choice == 'quit':
        game = False
