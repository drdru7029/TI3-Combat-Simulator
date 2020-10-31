def combat(ship1,ship2):
    valid = False
    while not valid:
        ship_list = ship1,ship2
        attacking_ship = 0
        if attacking_ship==0:
            defending_ship = 1
        else:
            defending_ship = 0
        #This is the combat loop that plays out until one ship's defenses are reduced to 0
        while ship1.defense > 0 and ship2.defense > 0:
            if ship_list[attacking_ship].attack <= ship_list[attacking_ship].capacitor:
                max_attack = ship_list[attacking_ship].attack
            else:
                max_attack = ship_list[attacking_ship].capacitor
            #Checks if player 2 is a human or computer. If computer, initializes AI actions
            if attacking_ship==1: #if the attacker is player 2
                if player_2_state == 2: #if player 2 is a computer
                    try:
                        attack_strike = ai_logic()
                        print attack_strike
                    except:
                        try:
                            if attack_strike > ship_list[attacking_ship].attack:
                                attack_strike = max_attack
                        except:
                            attack_strike = ship_list[attacking_ship].capacitor
                    attack_result = attack_power(ship_list[attacking_ship], ship_list[defending_ship], attack_strike)
                    attack_result = attack_result[0]
                    valid = True
                    if attack_result > 0:  # if the attack did not miss
                        ship1.defense -= attack_result
                    ship2.capacitor -= attack_strike
                    ship2.capacitor += Ship.capacitor_recharge
                    print 'attack strike',attack_strike
                    print 'attack result', attack_result
                else: #if player 2 is human
                    attack_strike = int(input(Fore.GREEN + '{}, enter your attack amount, max {}: '.format(ship_list[attacking_ship].ship_name,max_attack)))
                    attack_result = attack_power(ship_list[attacking_ship], ship_list[defending_ship], attack_strike)
                    attack_result = attack_result[0]
                    valid = True
            else:#if the attacker is player 1
                attack_strike = int(input(Fore.GREEN + '{}, enter your attack amount, max {}: '.format(ship_list[attacking_ship].ship_name, max_attack)))
                attack_result = attack_power(ship_list[attacking_ship], ship_list[defending_ship], attack_strike)
                attack_result = attack_result[0]
                valid = True
            if player_2_state==2: #for human input error responses
                if attacking_ship==0: #if human player 1 is attacking
                    if ship_list[attacking_ship].capacitor > 0: #Ships cannot fire if cap has been reduced to 0
                        #the following loop ensures a valid attack is input before continuing
                        while attack_strike > ship_list[attacking_ship].attack or attack_strike > ship_list[attacking_ship].capacitor:
                            if attack_strike > ship_list[attacking_ship].attack:
                                print Fore.RED + 'Your order exceeds our designed attack power, try again!'
                            elif attack_strike > ship_list[attacking_ship].capacitor:
                                print Fore.RED + 'You do not have enough remaining capacitor energy, try again!'
                            attack_strike = int(input(Fore.GREEN + '{}, enter your attack amount: '.format(ship_list[attacking_ship].ship_name)))
                        attack_result = attack_power(ship_list[attacking_ship],ship_list[defending_ship],attack_strike)
                        attack_result = attack_result[0]
                        valid = True
            if attacking_ship==0:
                if attack_result > 0:  # if the attack did not miss
                    ship2.defense -= attack_result
                ship1.capacitor -= attack_strike
                ship1.capacitor += Ship.capacitor_recharge
            if player_2_state==1:
                if attacking_ship==1:
                    if attack_result > 0:  # if the attack did not miss
                        ship1.defense -= attack_result
                    ship2.capacitor -= attack_strike
                    ship2.capacitor += Ship.capacitor_recharge
            if attacking_ship == 0:
                attacking_ship = 1
            elif attacking_ship == 1:
                attacking_ship = 0
            print ship_list[0].report()
            print ship_list[1].report()
    if ship1.defense <=0 or ship2.defense <=0:
        if ship1.defense <= 0:
            ship_win = 1
            ship_lose = 0
        else:
            ship_win = 0
            ship_lose = 1
        print ""
        print Back.BLUE + "Congratulations mighty {}, you have won the battle! {}'s broken hull" \
              " now lay in the black of space for all eternity. Might this be a lesson " \
              "to all who dare to oppose you.".format(ship_list[ship_win].ship_name, ship_list[ship_lose].ship_name)