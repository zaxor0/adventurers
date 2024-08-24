#!/usr/bin/python3

import random
import yaml

with open('player-classes.yaml','r') as file:
  playerClasses = yaml.safe_load(file)


attr = { 'Strength' : 0, 'Intelligence' : 0, 'Wisdom' : 0, 'Dexterity' : 0, 'Constitution' : 0, 'Charisma' : 0 }

def main():
  # roll stats
  for stat in attr:
    statRoll = diceRoll(3,6)
    attr[stat] = statRoll
  print(attr)
  possibleClasses = []
  # create an array of classes the rolls qualify the player for
  for pClass in playerClasses:
    qClass  = playerClasses[pClass]
    # if there are no requirements, add it to the array
    if qClass['Requirements'] == 'None':
      possibleClasses.append(qClass)
    # else evaluate player stats against class requirements
    else:
      reqs = qClass['Requirements']
      for stat in reqs:
        if attr[stat] >= reqs[stat]:
          print(stat)

def diceRoll(dieCount,dieSides):
  dieTotal = 0
  for i in range(0,dieCount):
    min = 1
    max = dieSides
    dieVal = random.randint(min,max)
    dieTotal += dieVal
  return(dieTotal)

main()
