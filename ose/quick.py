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
  torches = str(diceRoll(1,6))
  rations = str(diceRoll(1,6))

  gear = [ ]

  advGearList = [ 
    'Crowbar', 'Hammer, 12 spikes', 'Holy Water', 'Lantern, 3 oil flasks', 'Mirror (small) ', 'Pole 10\'',
    'Rope 50\'', 'Rope 50\', Grappling Hook', 'Sack (large)', 'Sack (small)', 'Stakes (3), mallet', 'Wolfsbane (1 bunch)'
    ]

  firstItem = advGearList[diceRoll(1,12) - 1]
  secondItem = advGearList[diceRoll(1,12) - 1]
  while secondItem == firstItem:
    secondItem = advGearList[diceRoll(1,12) - 1]
  gear.append(firstItem)
  gear.append(secondItem)
  items = ''
  for item in sorted(gear):
    items = items + ', ' + item
  gear = items[1:]
#  gear = gear + str(' ' * (46 - len(gear))) + '|'

  # armor
  if charClass == 'Magic User':
    armor = 'none'
  elif charClass == 'Thief':
    armor = 'Leather'
  else:
    armor = [ 'Leather', 'Leather, Shield', 'Chain', 'Chain, Shield', 'Plate', 'Plate, Shield' ]
    armor = armor[diceRoll(1,6) - 1] 
#  armor = armor + str(' ' * (11 - len(armor)))

  ac = { 'none' : 9, 'Leather' : 7, 'Leather, Shield' : 6, 'Chain' : 5, 'Chain, Shield' : 4, 'Plate' : 3, 'Plate, Shield' : 2 }
  ac = ac[armor.strip()]
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
    weapon = weapon + ', ' + secondWeapon
  else:
    weapons = [ 
      'Battle axe', 'Crossbow + 20 bolts', 'Hand axe', 'Mace', 'Pole arm', 'Short bow + 20 arrows', 
      'Short sword', 'Silver dagger', 'Sling + 20 stones', 'Spear', 'Sword', 'War hammer' 
      ]
    rangeWeapons = [ 'Crossbow + 20 bolts', 'Short bow + 20 arrows', 'Sling + 20 stones' ]
    meleeWeapons = [ 'Battle axe', 'Hand axe', 'Mace', 'Pole arm', 'Short sword', 'Silver dagger','Spear', 'Sword', 'War hammer']
    weapon = weapons[diceRoll(1,12) - 1]
    secondWeapon = weapons[diceRoll(1,12) - 1]
    while secondWeapon == weapon:
      secondWeapon = weapons[diceRoll(1,12) - 1]
    if weapon in rangeWeapons and secondWeapon in rangeWeapons:
      secondWeapon = meleeWeapons[diceRoll(1,9) - 1]
    weapon = weapon + ', ' + secondWeapon

  gold = diceRoll(3,6)

  return ac, armor, weapon, gear, torches, rations, gold

abilities = ['STR', 'INT','WIS','DEX','CON','CHA']
classes = ['Fighter', 'Magic User', 'Cleric', 'Thief']
party = []
totalGold = 0


for a in abilities:
  print(a + ' ',end='')

print('| Class      | HP | AC | Equipment                                                  | T | R | G |')
print('------------------------|------------|----|----|------------------------------------------------------------|---|---|---|')

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

  if len(possibleClasses) > 1:
    # keep the party to unique classes only
    charClass = random.choice(possibleClasses)
    # print(charClass, party)
    if charClass in party:
      possibleClasses.remove(charClass)
      if len(party) > 1 :
        charClass = random.choice(possibleClasses)
      else:
        charClass = possibleClasses[0]
    party.append(charClass)
  else:
    charClass = possibleClasses[0]

  if charClass in [ 'Fighter', 'Dwarf']:
    hp = diceRoll(1,8)
  elif charClass in [ 'Cleric', 'Elf', 'Halfling' ]:
    hp = diceRoll(1,6)
  elif charClass in [ 'Magic User', 'Thief']:
    hp = diceRoll(1,4)

  ac, armor, weapon, gear, torches, rations, gold = rollEquip(charClass, stats[3])
  totalGold += gold

  # print sheet
  for roll in stats:
    if roll < 10:
      roll = '  ' + str(roll)
    else:
      roll = ' ' + str(roll)
    print(roll + ' ', end='')
  ws = ' ' * (10 - len(charClass))
  gearString = 'A: ' + armor + '  W: ' + weapon
  gearString = gearString + (' ' * (58 - len(gearString)))
  gearString2 =  '                        |            |    |    ' +'| E:'+ gear
  gearString2 = gearString2 + (' ' * (108 - len(gearString2))) + '|   |   |   |'
  gold = (' ' * (2 - len(str(gold)))) + str(gold)
  print('| ' + charClass + ws + ' |  ' + str(hp) + ' |  ' + str(ac) + ' | ' + gearString + ' | ' + torches + ' | '  + rations + ' | ' + str(gold)  + '|' )
  print(gearString2)
  print()
print('...Everyone has a Backpack, tinderbox, and waterskin. T = Torches, R = Rations G = Gold')
print('...Total Party Gold:',str(totalGold))
quit()
