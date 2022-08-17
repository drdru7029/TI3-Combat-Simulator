import random
from attack_function import *
from colorama import init
from colorama import Fore, Back, Style
from logo import *
from ti3_documentation import *
import csv
from ti3_records import *
from ship_weapons import *
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

class Ship:
    """A prototype ship type"""

    #constructor
    # def __init__(self,max_attack,defense,mobility,accuracy,total_points_all,total_points_per):
    total_points_all = 45
    total_points_per = 10
    total_points_per_capacitor = 20
    capacitor_recharge = 3
    signature_modifier = 1
    num_of_ships = 0
    weapon_bays = 2
    weapon_options = ['pulse laser', 'beam laser', 'torpedo']
    instances = []

    def __init__(self, weapon_types, max_attack, min_attack, defense, mobility, accuracy, capacitor, signature, current_total_points_all, ship_name):
        #set the attributes with their initial values

        self.damage = 0
        self.weapon_types = weapon_types
        self.max_attack = max_attack
        self.min_attack = min_attack
        self.defense = defense
        self.mobility = mobility
        self.accuracy = accuracy
        self.capacitor = capacitor
        self.signature = signature
        self.current_total_points_all = current_total_points_all
        self.ship_name = ship_name
        self.status = "All systems go"
        Ship.instances.append(self)

        Ship.num_of_ships += 1

    def current_points(self):
        return self.current_total_points_all

    #report on the current state of the ship
    def report(self):
        #return a dictionary containing all attributes
        ship_dictionary = {'current damage':self.damage, 'weapon type': self.weapon_types, 'max_attack':self.max_attack, 'min attack': self.min_attack,'defense':self.defense, 'mobility':self.mobility,
                'accuracy':self.accuracy, 'capacitor': self.capacitor, 'signature': self.signature,'current total points':self.current_total_points_all,
                'total points per system':self.total_points_per, 'commander name':self.ship_name}
        # ship_dictionary_upper = Counter()
        # for k, v in ship_dictionary.items():
        #     ship_dictionary_upper.update({k.upper(): v})
        return ship_dictionary

    def update_status(self):
        if self.defense - self.damage <= 7:
            self.status = "We have sustained minor damage"
        elif self.defense - self.damage <= 5:
            self.status = "We have sustained moderate damage"
        elif self.defense - self.damage <= 3:
            self.status = "We have sustained heavy damage"
        elif self.defense - self.damage <= 2:
            self.status = "We have sustained critical damage and are at risk of total systems failure!"
        else:
            self.status = "All systems go"

    #lesson: this 'grow' method is critical in being able to record values from the subsequent functions
    def grow(self, defense, mobility, accuracy, capacitor, signature):
        # self.max_attack = max_attack
        self.defense = defense
        self.mobility = mobility
        self.accuracy = accuracy
        self.capacitor = capacitor
        self.signature = float((self.max_attack + defense + mobility + accuracy + capacitor) / Ship.total_points_all)

def create_ship():
    valid = False
    while not valid:
        new_ship_name = input(str("Enter your ship name: "))
        if len(new_ship_name)<=25:
            valid = True
        else:
            print "Your name is too long, please limit to less than or equal to 25 characters."
    valid = False
    return new_ship_name

# create_ship()
ship_1 = Ship(None,0,0,0,0,0,0,0,0,'Ship 1')
ship_2 = Ship(None,0,0,0,0,0,0,0,0,'Ship 2')

def input_controls(attribute, ship):
    #allow the user to input the initial design
    current_totals_pre = 0
    valid = False

    while not valid:
        try:
            if attribute.keys()==['capacitor']: #capacitor value has a different limit than other ship attributes
                new_attribute = input("Enter your {} value up to {}: ".format(attribute.keys(), Ship.total_points_per_capacitor))
                valid = True
                current_totals_pre += int(new_attribute)

                if 1 <= new_attribute <= Ship.total_points_per and ship.current_total_points_all+new_attribute <= Ship.total_points_all:
                    valid = True
                    ship.current_total_points_all+=new_attribute
                else:
                    print Fore.RED + "Value entered is not valid - please enter a value between 1 and {}: ".format(Ship.total_points_per)

            elif attribute.keys()==['weapon type']: #special case for weapons, in order access weapon subclasses,
                #and apply any additional weapons
                weapon_count = 0
                new_attribute = 0
                while new_attribute not in my_weapon_class_dict:
                    try:
                        new_attribute = raw_input("You may enter up to {} weapons. Enter your first {} (you have {} cap remaining), "
                                              "and your choices include: {}: "
                                              .format(Ship.weapon_bays, attribute.keys(), Ship.total_points_per_capacitor,
                                                      Ship.weapon_options))
                    except:
                        print "You have no such choice. Try again."

                new_weapon_attribute_keys = [new_attribute] #append any subsequent weapon selection to this list
                weapon_count+=1
                new_attribute = my_weapon_class_dict.get(new_attribute) #tie in selection with the pertinent data from the selected weapon class
                new_attribute = new_attribute.weapon_dict.get('attack power') #grab the value of the input
                new_weapon_attribute_values = [new_attribute]

                #add any additional weapons
                while weapon_count < ship.weapon_bays:
                    additional_weapon_validity = 0
                    while additional_weapon_validity not in my_weapon_class_dict:
                        try:
                            new_weapon_attribute_keys.append(raw_input("Enter your next weapon, or enter 'none' to decline."))
                            additional_weapon_validity = new_weapon_attribute_keys[-1]
                            print 'additional_weapon_validity',additional_weapon_validity
                            print 'new_weapon_attribute_keys',new_weapon_attribute_keys
                            if new_weapon_attribute_keys[-1] != 'none':
                                additional_weapon = my_weapon_class_dict.get(new_weapon_attribute_keys[-1])
                                additional_weapon = additional_weapon.weapon_dict.get('attack power')
                                new_weapon_attribute_values.append(additional_weapon)
                                #ship's max_attack value becomes the largest of all selected weapons
                                ship.max_attack = int(max(new_weapon_attribute_values))
                                ship.min_attack = int(min(new_weapon_attribute_values))
                            weapon_count+=1
                        except:
                            print "You have no such choice. Try again."
                            del new_weapon_attribute_keys[-1] #removes any invalid input from the list
                            if new_weapon_attribute_keys == 'none':
                                weapon_count += 1
                        if 'none' in additional_weapon_validity:
                            del new_weapon_attribute_keys[-1]
                            break


                else:
                    # current_totals_pre += int(new_attribute)
                    ship.min_attack = int(new_attribute)
                current_totals_pre += int(max(new_weapon_attribute_values))
                new_attribute = int(max(new_weapon_attribute_values))

                if 1 <= new_attribute <= Ship.total_points_per_capacitor and ship.current_total_points_all+new_attribute <= Ship.total_points_all:
                    valid = True
                    ship.current_total_points_all+=new_attribute
                else:
                    print Fore.RED + "Value entered is not valid - please enter a value between 1 and {}: ".format(Ship.total_points_per_capacitor)
                ship.weapon_types = new_weapon_attribute_keys
            else:
                new_attribute = input("Enter your {} value up to {}: ".format(attribute.keys(), Ship.total_points_per))
                current_totals_pre += int(new_attribute)
                if 1 <= new_attribute <= Ship.total_points_per and ship.current_total_points_all+new_attribute <= Ship.total_points_all:
                    valid = True
                    ship.current_total_points_all+=new_attribute
                else:
                    print Fore.RED + "Value entered is not valid - please enter a value between 1 and {}: ".format(Ship.total_points_per)
        except ValueError:
            Fore.RED + "Value entered is not valid - please enter a value between 1 and {}: ".format(Ship.total_points_per)

    valid = False
    new_attribute = int(new_attribute)
    print 'current points: ', ship.current_points()
    print 'You have {} remaining points'.format(Ship.total_points_all-ship.current_total_points_all)
    return new_attribute

def set_ship_design(ship):
    # #allow the user to input the initial design
    max_attack = {'max_attack': []}
    weapon_type = {'weapon type': []}
    defense = {'defense': []}
    mobility = {'mobility': []}
    accuracy = {'accuracy': []}
    capacitor = {'capacitor': []}
    signature = {'signature': []}
    # max_attack = input_controls(max_attack, ship)
    weapon_type = input_controls(weapon_type, ship)
    defense = input_controls(defense, ship)
    # mobility = input_controls(mobility, ship)
    mobility = 5 #defaults to 5 until a use is constructed
    ship.current_total_points_all += mobility
    print "Mobility defaults to 5 in the current build"
    print 'You have {} remaining points'.format(Ship.total_points_all - ship.current_total_points_all)
    accuracy = input_controls(accuracy, ship)
    capacitor = input_controls(capacitor, ship)
    count = 0
    if ship.current_total_points_all<Ship.total_points_all:
        print Ship.total_points_all
        valid = False
        if count > 0:
            if ship.current_total_points_all < Ship.total_points_all:
                valid = True
        while not valid:
            if input('You have not used up all available points. Choose 1 to continue or 2 to start over.')==1:
                valid = True
            else:
                ship.current_total_points_all = 0
                max_attack = {'max_attack': []}
                weapon_type = {'weapon type': []}
                defense = {'defense': []}
                mobility = {'mobility': []}
                accuracy = {'accuracy': []}
                capacitor = {'capacitor': []}
                weapon_type = input_controls(weapon_type, ship)
                # max_attack = input_controls(max_attack, ship)
                defense = input_controls(defense, ship)
                # mobility = input_controls(mobility, ship)
                mobility = 5
                print "Mobility defaults to 5 in the current build"
                ship.current_total_points_all += mobility
                accuracy = input_controls(accuracy, ship)
                capacitor = input_controls(capacitor, ship)
                count+=1
                valid = True
    ship.grow(defense, mobility, accuracy, capacitor, signature)
    ship.signature = float((ship.max_attack + defense + mobility + accuracy + capacitor) / float(ship.total_points_all))

def set_ship_design_auto(ship):
    current_total_points_all = 0
    max_attack = {'max_attack': []}
    defense = {'defense': []}
    mobility = {'mobility': []}
    accuracy = {'accuracy': []}
    capacitor = {'capacitor': []}
    signature = {'signature': []}
    trait_ideal_min = 5
    max_attack = random.randrange(5,Ship.total_points_per)
    ship.current_total_points_all+=max_attack
    #will want to eventually clean all this up and provide listening variables
    remaining_points = Ship.total_points_all - ship.current_total_points_all
    randrange_low = trait_ideal_min if trait_ideal_min <= remaining_points else remaining_points
    randrange_high = ship.current_total_points_all if ship.current_total_points_all<Ship.total_points_per else Ship.total_points_per
    # print 'current total poitns all', ship.current_total_points_all
    # print 'high',randrange_high
    # print 'low',randrange_low
    try:
        # defense = random.randrange(randrange_low,randrange_high)
        defense = 10
    except:
        try:
            defense = random.randrange(randrange_low, randrange_high)
        except:
            defense = randrange_low
    ship.current_total_points_all += defense
    remaining_points = Ship.total_points_all - ship.current_total_points_all
    randrange_low = trait_ideal_min if trait_ideal_min <= remaining_points else remaining_points
    randrange_high = ship.current_total_points_all if ship.current_total_points_all < Ship.total_points_per else Ship.total_points_per
    mobility = 5
    ship.current_total_points_all += mobility
    remaining_points = Ship.total_points_all - ship.current_total_points_all
    randrange_low = trait_ideal_min if trait_ideal_min <= remaining_points else remaining_points
    randrange_high = ship.current_total_points_all if ship.current_total_points_all < Ship.total_points_per else Ship.total_points_per
    try:
        accuracy = random.randrange(randrange_low,randrange_high)
    except:
        accuracy = randrange_low
    ship.current_total_points_all += accuracy
    remaining_points = Ship.total_points_all - ship.current_total_points_all
    ai_prefer_sigtank = random.randrange(0,1) #50/50 chance that the AI will prefer a lower cap in return for a lower signature. Otherwise, he will max out his cap
    if ai_prefer_sigtank == 1:
        randrange_low = trait_ideal_min if trait_ideal_min <= remaining_points else remaining_points
        randrange_high = ship.current_total_points_all if ship.current_total_points_all < Ship.total_points_per_capacitor else Ship.total_points_per_capacitor
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
                randrange_high = ship.current_total_points_all if ship.current_total_points_all < Ship.total_points_per_capacitor else Ship.total_points_per_capacitor
                capacitor = random.randrange(randrange_low, randrange_high)
            except:
                capacitor = randrange_low
    ship.current_total_points_all += capacitor
    ship.grow(defense, mobility, accuracy, capacitor, signature)
    ship.signature = float((max_attack + defense + mobility + accuracy + capacitor) / float(ship.total_points_all))




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
                        print Fore.RED + "{}'s powered his guns to the max!".format(ship2.ship_name)
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
        # print 'AI ATTACK STRIKE', attack_strike
        return attack_strike
    for_combat_log = [[]]
    if len(player_2_state)==0:
        player_2_state.append((int(input(str("Press 1 if Player 2 is Human, or 2 if a Computer")))))
    valid = False
    while not valid:
        ship_list = ship1,ship2
        attacking_ship = 0
        #This is the combat loop that plays out until one ship's defenses are reduced to 0
        while ship1.defense > 0 and ship2.defense > 0:
            if attacking_ship == 0:
                defending_ship = 1
            else:
                defending_ship = 0
            #set max_attack to either max_attack or capacitor, whichever is smallest
            if ship_list[attacking_ship].max_attack <= ship_list[attacking_ship].capacitor:
                max_attack = ship_list[attacking_ship].max_attack
            else:
                max_attack = ship_list[attacking_ship].capacitor
            if attacking_ship==0 or attacking_ship==1 and player_2_state[0]==1:
                if ship_list[attacking_ship].capacitor > 0: #Ships cannot fire if cap has been reduced to 0
                    valid2 = False
                    while not valid2:
                        try:
                            current_weapon = (raw_input('{}, equip your weapon, choices are: {}.'.format(ship_list[attacking_ship].ship_name,ship_list[attacking_ship].weapon_types)))
                            if current_weapon in ship_list[attacking_ship].weapon_types:
                                valid2 = True
                                current_weapon_equip = my_weapon_class_dict.get(current_weapon)  # tie in selection with the pertinent data from the selected weapon class
                                current_weapon_equip = current_weapon_equip.weapon_dict.get('attack power')
                                valid3 = False
                                while not valid3:
                                    try:
                                        attack_strike = int(input(Fore.GREEN + '{}, you have equipped your {}. Enter your '
                                                                               'attack amount, max {}: '.format(ship_list[attacking_ship].ship_name,current_weapon,current_weapon_equip)))
                                        if attack_strike<=max_attack:
                                            valid3 = True
                                    except:
                                        'That was not a valid input, try again'
                                max_attack = current_weapon_equip

                        except NameError:
                            print Fore.GREEN + 'That was not a valid input, try again'

                    #the following loop ensures a valid max_attack is input before continuing
                    while attack_strike > ship_list[attacking_ship].max_attack or attack_strike > ship_list[attacking_ship].capacitor:
                        if attack_strike > ship_list[attacking_ship].max_attack:
                            print Fore.RED + 'Your order exceeds our designed max_attack power, try again!'
                        elif attack_strike > ship_list[attacking_ship].capacitor:
                            print Fore.RED + 'You do not have enough remaining capacitor energy, try again!'
                        attack_strike = int(input(Fore.GREEN + '{}, enter your max_attack amount: '.format(ship_list[attacking_ship].ship_name)))
                    attack_result = attack_power(ship_list[attacking_ship],ship_list[defending_ship],attack_strike)
                    attack_result = attack_result[0]
                    valid = True
                    if attack_result > 0:  # if the max_attack did not miss
                        ship2.defense -= attack_result
                    if ship1.capacitor > 0:
                        ship1.capacitor -= attack_strike
                    Ship.capacitor_recharge = random.randrange(2,4)#capacitor will recharge within this range each round
                    ship1.capacitor += Ship.capacitor_recharge
                else:
                    print Fore.RED + "{} cannot make an max_attack, as his capacitor is completely drained".format(ship_list[attacking_ship].ship_name)
                    Ship.capacitor_recharge = random.randrange(2, 4)
                    ship1.capacitor += Ship.capacitor_recharge
            # Checks if player 2 is a human or computer. If computer, initializes AI actions
            elif attacking_ship == 1:  # if the attacker is player 2
                if player_2_state[0] == 2:  # if player 2 is a computer
                    try:
                        attack_strike = ai_logic(ship1,ship2)
                        print '*utilizing comprehensive AI logic*'
                    except:
                        print '*utilizing simplified AI logic*'
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
                    ship1.defense -= attack_result
                ship2.capacitor -= attack_strike
                Ship.capacitor_recharge = random.randrange(2, 4)
                ship2.capacitor += Ship.capacitor_recharge
            if attacking_ship == 0:
                attacking_ship = 1
            elif attacking_ship == 1:
                attacking_ship = 0
            print '**'
            justified_reports(ship1, ship2)
            print '**'
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
        print ""
        print Back.BLUE + "Congratulations mighty {}, you have won the battle! {}'s broken hull" \
              " now lay in the black of space for all eternity. Might this be a lesson " \
              "to all who dare to oppose you.".format(ship_list[ship_win].ship_name, ship_list[ship_lose].ship_name)
        valid = True

'''---------------------------Menu management area---------------------------'''


def justified_reports(ship1, ship2):
    #Fix the columns and justification of ship reports
    report_1 = ship1.report()
    report_2 = ship2.report()
    col_width = max(len(str(word)) for row in report_1.items() for word in row) + 1  # padding
    for row, row2 in zip(report_1.items(), report_2.items()):
        print "".join(str(word).ljust(col_width) for word in row), ' ', "".join(
            str(word).ljust(col_width) for word in row2)
    print ''

def display_menu():
    print Back.GREEN + "Welcome to the TI3 Tactical Simulator!"
    ti3_logo = logo_style()
    print ti3_logo
    print '1. Craft ships'
    print "2. Read some tips"
    print "3. [Placeholder]"
    print "4. Commence battle"
    print "5. View current ship reports"
    print "6. Set Player 2 to Human or Computer"
    print "0. Exit the tactical simulator program"
    print ""
    print Style.BRIGHT + "Please select an option from the above menu"

def get_menu_choice():
    option_valid = False
    while not option_valid: #these two lines basically mean "until a valid option is entered, do this"
        try:
            choice = raw_input("Option Selected: ")
            if 0<= int(choice) <= 6:
                option_valid = True
            else:
                print Fore.RED + "Please enter a valid option"
        except ValueError:
            print Fore.RED + "Please enter a valid option"
    return int(choice)

computer_names = ['Locutus of Borg', 'Yoda', 'Merci of El Nath', 'Leviathan', "Ace's Evil Twin", "Tops's Evil Twin", "Spade's Evil Twin", "Hitler's Spawn"]

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
    print Back.BLUE + "This is a TI3-inspired tactical space combat simulator"
    print ""
    noexit = True
    while noexit:
        display_menu()
        option = get_menu_choice()
        print ""
        if option == 1:
            #if fighting more than 1 battle per program execution, reset previous values
            reset_ships(ship1)
            reset_ships(ship2)
            name = raw_input(str(Back.CYAN + "What is the name of player 1? "))
            ship1.ship_name = name
            set_ship_design(ship1)
            print ""
            justified_reports(ship1, ship2)
            print ""
            #if set to 2, auto select name and call function to auto set attributes
            p2_manual_auto = raw_input(str(Back.CYAN + "Press 1 to manually set opposing player traits, or 2 to auto generate them"))
            if p2_manual_auto==1:
                name = raw_input(str(Back.CYAN + "What is the name of player 2? "))
                ship2.ship_name = name
                set_ship_design(ship2)
            else:
                name = computer_names[random.randrange(0,len(computer_names))]
                ship2.ship_name = name
                set_ship_design_auto(ship2)
            print ""
            justified_reports(ship1, ship2)
            print ""

        elif option == 2:
            tips_simple()
            print ""
        elif option == 3:
            print Fore.RED + "This is a work in progress and has not yet been implemented"
            print ''
        elif option == 4: #commence battle
            combat(ship_1, ship_2)
            # print "This is a work in progress and has not yet been implemented"
            print ''
        elif option == 5:
            justified_reports(ship1,ship2)
        elif option == 6:
            player_2_state.append(int(input(str("Press 1 if Player 2 is Human, or 2 if a Computer"))))
            print ""
        elif option == 0:
            noexit = False
            print ""
    print Fore.BLUE + Back.WHITE + "Thank you for using the tactical space combat simulator"

def main():
    #instantiate the class
    # ship_1 = Ship(0,0,0,0,0)
    # set_ship_design(ship_1)
    manage_ships(ship_1, ship_2)
    print Ship.num_of_ships

if __name__ == "__main__":
    main()