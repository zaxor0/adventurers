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
partyClasses = []
totalGold = 0
abilities = ['STR', 'INT','WIS','DEX','CON','CHA']
classes = {
  'Fighter' : { 'hd' :  8, 'saves' : [12, 13, 14, 15, 16] },  'Dwarf' : { 'hd':  8 , 'saves' : [8, 9, 10, 13, 12] },
  'Cleric': { 'hd' : 6 , 'saves' : [11, 12, 14, 16, 15] },  'Elf': { 'hd' : 6, 'saves' : [12, 13, 13, 15, 15] } , 
  'Halfling': { 'hd' : 6 , 'saves' : [8, 9, 10, 13, 12] }, 'Magic User': { 'hd' : 4, 'saves' : [13, 14, 13, 16, 15] }, 
  'Thief': { 'hd' : 4 , 'saves' : [13, 14, 13, 16, 15] } 
  }
advGearList = [ 
  'Crowbar', 'Hammer +12 spikes', 'Holy Water', 'Lantern +3 oil flasks', 'Mirror (small metal)', 'Pole 10\'',
  'Rope 50\'', 'Rope 50\' +Grappling Hook', 'Sack (large)', 'Sack (small)', 'Stakes (3) +Mallet', 'Wolfsbane (1 bunch)'
  ]
armorDict = { 'None' : 9, 'Leather' : 7, 'Leather, Shield' : 6, 'Chain' : 5, 'Chain, Shield' : 4, 'Plate' : 3, 'Plate, Shield' : 2 }
weapons = [ 'Battle axe', 'Crossbow + 20 bolts', 'Hand axe', 'Mace', 'Pole arm', 'Short bow + 20 arrows', 'Short sword', 'Silver dagger', 'Sling + 20 stones', 'Spear', 'Sword', 'War hammer' ]
meleeWeapons = [ 'Battle axe', 'Hand axe', 'Mace', 'Pole arm', 'Short sword', 'Silver dagger','Spear', 'Sword', 'War hammer']
clericWeapons = [ 'Mace', 'Sling + 20 stones', 'Staff', 'War hammer' ]
standardMod = { 3 : -3, 4 : -2, 6 : -1, 9 : 0, 13 : 1, 16 : 2, 18 : 3}
intMod = { 3 : 0, 13 : 1, 16 : 2, 18 : 3}
chaMod = { 3 : -2, 4 : -1, 6 : -1, 9 : 0, 13 : 1, 16 : 1, 18 : 2}
spells = ['Charm Person', 'Detect Magic', 'Floating Disc', 'Hold Portal', 'Light', 'Magic Missile', 'Protection from Evil', 'Read Language','Read Magic', 'Shield', 'Sleep', 'Ventriloquism' ]

# FUNCTIONS
def printSheets(party):
  for row in range(len(charSheet)):
    line = ''
    for char in range(len(party)):
      charLine = party[char][row]
      ws = ' ' * (23 - len(charLine)) 
      charLine = ' '  + charLine + ws + '|'
      line = line + charLine
    print(line)


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
  if '+' in firstItem:
    gear.append(firstItem.split('+')[0])
    gear.append(firstItem.split('+')[1])
  else:
    gear.append(firstItem)
  if '+' in secondItem:
    gear.append(secondItem.split('+')[0])
    gear.append(secondItem.split('+')[1])
  else:
    gear.append(secondItem)

  if len(gear) == 3:
    gear.append(' ')
  if len(gear) == 2:
    gear.append(' ')
    gear.append(' ')

  # armor
  if charClass == 'Magic User':
    armor = 'None'
  elif charClass == 'Thief':
    armor = 'Leather'
  else:
    armor = [*armorDict] # unpack dict keys (armor by name) into an array
    armor = armor[diceRoll(1,6) - 1] 

  ac = armorDict[armor]
  for score in standardMod:
    if score <= dex:
      mod = standardMod[score]
  ac = ac - mod

  ## weapon selection
  weaponSelection = []
  # magic users only get daggers
  if charClass == 'Magic User':
    weaponSelection.append('Dagger')

  # clerics only get blunt weapons
  if charClass == 'Cleric':
    weapon = clericWeapons[diceRoll(1,4) - 1]
    secondWeapon = clericWeapons[diceRoll(1,4) - 1]
    while secondWeapon == weapon:
      secondWeapon = clericWeapons[diceRoll(1,4) - 1]
    weaponSelection.append(weapon)
    weaponSelection.append(secondWeapon)

  # everyone else get 1 melee and 1 second weapon
  weapon = meleeWeapons[diceRoll(1,9) - 1]
  secondWeapon = weapons[diceRoll(1,12) - 1]
  weaponSelection.append(weapon)
  weaponSelection.append(secondWeapon)
  
  # everyon gets 3d6 of gold
  gold = diceRoll(3,6)

  # return all equipment
  return ac, armor, weaponSelection, gear, torches, rations, gold

for i in range(charCount):
  stats = []
  for j in range(0,6):
    roll = diceRoll(3,6)
    stats.append(roll)
  
  primaryStats = stats[:4]
  highestPrimary = max(primaryStats)
  highestStat = max(stats) 

  # generate array of possible classes for this character
  possibleClasses = []
  if stats[0] == highestPrimary:
    possibleClasses.append('Fighter')
  if stats[1] == highestPrimary:
    possibleClasses.append('Magic User')
  if stats[2] == highestPrimary:
    possibleClasses.append('Cleric')
  if stats[3] == highestPrimary:
    possibleClasses.append('Thief')

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
    partyClasses.append(charClass)
  else:
    charClass = possibleClasses[0]

  ac, armor, weapon, gear, torches, rations, gold = rollEquip(charClass, stats[3])
  totalGold += gold

  mods = []
  position = 0
  for roll in stats:
    position += 1
    if position == 2:   # intelligence
      statMod = intMod
    elif position == 6: # charisma
      statMod = chaMod
    else: 
      statMod = standardMod
    for score in statMod:
      if score <= roll:
        mod = statMod[score]
    mods.append(mod)

  hd = classes[charClass]['hd']
  hp = diceRoll(1,hd) + mods[4] 
  if hp < 1:
    hp = 1

  gold = str(gold)

  saves = classes[charClass]['saves']

  if charClass == 'Magic User':
    spell = random.choice(spells) 
#  elif charClass == 'Cleric':
#    spell = 'TU -- 1 HD: 7, 2 HD: 9, 3 HD: 11 |'
  else:
    spell = '    ' 

  charSheet = [ 
    charClass, 
    str('STR ' + str(stats[0]) + (' ' * ( 4- len(str(stats[0])))) + '(' + str(mods[0]) + ')' ),
    str('INT ' + str(stats[1]) + (' ' * ( 4- len(str(stats[1])))) + '(' + str(mods[1]) + ')' ),
    str('WIS ' + str(stats[2]) + (' ' * ( 4- len(str(stats[2])))) + '(' + str(mods[2]) + ')' ),
    str('DEX ' + str(stats[3]) + (' ' * ( 4- len(str(stats[3])))) + '(' + str(mods[3]) + ')' ),
    str('CON ' + str(stats[4]) + (' ' * ( 4- len(str(stats[4])))) + '(' + str(mods[4]) + ')' ),
    str('CHA ' + str(stats[5]) + (' ' * ( 4- len(str(stats[5])))) + '(' + str(mods[5]) + ')' ),
    str('----------------------'),
    str('HP: ' + str(hp) + '  AC: ' + str(ac)), 
    str('Torches: ' + torches),
    str('Rations: '  + rations),
    str('Armor: ' + armor),
    str('Weapon:'),
    str('  ' + weapon[0]),
    str('  ' + weapon[1]),
    str('Equipment:'),
    '  Backpack',
    '  Tinderbox',
    '  Waterskin',
    str('  ' + gear[0]),
    str('  ' + gear[1]),
    str('  ' + gear[2]),
    str('  ' + gear[3]),
    str('Gold: ' + gold),
    str('----------------------'),
    str('Death/poison       ' + str(saves[0])),
    str('Wands              ' + str(saves[1])),
    str('Paralysis/Petrify  ' + str(saves[2])), 
    str('Breath Attacks     ' + str(saves[3])),
    str('Spells/Rods/Staves ' + str(saves[4])),
    str('----------------------'),
    'Spells:',
    spell,
    ]

  party.append(charSheet)
  
# print all sheets
characterCount = range(len(party)) 
partySubset = []
modulus = 6
for index in enumerate(characterCount, start=1):
  partySubset.append(party[index[1]])
  if index[0] % modulus == 0:
    printSheets(partySubset)
    print()
    partySubset = []

if len(partySubset) > 0:
  printSheets(partySubset)
print()
print('...Total Party Gold:',str(totalGold))
quit()
