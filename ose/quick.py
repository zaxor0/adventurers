#!/usr/bin/python3

import random
import sys

# ARGUMENTS
try:
  charCount = int(sys.argv[1])
except:
  print('missing number of characters')
  quit()

# VARIABLES
party = []
totalGold = 0
abilities = ['STR', 'INT','WIS','DEX','CON','CHA']
classes = {'Fighter' : 8,  'Dwarf' : 8, 'Cleric': 6, 'Elf': 6, 'Halfling': 6, 'Magic User': 4, 'Thief':4 }
advGearList = [ 
  'Crowbar', 'Hammer, 12 spikes', 'Holy Water', 'Lantern, 3 oil flasks', 'Mirror (small) ', 'Pole 10\'',
  'Rope 50\'', 'Rope 50\', Grappling Hook', 'Sack (large)', 'Sack (small)', 'Stakes (3), mallet', 'Wolfsbane (1 bunch)'
  ]
armorDict = { 'None' : 9, 'Leather' : 7, 'Leather, Shield' : 6, 'Chain' : 5, 'Chain, Shield' : 4, 'Plate' : 3, 'Plate, Shield' : 2 }
weapons = [ 'Battle axe', 'Crossbow + 20 bolts', 'Hand axe', 'Mace', 'Pole arm', 'Short bow + 20 arrows', 'Short sword', 'Silver dagger', 'Sling + 20 stones', 'Spear', 'Sword', 'War hammer' ]
meleeWeapons = [ 'Battle axe', 'Hand axe', 'Mace', 'Pole arm', 'Short sword', 'Silver dagger','Spear', 'Sword', 'War hammer']
clericWeapons = [ 'Mace', 'Sling + 20 stones', 'Staff', 'War hammer' ]
dexMod = { 0 : -3, 4 : -2, 6 : -1, 9 : 0, 13 : 1, 16 : 2, 18 : 3}

# FUNCTIONS
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

  gear = []

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

  # armor
  if charClass == 'Magic User':
    armor = 'None'
  elif charClass == 'Thief':
    armor = 'Leather'
  else:
    armor = [*armorDict] # unpack dict keys (armor by name) into an array
    armor = armor[diceRoll(1,6) - 1] 

  ac = armorDict[armor]
  for score in dexMod:
    if score <= dex:
      mod = dexMod[score]

  ## weapon selection
  # magic users only get daggers
  if charClass == 'Magic User':
    weapon = 'Dagger'

  # clerics only get blunt weapons
  if charClass == 'Cleric':
    weapon = clericWeapons[diceRoll(1,4) - 1]
    secondWeapon = clericWeapons[diceRoll(1,4) - 1]
    while secondWeapon == weapon:
      secondWeapon = clericWeapons[diceRoll(1,4) - 1]
    weapon = weapon + ', ' + secondWeapon

  # everyone else get 1 melee and 1 second weapon
  weapon = meleeWeapons[diceRoll(1,9) - 1]
  secondWeapon = weapons[diceRoll(1,12) - 1]
  weapon = weapon + ', ' + secondWeapon
  
  # everyon gets 3d6 of gold
  gold = diceRoll(3,6)

  # return all equipment
  return ac, armor, weapon, gear, torches, rations, gold

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
    arrayClasses = [*classes]
    possibleClasses.append(arrayClasses[highPos])
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

  hd = classes[charClass]
  hp = diceRoll(1,hd)

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
