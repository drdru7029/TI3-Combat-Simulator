from ship_weapons import *
import ship_components as sc

class Ship:
    """A prototype ship type"""

    #constructor
    # def __init__(self,max_attack,defense,mobility,accuracy,total_points_all,total_points_per):
    total_points_all = 65
    total_points_per = 10
    total_points_per_capacitor = 20
    # capacitor_recharge = 3
    signature_modifier = 1
    num_of_ships = 0
    weapon_bays = 2
    weapon_options = my_weapon_class_dict #connects directly to ship_weapons.py
    shield_bays = 1
    shield_options = sc.my_component_class_dict['shields']
    capacitor_options = sc.my_component_class_dict['capacitor']
    accuracy_options = sc.my_component_class_dict['accuracy']
    defense_options = sc.my_component_class_dict['defense']
    mobility_options = sc.my_component_class_dict['mobility']
    instances = []

    attribute_dict = {'weapons': {'bay count': weapon_bays, 'options':weapon_options}, 'shields':
        {'bay count': shield_bays, 'options': shield_options}, 'capacitor':{'options':capacitor_options},
                      'accuracy': {'options': accuracy_options}, 'defense':{'options': defense_options},
                      'mobility':{'options': mobility_options}}

    def __init__(self, weapon_types, max_attack, min_attack, defense, mobility, accuracy, capacitor, signature,
                 current_total_points_all, ship_name, commander_name, damage, status, shields):
        #set the attributes with their initial values

        #Ship Attributes
        """Note: the concept of ship attributes will be moved from what are now final derived values, e.g. 'mobility',
        to individual components (like 'thrusters') which, based on their design characteristics, will derive attributes
        like 'mobility'.
        First up in this new shift will be 'shields', 'armor', and changing 'defense' to 'hull'. There will thus be
        three layers of 'defense' that will be treated individually."""

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
        self.commander_name = commander_name
        self.damage = 0
        self.status = "All systems go"
        self.shields = shields


        #Ship components


        Ship.instances.append(self)

        Ship.num_of_ships += 1


    def current_points(self):
        return self.current_total_points_all



    # def ship_components(self):
    #     self.weapon_types = {'weapon type': []}
    #     self.capacitor = {'capacitor': []}
    #     self.shields = {'shields': []}
    #     self.accuracy = {'accuracy': []}
    #     self.defense = {'defense': []}

    def ship_components(self, component_name, component_value):
        mydict = {'weapon type': self.weapon_types, 'capacitor' :self.capacitor, 'shields': self.shields,
        'accuracy': self.accuracy, 'defense': self.defense}

        for keys,values in mydict.items():
            if component_name==keys:
                values = component_value




        # constructable_components_dict = {weapon_types: {'weapon type': []}, capacitor: {'capacitor': []},
    #                                      shields: {'shields': []}, accuracy: {'accuracy': []}, defense: {'defense': []}}

        # for component, values in constructable_components_dict.items():
        #     ship.component = add_component(ship, component)


    #report on the current state of the ship
    def report(self):
        #return a dictionary containing all attributes
        ship_dictionary = {'current damage':self.damage, 'weapon type': self.weapon_types, 'max_attack':self.max_attack,
                           'min attack': self.min_attack,'defense':self.defense, 'mobility':self.mobility,
                'accuracy':self.accuracy, 'capacitor': self.capacitor, 'signature': self.signature, 'shields':self.shields,
                           'current total points':self.current_total_points_all,
                'total points per system':self.total_points_per, 'ship name': self.ship_name, 'commander name':self.commander_name}
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
    def grow(self, all_components,defense, mobility, accuracy, capacitor, signature):

        for component in all_components:
            self.component = component


        self.defense = defense
        self.mobility = mobility
        self.accuracy = accuracy
        self.capacitor = capacitor
        self.signature = float((self.max_attack + defense + mobility + accuracy + capacitor) / Ship.total_points_all)

    # ship_report = self.report()

# test = Ship(weapon_types=None, max_attack=0, min_attack=0, defense=0, mobility=0, accuracy=0, capacitor=0,
#                  signature=0, current_total_points_all=0, ship_name='Ship 1', commander_name=None, damage=0,
#                  status='all systems go', shields=None)
#
# for component in test.__dict__:
#     print(component)