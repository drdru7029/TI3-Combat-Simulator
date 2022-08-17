from main_run import *

def attack_power(ship_attacker, ship_defender, attack_strength):

    """Defines the attack mechanics of a ship"""

    #Higher attack power will yield higher variations in actual attack strength
    attack_stats = []
    if attack_strength>5:
        range_value = attack_strength-5
        range_value = attack_strength-range_value
        attack_value = random.uniform(range_value,attack_strength) #numpy allows float arrays, randrange does not
        #but, random.uniform will return a random float within a range
        # print(attack_value

    #Lower attack power will achieve higher atack strength
    elif 4 <= attack_strength <= 6 :
        range_value = attack_strength-3
        range_value = attack_strength-range_value
        attack_value = random.uniform(range_value,attack_strength)
        # print(attack_value

    else:
        range_value = attack_strength - 1
        range_value = attack_strength - range_value
        attack_value = random.uniform(range_value, attack_strength)


    #Accuracy determines whether or not the activated attack hits or misses
    chance_of_hit = random.randrange(1,10)
    #Penalize very large attack values by increasing miss chance, while rewarding small values by decreasing it
    if attack_value >= 8:
        chance_of_hit += 3
    elif attack_value >= 6:
        chance_of_hit += 2
    if attack_value < 2:
        chance_of_hit -= 3
    elif attack_value < 4:
        chance_of_hit = chance_of_hit
    # print('chance of hit', chance_of_hit
    attack_value_post_sig = float(attack_value * ship_defender.signature)


    if chance_of_hit>ship_attacker.accuracy:
        print(Fore.RED + "Damn it all to hell, {} tried to attack with a power of {} and missed!".format(ship_attacker.ship_name, attack_strength))
        attack_stats.append(0)
        attack_value = 0
    else:
        if attack_value/attack_strength>=.9:
            print(Fore.GREEN + "{} achieved a direct hit with a strength of {}, of which {} landed due to {}'s signature!"
                  .format(ship_attacker.ship_name, attack_value, attack_value_post_sig, ship_defender.ship_name))
        elif attack_value/attack_strength>=.7:
            print(Fore.GREEN + "{} struck a reasonable hit with a strength of {}, of which {} landed due to {}'s "
                               "signature. It could have been better.".format(ship_attacker.ship_name, attack_value,
                                                                              attack_value_post_sig, ship_defender.ship_name))
        elif attack_value/attack_strength>=.5:
            print(Fore.LIGHTGREEN_EX + "{} needs to improve his focus-- he barely matched half of his attack power and "
                                       "hit with a strength of {}, of which {} landed due to {}'s signature!"
                  .format(ship_attacker.ship_name, attack_value, attack_value_post_sig, ship_defender.ship_name))
        else:
            print(Fore.LIGHTGREEN_EX + "This was a terrible shot, {} was too ambitious in his strike, only hitting with "
                                       "an attack strength of {},of which {} landed due to {}'s signature!"
                  .format(ship_attacker.ship_name, attack_value, attack_value_post_sig, ship_defender.ship_name))
        #record hits to a list for subsequent stat tracking
        attack_stats.append(attack_value)
    attack_value = float(attack_value * ship_defender.signature)


    #With high attack values there is a 30% chance of having the attacker's capacitor drained to 0. Is it worth the risk?
    if attack_strength >=8:
        chance_of_capacitor_damage = random.randrange(0,10)
        # chance_of_capacitor_damage = 10
        # print('chance of capacitor damage', chance_of_capacitor_damage
        if chance_of_capacitor_damage >=7:
            ship_attacker.capacitor-=3
            # if ship_attacker.capacitor > 0:
            #     ship_attacker.capacitor=0
            print("Good God, {}'s insanely risky attack power caused his capacitor to breach, draining it heavily!".format(ship_attacker.ship_name))
    return attack_value, attack_stats