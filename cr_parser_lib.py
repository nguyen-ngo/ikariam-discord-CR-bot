import re
import os
import json


def crParse(cr_file, cr):
    with open(cr_file, "r") as file:
        cr_result = json.load(file)  # dict

    clans = []
    for clan in cr_result:
        clans.append(clan)

    regex_attackers = r"(.+\n vs)"
    attackers = re.findall(r"(.+\n vs)", cr, re.VERBOSE)  # list
    defenders = re.findall(r"(vs\n .+)", cr, re.VERBOSE)  # list
    for clan in clans:
        regex_attacker = r"(\[({})\])".format(clan)
        attacker = re.findall(regex_attacker, attackers[0], re.MULTILINE)
        if len(attacker) != 0:
            break

    for clan in clans:
        regex_defender = r"(\[({})\])".format(clan)
        defender = re.findall(regex_defender, defenders[0], re.MULTILINE)
        if len(defender) != 0:
            break

    attacker = attacker[0][1]
    defender = defender[0][1]

    damage_regex = re.compile(r"(Damage Received[.]+([0-9]+))", re.M)
    damage = damage_regex.findall(cr)

    attacker_damage_received = int(damage[0][1])
    defender_damage_received = int(damage[1][1])
    cr_change = {}
    cr_change[attacker] = attacker_damage_received
    cr_change[defender] = defender_damage_received

    with open(cr_file, "r") as result_file:
        cr_result = json.load(result_file)  # dict

    cr_result[attacker] += attacker_damage_received
    cr_result[defender] += defender_damage_received

    with open(cr_file, "w+") as result_file:
        result_file.write(json.dumps(cr_result))
    return attacker, defender, cr_change, cr_result


def getTotalDamage():
    with open("iks-vs-dwood.json".format(os.sep), "r") as result_file:
        result = json.load(result_file)  # dict
    return result
