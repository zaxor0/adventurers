#!/usr/bin/python3

import random
import yaml

with open('ose/player-classes.yaml','r') as file:
  playerClasses = yaml.safe_load(file)


attr = { 'Strength' : 0, 'Intelligence' : 0, 'Wisdom' : 0, 'Dexterity' : 0, 'Constitution' : 0, 'Charisma' : 0 }

def main():
  # roll stats
  highestRoll = 0
  for stat in attr:
    statRoll = diceRoll(3,6)
    if statRoll > highestRoll:
      highestRoll = statRoll
    attr[stat] = statRoll
  bestStats = []
  for stat in attr:
    if attr[stat] >= highestRoll:
      bestStats.append(stat)
  possibleClasses = []
  # create an array of classes the rolls qualify the player for
  for pClass in playerClasses:
    qClass  = playerClasses[pClass]
    # if there are no requirements, add it to the array
    if qClass['Requirements'] == 'None':
      possibleClasses.append(pClass)
    # else evaluate player stats against class requirements
    else:
      reqs = qClass['Requirements']
      reqCount = 0
      reqMeetCount = 0
      for stat in reqs:
        reqCount += 1
        if attr[stat] >= reqs[stat]:
          reqMeetCount += 1
      if reqMeetCount == reqCount:
        possibleClasses.append(pClass)
  # narrow the choices to those whose prime req. matches the player's highest stat(s)
  choicestClasses = []
  for pClass in possibleClasses:
    for pr in playerClasses[pClass]['Prime-Requisite']:
      if pr in bestStats:      
        choicestClasses.append(pClass)
  if len(choicestClasses) == 0:
    # if choicest classes is empty, can happen if con is your best score, compare against second best
    nextHighestRoll = 0
    for stat in attr:
      if stat != bestStats[0] and attr[stat] > nextHighestRoll:
        nextHighestRoll = attr[stat]
        nextHighestStat = stat
    choicestClasses = []
    for pClass in possibleClasses:
      for pr in playerClasses[pClass]['Prime-Requisite']:
        if pr == nextHighestStat:      
          choicestClasses.append(pClass)

  playerClass = random.choice(choicestClasses)
  characterSheet(playerClass, attr)

def characterSheet(playerClass, attr):
  print('you are a', playerClass)
  for stat in attr:
    tabs = '\t'
    if len(stat) < 7:
      tabs = '\t\t'
    print(stat,tabs,attr[stat])



def diceRoll(dieCount,dieSides):
  dieTotal = 0
  for i in range(0,dieCount):
    min = 1
    max = dieSides
    dieVal = random.randint(min,max)
    dieTotal += dieVal
  return(dieTotal)

main()
