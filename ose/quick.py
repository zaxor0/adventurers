#!/usr/bin/python3

import random
import sys

try:
  charCount = int(sys.argv[1])
except:
  print('missing number of characters')
  quit()

def diceRoll(dieCount,dieSides):
  dieTotal = 0
  for i in range(0,dieCount):
    min = 1
    max = dieSides
    dieVal = random.randint(min,max)
    dieTotal += dieVal
  return(dieTotal)

def rollEquip(charClass, dex):
  # basic gear
  torches = str(diceRoll(1,6)) + ' torches' 
  rations = str(diceRoll(1,6)) + ' ration' 
  gear = [ 'Backpack', 'tinderbox', 'waterskin', torches, rations ]
  # armor
  if charClass == 'Magic User':
    armor = 'none'
  elif charClass == 'Thief':
    armor = 'leather'
  else:
    armor = [ 'leather', 'leather + S', 'chainmail', 'chainmail + S', 'platemail', 'platemail + S' ]
    armor = armor[diceRoll(1,6) - 1] 
  armor = armor + str(' ' * (13 - len(armor)))

  ac = { 'leather' : 7, 'leather + S' : 6, 'chainmail' : 5, 'chainmail + S' : 4, 'platemail' : 3, 'platemail + S' : 2 }
  ac = ac[armor]
  dexMod = { 3 : -3, 5 : -2, 8 : -1, 12 : 0, 15 : 1, 17 : 2, 18 : 3}
  for dex in dexMod:
    mod = dexMod[dex]

  # weapon
  if charClass == 'Magic User':
    weapon = 'Dagger'
  elif charClass == 'Cleric':
    weapons = [ 'Mace', 'Sling + 20 stones', 'Staff', 'War hammer' ]
    weapon = weapons[diceRoll(1,4) - 1]
    secondWeapon = weapons[diceRoll(1,4) - 1]
    while secondWeapon == weapon:
      secondWeapon = weapons[diceRoll(1,4) - 1]
    weapon = weapon + ' , ' + secondWeapon
  else:
    weapons = [ 
      'Battle axe', 'Crossbow + 20 bolts', 'Hand axe', 'Mace', 'Pole arm', 'Short bow + 20 arrows', 
      'Short sword', 'Silver dagger', 'Sling + 20 stones', 'Spear', 'Sword', 'War hammer' 
      ]
    weapon = weapons[diceRoll(1,12) - 1]
    secondWeapon = weapons[diceRoll(1,12) - 1]
    while secondWeapon == weapon:
      secondWeapon = weapons[diceRoll(1,12) - 1]
    weapon = weapon + ' , ' + secondWeapon
  return ac, armor, weapon, gear

abilities = ['STR', 'INT','WIS','DEX','CON','CHA']
classes = ['Fighter', 'Magic User', 'Cleric', 'Thief']
party = []


for a in abilities:
  print(a + ' ',end='')
print(' | Class      | HP | Armor         | Weapon                |')
print('-------------------------|------------|----|---------------|----------------------')

for i in range(charCount):
  stats = []
  highPos = 0
  for j in range(0,6):
    roll = diceRoll(3,6)
    stats.append(roll)
    if stats[j] > stats[highPos]:
      highPos = j

  # generate array of possible classes for this character
  possibleClasses = []
  # if str, int, wis, or dex is the highest, default to the appropriate class
  if highPos < 4:
    possibleClasses.append(classes[highPos])
  # if not the highest, of the first 4 stats, add the most appropriate to the class possibilities
  elif stats[0] > stats[1] and stats[0] > 2 and stats[0] > 3:
    possibleClasses.append('Fighter')
  elif stats[1] > stats[0] and stats[1] > 2 and stats[0] > 3:
    possibleClasses.append('Magic User')
  elif stats[2] > stats[0] and stats[2] > 1 and stats[0] > 3:
    possibleClasses.append('Cleric')
  elif stats[3] > stats[0] and stats[3] > 1 and stats[3] > 2:
    possibleClasses.append('Thief')
  else:
    possibleClasses.append('Fighter')
  # classes with min. req.
  if stats[4] >= 9:
    possibleClasses.append('Dwarf')
  if stats[1] >= 9:
    possibleClasses.append('Elf')
  if stats[4] >= 9 and stats[3] >= 9:
    possibleClasses.append('Halfling')

  # keep the party to unique classes only
  charClass = random.choice(possibleClasses)
#  print(charClass, party)
  if charClass in party:
    possibleClasses.remove(charClass)
    if len(party) > 1 :
      charClass = random.choice(possibleClasses)
    else:
      charClass = possibleClasses[0]
  party.append(charClass)

  if charClass in [ 'Fighter', 'Dwarf']:
    hp = diceRoll(1,8)
  elif charClass in [ 'Cleric', 'Elf', 'Halfling' ]:
    hp = diceRoll(1,6)
  elif charClass in [ 'Magic User', 'Thief']:
    hp = diceRoll(1,4)

  armor, weapon, gear = rollEquip(charClass, stats[3])

  # print sheet
  for roll in stats:
    if roll < 10:
      roll = '  ' + str(roll)
    else:
      roll = ' ' + str(roll)
    print(roll + ' ', end='')
  ws = ' ' * (10 - len(charClass))
  print(' | ' + charClass + str(ws) + ' |  ' + str(hp) + ' | ' + armor + ' | ' + weapon )
#  print(str(' ' * 40) + str(gear))
quit()
