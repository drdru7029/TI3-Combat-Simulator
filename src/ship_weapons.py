# from ship_class_b import *
# from shapely.geometry import Point

#The weapon 'outputs' will be the actual attack value, a value that determines capacitor drain, and a value that
#indicates whether damage can be spread to multiple subsystems, or focused onto one.

#Define the primary weapon class
class Weapon:
    """A weapon prototype blueprint"""


    total_weapon_attack_power = 10 #the highest designed attack power for this type of weapon
    weapon_capacitor_drain = 1 # some weapons will drain more or less than the damage they project
    weapon_size = 1 #this will be used to limit the type of weapon that can be installed on a given ship type
    focused_damage = 0 #1 if damage will focus on one subsystem; 0 if it will be spread. The default class value is 0.

    def __init__(self, weapon_attack=10, weapon_health=1, weapon_status=1):
        # self.weapon_attack = weapon_attack
        self.weapon_health = weapon_health
        self.weapon_status = weapon_status

    def weapon_dict2(self):
        #indeed, this method only needs to exist at the master class level. how wonderful!
        class_dict = {'power': self.total_weapon_attack_power,'cap drain': self.weapon_capacitor_drain, 'focused damage': self.focused_damage}
        # print(weapon_dict
        return class_dict

    class_dict = {'identifier': 'laser parent', 'power': total_weapon_attack_power, 'capacitor drain': weapon_capacitor_drain, 'size': weapon_size,
                  'focused damage': focused_damage}

#Define the major weapon subclasses
class Laser(Weapon):
    """An energy weapon template"""

    # class_dict = 'weapon laser parent'

    def __init__(self):
        super().__init__()

    focused_damage = 1

    def cap_drain_effect(self, ship):
        if ship.capacitor<=0:
            self.weapon_status = 0
        elif ship.capacitor>0:
            self.weapon_status = 1

    def focused_damage_accuracy(self):
        #if weapon health drops below half (.5), it loses the ability to selectively focus damage,
        #and subsequent attacks will apply the focused damage to a randomly selected subsystem
        if self.weapon_health <.5 :
            select_focused_damage_ability = 0
        else:
            select_focused_damage_ability = 1
        return select_focused_damage_ability

    class_dict = {'identifier': 'laser parent', 'power': Weapon.total_weapon_attack_power, 'capacitor drain': Weapon.weapon_capacitor_drain,
                  'size': Weapon.weapon_size, 'focused damage': focused_damage}


class Torpedo(Weapon):
    """A projectile weapon template"""

    def __init__(self):
        super().__init__()
        #Note, only 'new' (i.e. specific to this child class) attributes should be added here as self.newatt = x

    total_weapon_attack_power = 6 #Healthy Torpedo damage should be fixed at its total value

    # class_dict = {'power': total_weapon_attack_power}

    def cap_drain_effect(self, ship):
        #a torpedo weapon will still function during complete cap loss,but at 50% effectiveness
        if ship.capacitor<=0:
            ship.attack = ship.attack*.5
        elif ship.capacitor>0:
            ship.attack = ship.attack*1

    def damage_application_strength(self, ship):
        # if torpedo weapon health drops below half (.6), damage application drops by 15% per .1 loss in health
        strength_reduction_threshold = .6
        if self.weapon_health <= strength_reduction_threshold:
            strength_reduction = self.weapon_health / .1
            strength_reduction = .15 * ((strength_reduction_threshold*10)-strength_reduction)
            print('strength_reduction: ', 1-strength_reduction)
            ship.attack = ship.attack * (1-strength_reduction)

    class_dict = {'identifier': 'torpedo parent', 'power': total_weapon_attack_power,
                  'capacitor drain': Weapon.weapon_capacitor_drain,
                  'size': Weapon.weapon_size, 'focused damage': Weapon.focused_damage}

    def apply_basic_ship_attributes(self, ship):
        ship.max_attack = self.class_dict['power']




#Define the children of each major subclass
class BeamLaser(Laser):
    """A lower-powered weapon that specializes in focused attacks, and is weakly capacitor-dependant"""

    def __init__(self):
        super().__init__()

    total_weapon_attack_power = 6
    weapon_capacitor_drain = 0.8

    class_dict = {'identifier': 'beam laser', 'power': total_weapon_attack_power,
                  'size': Laser.weapon_size, 'capacitor drain': weapon_capacitor_drain,
                  'focused damage': Laser.focused_damage}

class PulseLaser(Laser):
    """A higher-powered weapon that specializes in focused attacks, and is strongly capacitor-dependant"""

    # Laser.weapon_capacitor_drain = 1.2

    def __init__(self):
        super().__init__()

    weapon_capacitor_drain = 1.2 #how to connect this to the action?

    class_dict = {'identifier': 'pulse laser', 'power': Laser.total_weapon_attack_power,
                  'size': Laser.weapon_size, 'focused damage': Laser.focused_damage,
                  'capacitor drain': weapon_capacitor_drain,}

    def apply_basic_ship_attributes(self, ship):

        """The function where any special properties related to the parent/child class are triggered to be sent to
        the ship upon construction."""

        print('applying basic ship attributes.', ship.max_attack, self.class_dict['power'])
        if ship.max_attack < self.class_dict['power']:
            ship.max_attack = self.class_dict['power']
        else:
            ship.min_attack = self.class_dict['power']


# Dictionary of weapon subclasses to associate with user input
my_weapon_class_dict = {'beam laser': BeamLaser, 'pulse laser': PulseLaser, 'torpedo': Torpedo}


# mytest = my_weapon_class_dict.get('pulse laser')
#
# print('Pulse_laser_all', mytest.class_dict)
#
# workingtest = mytest.class_dict.get('power')
#
# print('Pulse_laser_focused_damage',PulseLaser.focused_damage)
# print('Pulse_laser_cap_drain',PulseLaser.weapon_capacitor_drain)
#
#
# print('Laser_cap_drain',Laser.weapon_capacitor_drain)
# print('Weapon_focused_damage', Weapon.focused_damage)


# mytestb = mytest.weapon_dict2()


# mytorp = mytest()
# mytest2 = mytorp.weapon_dict2()
#
# print(workingtest)
# print(mytest2)

# new_attribute = my_weapon_class_dict.get(new_attribute) #tie in selection with the pertinent data from the selected weapon class
# new_attribute = new_attribute.weapon_dict.get('power') #grab the value of the input
# new_weapon_attribute_values = [new_attribute]

###TESTING BELOW###

# print(Torpedo.weapon_capacitor_drain
# # print(Torpedo.weapon_dict.get('cap drain')
# #so, the following illustrates how to call class attributes from the ground up,
# # without having to specify child or parent classes first
# mytorp = Torpedo(10,1,1)
# mylaser = PulseLaser(10,1,1)
# mytorpdict = mytorp.weapon_dict2()
# print(mytorpdict.get('cap drain')
# print(mytorpdict
# mylaserdict = mylaser.weapon_dict2()
# print(mylaserdict

# ace_beam_laser = BeamLaser(10,1,1)
# ace_torpedo = Torpedo(10,1,1)
#
# ship_1.capacitor = 10
# #test changing the ship's capacitor
# ace_torpedo.weapon_health = .3
# ace_beam_laser.cap_drain_effect(ship_1) #apply the Laser class's cap drain effect
# print(ace_beam_laser.weapon_status #check to make sure the weapon status is correctly modified
# ship_1.attack = 10
# ace_torpedo.damage_application_strength(ship_1)
# print('torpedo damage', ship_1.attack
#
# my_function = lambda a, b : a + b
# print(my_function(1, 2)
#
# #example of how to make a Shapely point
# patch = Point(0.0,0.0).buffer(10.0)
# print(patch.area

#example of how to use user input to access class attributes
# new_attribute = raw_input("enter data")
# #
# weapon_choice = my_weapon_class_dict.get(new_attribute)
# print(weapon_choice.weapon_dict.get('cap drain')
