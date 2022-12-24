import random as rand

from game import Game
from player import Player

FIGHTS_PER_LEVEL = 10
PLAYER_LEVELS = 10

def Attack_Melee(player, c_obj):
    damage = player.StatMod(player.STR)
    roll = rand.randint(0, 20)
    # print("p roll", roll)
    if roll == 20:
        if player.MAIN_HAND != "":
            damage += player.MAIN_HAND.MeleeDmg() + player.MAIN_HAND.MeleeDmg()
        if player.ALT_HAND != "":
            damage += player.ALT_HAND.MeleeDmg() + player.ALT_HAND.MeleeDmg()
        return damage
    else:
        roll += player.StatMod(player.STR)
        if player.MAIN_HAND != "":
            damage += player.MAIN_HAND.MeleeDmg()
            roll += player.MAIN_HAND.MainToHit_Bonus
        if player.ALT_HAND != "":
            damage += player.ALT_HAND.MeleeDmg()
            roll += player.ALT_HAND.AltToHit_Bonus
        if roll >= c_obj.AC:
            return damage
        else:
            return 0

def monsterAttack(monster):
    roll = rand.randint(0, 20)
    # print("m roll", roll)
    damage = monster.getDmg_Melee()
    if roll == 20:
        damage += monster.getDmg_Melee()
        return roll, damage, True
    roll += monster.HitBonus
    return roll, damage, False

def playerTakeDmg(p, roll, dmg):
    current_ac = p.AC
    weight = p.InventoryWeight()
    if p.ARMOR != "":
        current_ac += p.ARMOR.ArmorClass
        weight += p.ARMOR.WEIGHT
    if p.MAIN_HAND != "":
        current_ac += p.MAIN_HAND.ArmorClass
        weight += p.MAIN_HAND.WEIGHT
    if p.ALT_HAND != "":
        current_ac += p.ALT_HAND.ArmorClass
        weight += p.ALT_HAND.WEIGHT
    
    dodge = p.StatMod(p.DEX)
    if weight >= 100 and weight < 200:
        dodge -= 1
    elif weight >= 200 and weight < 250:
        dodge -= 2
    elif weight >= 250 and weight < 300:
        dodge -= 3
    elif weight >= 300:
        dodge -= 5

    if roll >= current_ac + dodge:
        return dmg
    else:
        return 0

def fight(p, m):
    total_dmg_taken = 0
    total_dmg_dealt = 0
    while True:
        damage_dealt = Attack_Melee(p, m)
        # print("dmg dealt", damage_dealt)
        m.HEALTH -= damage_dealt
        total_dmg_dealt += damage_dealt
        roll, m_dmg, crit = monsterAttack(m)
        if crit:
            player.CURR_HEALTH -= m_dmg
            total_dmg_taken += m_dmg
            # print("damage taken", m_dmg)
        else:
            dmg_taken = playerTakeDmg(p, roll, m_dmg)
            player.CURR_HEALTH -= dmg_taken
            # print("damage taken", dmg_taken)
            total_dmg_taken += dmg_taken
        if player.HEALTH <= 0:
            return False, total_dmg_taken, total_dmg_dealt
        if m.HEALTH <= 0:
            return True, total_dmg_taken, total_dmg_dealt
        

game = Game()

player = Player(game)
player.MAIN_HAND = ""
player.ALT_HAND = ""
player.ARMOR = ""

all_armor = game.ALL_ARMOR
all_armor.insert(0, "")
all_weapons = game.ALL_WEAPONS
all_weapons.insert(0, "")
all_monsters = game.ALL_MONSTERS
stats = []
for m in range(len(all_monsters)):
    row = []
    for level in range(10):
        row.append(0)
    stats.append(row)
builds = []

for armor in all_armor:
    player.ARMOR = armor
    for weapon in all_weapons:
        player.MAIN_HAND = weapon
        for a_weapon in all_weapons:
            player.ALT_HAND = a_weapon
            build = []
            print("=PLAYER=")
            print("  Armor: ", end="")
            if player.ARMOR != "":
                print(player.ARMOR.name)
                build.append([player.ARMOR.name])
            else:
                print("")
                build.append([])
            print("  Main Hand: ", end="")
            if player.MAIN_HAND != "":
                print(player.MAIN_HAND.name)
                build.append([player.MAIN_HAND.name])
            else:
                print("")
                build.append([])
            print("  Alt Hand: ", end="")
            if player.ALT_HAND != "":
                print(player.ALT_HAND.name)
                build.append([player.ALT_HAND.name])
            else:
                print("\n")
                build.append([])

            
            
            builds.append(build)

                
                

print("\n\n==Script Finished==")
print(builds)