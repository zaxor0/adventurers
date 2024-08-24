#!/usr/bin/python3

import random
import yaml

with open('player-classes.yaml','r') as file:
  playerClasses = yaml.safe_load(file)


attr = { 'strength' : 0, 'intelligence' : 0, 'wisdom' : 0, 'dexterity' : 0, 'constitution' : 0, 'charisma' : 0 }

def main():
  # roll stats
  for stat in attr:
    statRoll = diceRoll(3,6)
    attr[stat] = statRoll

  print(attr)


def diceRoll(dieCount,dieSides):
  dieTotal = 0
  for i in range(0,dieCount):
    min = 1
    max = dieSides
    dieVal = random.randint(min,max)
    dieTotal += dieVal
  return(dieTotal)

main()
