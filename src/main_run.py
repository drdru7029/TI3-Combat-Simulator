import random
from attack_function import *
from colorama import init
from colorama import Fore, Back, Style
from logo import *
from ti3_documentation import *
import csv
from ti3_records import *
from ship_weapons import *
import ship_classes as sc
import ship_components as scomp
from collections import Counter


#ANSI escape sequences for terminal coloring
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#initialize colorama's ANSI library
init(autoreset=True)
player_2_state = []


def dump_to_json(instance):
    import json

    # save ship design to json

    loadout_filename = '{}_{}'.format(instance.commander_name, instance.ship_name)

    ship_session_name = '{}.json'.format(loadout_filename)
    with open(ship_session_name, 'w') as f:
        json.dump(instance.__dict__, f)
    print('{} saved'.format(ship_session_name))
    print('Ship loadout saved as {}'.format(json.dumps(instance.__dict__)))


def load_from_json(filename):
    import json

    with open(filename) as json_file:
        print('')
        print('{} loaded.'.format(filename))
        print('')
        loaded_object = json.load(json_file)
        print('loaded_object',loaded_object)
        return sc.Ship(**loaded_object)


def allow_partial_inputs(Class_and_attribute, choice):
    """Allow the player to enter partial weapon name keys"""

    for each in Class_and_attribute:
        if choice in each:
            choice = each
            break



    return choice



def create_ship():
    valid = False
    while not valid:
        new_ship_name = input(str("Enter your ship name: "))
        if len(new_ship_name)<=25:
            valid = True
        else:
            print("Your name is too long, please limit to less than or equal to 25 characters.")
    valid = False
    return new_ship_name

master_component_dict = {'weapons': my_weapon_class_dict, 'shields':scomp.my_component_class_dict['shields'],
                         'capacitor':scomp.my_component_class_dict['capacitor'], 'accuracy': scomp.my_component_class_dict['accuracy'],
                         'defense': scomp.my_component_class_dict['defense'], 'mobility':scomp.my_component_class_dict['mobility']}

# create_ship()


ship_1 = sc.Ship(weapon_types=None, max_attack=0, min_attack=0, defense=0, mobility=0, accuracy=0, capacitor=0,
                 signature=0, current_total_points_all=0, ship_name='Ship 1', commander_name=None, damage=0,
                 status='all systems go', shields=None)

ship_2 = sc.Ship(weapon_types=None, max_attack=0, min_attack=0, defense=0, mobility=0, accuracy=0, capacitor=0,
                 signature=0, current_total_points_all=0, ship_name='Ship 2', commander_name=None, damage=0,
                 status='all systems go', shields=None)



# def input_controls(attribute, ship):
    #allow the user to input the initial design



def add_component(ship, ship_attribute_key):

    """Should be run for each adjustable attribute in the active ship.

    ship = active ship instance (e.g. ship_1)
    ship_attribute_key = currently selected attribute (e.g. 'weapons')

    """

    valid = False
    current_totals_pre = 0
    count = 0
    new_attribute_input = 0

    try:
        bay_count = sc.Ship.attribute_dict[ship_attribute_key]['bay count']
    except:
        bay_count = 1

    while new_attribute_input not in sc.Ship.attribute_dict[ship_attribute_key]['options']:
        try:

            new_attribute_choice = input(
                "You may enter up to {} {}. Enter the full or partial name of "
                "your first {} (you have {} cap remaining), ""and your choices include: {}: "
                    .format(bay_count, ship_attribute_key,
                            ship_attribute_key, sc.Ship.total_points_per_capacitor,
                            sc.Ship.attribute_dict[ship_attribute_key]['options']))

            new_attribute_input = allow_partial_inputs(sc.Ship.attribute_dict[ship_attribute_key]['options'],
                                                       new_attribute_choice)


        except:
            print("You have no such choice. Try again.")

    new_attribute_keys = [new_attribute_input]  # append any subsequent weapon selection to this list

    count += 1

    new_attribute_input = master_component_dict[ship_attribute_key].get(
        new_attribute_input)  # tie in selection with the pertinent data from the selected weapon class
    print('newattinput', new_attribute_input)
    #This would apply to the ship being fit all 'special' attributes in one place. Need to figure out how to
    #call the function from within the class. Edit, this seems to work!
    #Note, the final effects of all actions within this function should fit nicely to all of the main
    #attributes designated in the ship class. As long as these two variables agree, no other complexity should be needed
    try:
        new_attribute_input.apply_basic_ship_attributes(new_attribute_input, ship)
    except AttributeError:
        pass

    new_attribute_input = new_attribute_input.class_dict.get('power')  # grab the value of the input
    # BeamLaser.class_dict.get('power')
    new_item_attribute_values = [new_attribute_input]





    # add any additional items

    while count < bay_count:

        additional_item_validity = 0
        while additional_item_validity not in sc.Ship.attribute_dict[ship_attribute_key]['options']:
            try:

                additional_item_pre = input("Enter your next {}, or enter 'none' to decline.".format
                                            (ship_attribute_key))
                additional_item = allow_partial_inputs(sc.Ship.attribute_dict[ship_attribute_key]['options'],
                                                       additional_item_pre)
                new_attribute_keys.append(additional_item)

                additional_item_validity = new_attribute_keys[-1]
                if new_attribute_keys[-1] != 'none':
                    additional_item = master_component_dict[ship_attribute_key].get(new_attribute_keys[-1])
                    additional_item = additional_item.class_dict.get('power')
                    new_item_attribute_values.append(additional_item)
                    # if ship_attribute_key == 'weapons':
                    #     ship.min_attack = int(min(new_item_attribute_values))
                    #     ship.max_attack = int(max(new_item_attribute_values))
                count += 1

            except:
                print("You have no such choice. Try again.")
                del new_attribute_keys[-1]  # removes any invalid input from the list
                if new_attribute_keys == 'none':
                    count += 1

            if 'none' in additional_item_validity:
                del new_attribute_keys[-1]
                break

    # nonlocal new_attribute
    new_attribute = int(max(new_item_attribute_values))

    print('new attribute',new_attribute, 'total cap', sc.Ship.total_points_per_capacitor)
    print('totals', ship.current_total_points_all + new_attribute, 'ship total points', sc.Ship.total_points_all)

    if 1 <= new_attribute <= sc.Ship.total_points_per_capacitor and ship.current_total_points_all + new_attribute <= sc.Ship.total_points_all:
        valid = True
        ship.current_total_points_all += new_attribute
    else:
        print(Fore.RED + "Value entered is not valid - please enter a value between 1 and {}: ".format(
            sc.Ship.total_points_per_capacitor))

    current_totals_pre += int(max(new_item_attribute_values))

    # print('CHECKTHIS',ship.ship_components().mydict[ship_attribute_key], new_attribute)

    # ship.ship_components().mydict[ship_attribute_key] = new_attribute

    return new_attribute_keys


# for keys,values in ship_1.attribute_dict.items():
#     print(keys)
#     for k,v in values.items():
#         print(k,v)

#look at this. we dont' use master_component_dict, or any other code in main_run except for the initial ship instantiation;
#we only use that ship instance's own attribute dict to then connect with the component classes and access all attributes to feed
#back into the ship. perfect.
#the only other complexity is the my_component_class_dict in the ships_component module.



# for keys,values in ship_1.attribute_dict.items():
#     print(keys)
#     for component in ship_1.attribute_dict[keys]['options']:
#         print(component)
#         print(ship_1.attribute_dict[keys]['options'][component].class_dict.items())
#     add_component(ship_1,keys)

def set_ship_design(ship):

    """
    CURRENT: in the process of reforming ship design and add component functionality to require less redundant code
    and put add component operations in a for loop relying on the contents of the Ship class component attributes for
    execution. When ready, only adding new component classes and supplying the ship classes with the necessary attributes
    will be enough to add them to this ship construction function
    To do:
    -finish reforming add_component().
    -connect ship.component to the for loop
    -add minimum viable placeholders for all required components (e.g. accuracy, defense).
    """

    signature = {'signature': []}

    all_component_values = []

    for idx,(keys, values) in enumerate(ship.attribute_dict.items()):
        print(keys)
        for component in ship.attribute_dict[keys]['options']:
            print('component',component)
            print('classdict_info',ship.attribute_dict[keys]['options'][component].class_dict.items())

        new_component_value = add_component(ship, keys)

        ship.ship_components(keys, new_component_value)

    count = 0
    if ship.current_total_points_all < sc.Ship.total_points_all: #as long as current ship points are less than total points
        valid = False
        if count > 0:
            if ship.current_total_points_all < sc.Ship.total_points_all:
                valid = True
        while not valid:
            if int(input('You have not used up all available points. Choose 1 to continue or 2 to start over.\n'))==1:
                valid = True
            else:



                count+=1
                valid = True
    # ship.grow(defense, mobility, accuracy, capacitor, signature)
    # ship.signature = float((ship.max_attack + defense + mobility + accuracy + capacitor) / float(ship.total_points_all))
    ship.signature = 1.0



def set_ship_design_auto(ship):
    current_total_points_all = 0
    max_attack = {'max_attack': []}
    defense = {'defense': []}
    mobility = {'mobility': []}
    accuracy = {'accuracy': []}
    capacitor = {'capacitor': []}
    signature = {'signature': []}
    trait_ideal_min = 5

    current_totals_pre = 0

    #apply weapon choices
    weapon_count = 0
    # new_attribute = 'torpedo'
    weapon_options_count = len(ship.weapon_options)
    weapon_choice = list(range(0, weapon_options_count))
    print('weapon_choice',weapon_choice)

    def ai_choose_weapon():
        #allows the AI to auto-choose from the available weapons, removing the selection from the list each use
        if len(weapon_choice)<weapon_options_count:
            #allows the computer to select only 1 weapon if he so desires
            weapon_choice.append('none')

        for_weapon_choice_decision = [i for i in weapon_choice if i!='none']
        weapon_choice_decision = random.choice(for_weapon_choice_decision)
        del weapon_choice[weapon_choice_decision]

        weapon_attribute = ship.weapon_options[weapon_choice_decision]
        return weapon_attribute
    new_attribute = ai_choose_weapon()


    new_weapon_attribute_keys = [new_attribute]  # append any subsequent weapon selection to this list
    weapon_count += 1
    new_attribute = my_weapon_class_dict.get(new_attribute)  # tie in selection with the pertinent data from the selected weapon class
    new_attribute = new_attribute.class_dict.get('power')  # grab the value of the input
    new_weapon_attribute_values = [new_attribute]

    while weapon_count < ship.weapon_bays:
        additional_weapon_validity = 0
        new_weapon = ai_choose_weapon()
        new_weapon_attribute_keys.append(new_weapon)
        additional_weapon_validity = new_weapon_attribute_keys[-1]

        if new_weapon_attribute_keys[-1] != 'none':
            additional_weapon = my_weapon_class_dict.get(new_weapon_attribute_keys[-1])
            additional_weapon = additional_weapon.class_dict.get('power')
            new_weapon_attribute_values.append(additional_weapon)
            # ship's max_attack value becomes the largest of all selected weapons
            ship.max_attack = int(max(new_weapon_attribute_values))
            ship.min_attack = int(min(new_weapon_attribute_values))
        weapon_count += 1
        # current_totals_pre += int(new_attribute)

        ship.max_attack = int(max(new_weapon_attribute_values))
        ship.min_attack = int(new_attribute)
        current_totals_pre += int(max(new_weapon_attribute_values))
        new_attribute = int(max(new_weapon_attribute_values))

        if 1 <= new_attribute <= sc.Ship.total_points_per_capacitor and ship.current_total_points_all + new_attribute <= sc.Ship.total_points_all:
            valid = True
            ship.current_total_points_all += new_attribute
        else:
            print( 'ai ship selection problem, line 299')
        ship.weapon_types = new_weapon_attribute_keys

    #will want to eventually clean all this up and provide listening variables
    remaining_points = sc.Ship.total_points_all - ship.current_total_points_all
    randrange_low = trait_ideal_min if trait_ideal_min <= remaining_points else remaining_points
    randrange_high = ship.current_total_points_all if ship.current_total_points_all<sc.Ship.total_points_per else sc.Ship.total_points_per
    # print( 'current total poitns all', ship.current_total_points_all
    # print( 'high',randrange_high
    # print( 'low',randrange_low
    try:
        # defense = random.randrange(randrange_low,randrange_high)
        defense = 10
    except:
        try:
            defense = random.randrange(randrange_low, randrange_high)
        except:
            defense = randrange_low
    ship.current_total_points_all += defense
    current_totals_pre += int(new_attribute)
    remaining_points = sc.Ship.total_points_all - ship.current_total_points_all
    randrange_low = trait_ideal_min if trait_ideal_min <= remaining_points else remaining_points
    randrange_high = ship.current_total_points_all if ship.current_total_points_all < sc.Ship.total_points_per else sc.Ship.total_points_per
    mobility = 5
    ship.current_total_points_all += mobility
    remaining_points = sc.Ship.total_points_all - ship.current_total_points_all
    randrange_low = trait_ideal_min if trait_ideal_min <= remaining_points else remaining_points
    randrange_high = ship.current_total_points_all if ship.current_total_points_all < sc.Ship.total_points_per else sc.Ship.total_points_per
    try:
        accuracy = random.randrange(randrange_low,randrange_high)
    except:
        accuracy = randrange_low
    ship.current_total_points_all += accuracy
    current_totals_pre += int(new_attribute)
    remaining_points = sc.Ship.total_points_all - ship.current_total_points_all
    ai_prefer_sigtank = random.randrange(0,1) #50/50 chance that the AI will prefer a lower cap in return for a lower signature. Otherwise, he will max out his cap
    if ai_prefer_sigtank == 1:
        randrange_low = trait_ideal_min if trait_ideal_min <= remaining_points else remaining_points
        randrange_high = ship.current_total_points_all if ship.current_total_points_all < sc.Ship.total_points_per_capacitor else sc.Ship.total_points_per_capacitor
        try:
            capacitor = random.randrange(randrange_low,randrange_high)
        except:
            capacitor = randrange_low
    else:
        try:
            capacitor = remaining_points
        except:
            try:
                randrange_low = trait_ideal_min if trait_ideal_min <= remaining_points else remaining_points
                randrange_high = ship.current_total_points_all if ship.current_total_points_all < sc.Ship.total_points_per_capacitor else sc.Ship.total_points_per_capacitor
                capacitor = random.randrange(randrange_low, randrange_high)
            except:
                capacitor = randrange_low
    ship.current_total_points_all += capacitor
    current_totals_pre += int(new_attribute)
    ship.grow(defense, mobility, accuracy, capacitor, signature)
    print( 'max_attack', ship.max_attack)
    print( 'total points', ship.total_points_all)
    ship.signature = float((ship.max_attack + defense + mobility + accuracy + capacitor) / float(ship.total_points_all))




def ai_auto_generate():
    pass


def combat(ship1,ship2):
    def ai_logic(ship1, ship2):  # this is currently not functioning correctly inside the combat function
        ship_list = ship1, ship2
        """Defines AI max_attack logic--currently no difficulty gradients"""
        if ship_list[defending_ship].defense >= max_attack:
            if max_attack>7: #the AI decides whether to risk a high powered max_attack
                suicide_attack_chance = random.randrange(0,10)
                if suicide_attack_chance>=7: #the AI will risk a high powered max_attack
                    try:
                        print( Fore.RED + "{}'s powered his guns to the max!".format(ship2.ship_name))
                        attack_strike = max_attack
                    except:
                        attack_strike = ship_list[attacking_ship].capacitor
            else: #the AI decides to play it safe
                try:
                    attack_strike = max_attack
                except:
                    attack_strike = ship_list[attacking_ship].capacitor
        else:
            try:
                attack_strike = ship_list[defending_ship].defense+1
            except:
                attack_strike = max_attack
        # print( 'AI ATTACK STRIKE', attack_strike
        return attack_strike
    for_combat_log = [[]]
    if len(player_2_state)==0:
        player_2_state.append((int(input("Press 1 if Player 2 is Human, or 2 if a Computer"))))

    battle_has_begun = False
    valid = False
    while not valid:
        ship_list = ship1,ship2 #REMEMBER, ship1 and ship2 are static variables; ship1 will always be the
        #first ship to enter information.
        # print('ship_list',ship_list)
        attacking_ship = 0
        #This is the combat loop that plays out until one ship's defenses are reduced to 0
        while ship1.defense > 0 and ship2.defense > 0:
            if attacking_ship == 0:
                defending_ship = 1
            else:
                defending_ship = 0
            #sets the ship objects to the proper attackers/defenders
            if attacking_ship == 0:
                attacking_ship_object = ship1
                defending_ship_object = ship2
            else:
                attacking_ship_object = ship2
                defending_ship_object = ship1
            #set max_attack to either max_attack or capacitor, whichever is smallest
            if ship_list[attacking_ship].max_attack <= ship_list[attacking_ship].capacitor:
                max_attack = ship_list[attacking_ship].max_attack
            else:
                max_attack = ship_list[attacking_ship].capacitor

            # def execute_attack():
            if attacking_ship==0 or attacking_ship==1 and player_2_state[0]==1:
                if ship_list[attacking_ship].capacitor > 0: #Ships cannot fire if cap has been reduced to 0
                    valid2 = False
                    while not valid2:
                        try:
                            if battle_has_begun==False:
                                current_weapon = (input('{}, equip your weapon using its partial or full name, your choices are: {}.'.
                                                        format(ship_list[attacking_ship].ship_name,
                                                               ship_list[attacking_ship].weapon_types)))

                                current_weapon = allow_partial_inputs(ship_list[attacking_ship].weapon_types, current_weapon)

                                battle_has_begun = True

                            else:
                                if current_weapon: #give player the option to continue with previous weapon
                                    continue_with_weapon = input("Press enter to continue with your previous weapon, or "
                                                                 "enter a new one from this list: {}".format
                                                                 (ship_list[attacking_ship].weapon_types))
                                    if len(continue_with_weapon)>0:
                                        current_weapon = continue_with_weapon
                                        current_weapon = allow_partial_inputs(ship_list[attacking_ship].weapon_types,
                                                                              current_weapon)
                                else:
                                    current_weapon = (input('{}, equip your weapon, choices are: {}.'.
                                                            format(ship_list[attacking_ship].ship_name,ship_list[attacking_ship].weapon_types)))

                                    current_weapon = allow_partial_inputs(ship_list[attacking_ship].weapon_types,
                                                                          current_weapon)

                            if current_weapon in ship_list[attacking_ship].weapon_types:
                                valid2 = True
                                current_weapon_equip = my_weapon_class_dict.get(current_weapon)  # tie in selection with the pertinent data from the selected weapon class
                                current_weapon_equip = current_weapon_equip.class_dict.get('power')
                                valid3 = False
                                while not valid3:
                                    try:
                                        attack_strike = int(input(Fore.GREEN + '{}, you have equipped your {}. Enter your '
                                                                               'attack amount, max {}: '.format(ship_list[attacking_ship].ship_name,current_weapon,current_weapon_equip)))
                                        if attack_strike<=max_attack:
                                            valid3 = True
                                    except:
                                        print('That was not a valid input, try again',current_weapon)
                                max_attack = current_weapon_equip

                        except NameError:
                            print( Fore.GREEN + 'That was not a valid input, try again')

                    #the following loop ensures a valid max_attack is input before continuing
                    while attack_strike > ship_list[attacking_ship].max_attack or attack_strike > ship_list[attacking_ship].capacitor:
                        if attack_strike > ship_list[attacking_ship].max_attack:
                            print( Fore.RED + 'Your order exceeds our designed max_attack power, try again!')
                        elif attack_strike > ship_list[attacking_ship].capacitor:
                            print( Fore.RED + 'You do not have enough remaining capacitor energy, try again!')
                        attack_strike = int(input(Fore.GREEN + '{}, enter your max_attack amount: '.format(ship_list[attacking_ship].ship_name)))

                    attack_result = attack_power(ship_list[attacking_ship],ship_list[defending_ship],attack_strike)
                    attack_result = attack_result[0]
                    valid = True

                    if attack_result > 0:  # if the max_attack did not miss
                        defending_ship_object.defense -= attack_result
                    if attacking_ship_object.capacitor > 0:
                        attacking_ship_object.capacitor -= attack_strike

                    sc.Ship.capacitor_recharge = random.randrange(2,4)#capacitor will recharge within this range each round
                    ship1.capacitor += sc.Ship.capacitor_recharge
                else:
                    print( Fore.RED + "{} cannot make an max_attack, as his capacitor is completely drained".format(ship_list[attacking_ship].ship_name))
                    sc.Ship.capacitor_recharge = random.randrange(2, 4)
                    ship1.capacitor += sc.Ship.capacitor_recharge
            # Checks if player 2 is a human or computer. If computer, initializes AI actions
            elif attacking_ship == 1:  # if the attacker is player 2
                if player_2_state[0] == 2:  # if player 2 is a computer
                    try:
                        attack_strike = ai_logic(ship1,ship2)
                        print( '*utilizing comprehensive AI logic*')
                    except:
                        print( '*utilizing simplified AI logic*')
                        try:
                            if attack_strike > ship_list[attacking_ship].max_attack:
                                attack_strike = max_attack
                        except:
                            attack_strike = ship_list[attacking_ship].capacitor
                    attack_result = attack_power(ship_list[attacking_ship], ship_list[defending_ship],
                                                 attack_strike)
                    attack_result = attack_result[0]
                    valid = True

            if attacking_ship==1:
                if attack_result > 0:  # if the max_attack did not miss
                    defending_ship_object.defense -= attack_result
                attacking_ship_object.capacitor -= attack_strike
                sc.Ship.capacitor_recharge = random.randrange(2, 4)
                attacking_ship_object.capacitor += sc.Ship.capacitor_recharge
            if attacking_ship == 0:
                attacking_ship = 1
            elif attacking_ship == 1:
                attacking_ship = 0

            print( '**')
            justified_reports(ship1, ship2)
            print( '**')
            # return attacking_ship, defending_ship
            #execute_attack()
    if ship1.defense <=0 or ship2.defense <=0:
        #in order to factor in a tie shot, I've got to put all of the above into a function else i'll be
        #spamming way too much code
        if ship1.defense <= 0:
            ship_win = 1
            ship_lose = 0
            for_combat_log = ['Lose', 'Win']
            record_battle_history(for_combat_log)
        else:
            ship_win = 0
            ship_lose = 1
            for_combat_log = ['Win','Lose']
            record_battle_history(for_combat_log)
        print( "")
        print( Back.BLUE + "Congratulations mighty {}, you have won the battle! {}'s broken hull" \
              " now lay in the black of space for all eternity. Might this be a lesson " \
              "to all who dare to oppose you.".format(ship_list[ship_win].ship_name, ship_list[ship_lose].ship_name))
        valid = True

'''---------------------------Menu management area---------------------------'''


def justified_reports(ship1, ship2):
    #Fix the columns and justification of ship reports
    report_1 = ship1.report()
    report_2 = ship2.report()
    col_width = max(len(str(word)) for row in report_1.items() for word in row) + 1  # padding
    for row, row2 in zip(report_1.items(), report_2.items()):
        print( "".join(str(word).ljust(col_width) for word in row), ' ', "".join(
            str(word).ljust(col_width) for word in row2))
    print( '')

def display_menu():
    print( Back.GREEN + "Welcome to the TI3 Tactical Simulator!")
    ti3_logo = logo_style()
    print( ti3_logo)
    print('1. Craft ships')
    print("2. Read some tips")
    print("3. [Placeholder]")
    print("4. Commence battle")
    print("5. View current ship reports")
    print("6. Set Player 2 to Human or Computer")
    print("7. Load existing ship layouts")
    print("0. Exit the tactical simulator program")
    print("")
    print( Style.BRIGHT + "Please select an option from the above menu")

def get_menu_choice():
    option_valid = False
    while not option_valid: #these two lines basically mean "until a valid option is entered, do this"
        try:
            choice = input("Option Selected: ")
            if 0<= int(choice) <= 7:
                option_valid = True
            else:
                print( Fore.RED + "Please enter a valid option")
        except ValueError:
            print( Fore.RED + "Please enter a valid option")
    return int(choice)

computer_commander_names = ['Locutus of Borg', 'Yoda', 'Merci of El Nath', 'Leviathan', "Ace's Evil Twin",
                            "Tops's Evil Twin", "Spade's Evil Twin", "Hitler's Spawn"]
computer_ship_names = ['Apocalypse', 'Enterprise', 'Excelsior', 'Red Baron']


def reset_ships(ship):
    #resets values upon a new combat session
    ship.current_total_points_all = 0
    ship.max_attack = 0
    ship.defense = 0
    ship.mobility = 0
    ship.accuracy = 0
    ship.capacitor = 0
    ship.signature = 0

def manage_ships(ship1,ship2):
    print( Back.BLUE + "This is a TI3-inspired tactical space combat simulator")
    print( "")
    noexit = True
    while noexit:
        display_menu()
        option = get_menu_choice()
        print( "")
        if option == 1:
            #if fighting more than 1 battle per program execution, reset previous values
            reset_ships(ship1)
            reset_ships(ship2)

            commander_name = input(str(Back.CYAN + "What is the name of player 1?"))
            ship_name = input(str(Back.CYAN + "Choose a name for your ship: "))

            ship1.commander_name = commander_name
            ship1.ship_name = ship_name

            set_ship_design(ship1)

            #save ship to json
            print(ship1.commander_name, ship1.commander_name)
            dump_to_json(ship1)


            print( "")
            justified_reports(ship1, ship2)
            print( "")
            #if set to 2, auto select name and call function to auto set attributes
            p2_manual_auto = input(str(Back.CYAN + "Press 1 to manually set opposing player traits, or 2 to auto generate them"))
            if p2_manual_auto==1:
                commander_name = input(str(Back.CYAN + "What is the name of player 2? "))
                ship2.commander_name = commander_name
                set_ship_design(ship2)

            else:
                commander_name = computer_commander_names[random.randrange(0,len(computer_commander_names))]
                ship2.commander_name = commander_name

                ship_name = computer_ship_names[random.randrange(0,len(computer_ship_names))]
                ship2.ship_name = ship_name



                set_ship_design_auto(ship2)

            dump_to_json(ship2)

            print( "")
            justified_reports(ship1, ship2)
            print( "")

        elif option == 2:
            tips_simple()
            print( "")

        elif option == 3:
            print(Fore.RED + "This is a work in progress and has not yet been implemented")
            print( '')

        elif option == 4: #commence battle
            combat(ship_1, ship_2)
            # print( "This is a work in progress and has not yet been implemented"
            print( '')

        elif option == 5:
            justified_reports(ship1,ship2)

        elif option == 6:
            player_2_state.append(input("Press 1 if Player 2 is Human, or 2 if a Computer"))
            print( "")

        elif option == 7:
            ship_1 = load_from_json('ace_test.json')
            ship_2 = load_from_json('Merci of El Nath_Enterprise.json')

        elif option == 0:
            noexit = False
            print( "")
    print(Fore.BLUE + Back.WHITE + "Thank you for using the tactical space combat simulator")

def main():
    #instantiate the class
    # ship_1 = Ship(0,0,0,0,0)
    # set_ship_design(ship_1)
    manage_ships(ship_1, ship_2)
    print(sc.Ship.num_of_ships)

if __name__ == "__main__":
    main()