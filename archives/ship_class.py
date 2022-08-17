


class Ship:
    """A prototype ship type"""

    #constructor
    # def __init__(self,attack,defense,mobility,accuracy,total_points_all,total_points_per):
    _total_points_all = 25
    _total_points_per = 10
    def __init__(self):
        #set the attributes with their initial values

        self._damage = damage
        self._attack = attack
        self._defense = 0
        self._mobility = 0
        self._accuracy = 0
        self._current_total_points_all = 0
        self._status = "All systems go"

    #report on the current state of the ship
    def report(self):
        #return a dictionary containing all attributes
        return {'current damage':self._damage, 'attack':self._attack, 'defense':self._defense,'mobility':self._mobility,
                'accuracy':self._accuracy, 'current total points':self._current_total_points_all,'total points per system':self._total_points_per}

    def update_status(self):
        if self._defense - self._damage <= 7:
            self._status = "We have sustained minor damage"
        elif self._defense - self._damage <= 5:
            self._status = "We have sustained moderate damage"
        elif self._defense - self._damage <= 3:
            self._status = "We have sustained heavy damage"
        elif self._defense - self._damage <= 2:
            self._status = "We have sustained critical damage and are at risk of total systems failure!"
        else:
            self._status = "All systems go"

    #lesson: this 'grow' method is critical in being able to record values from the subsequent functions
    def grow(self, attack, defense, mobility, accuracy):
        self._attack = attack
        self._defense = defense
        self._mobility = mobility
        self._accuracy = accuracy

'''THE BIG PROBLEM IS HERE, NEED TO FIND A WAY TO 1) CHECK INSTANCE VARIABLE FOR CURRENT TOTALS, AND 2)'''
'''MAKE THE LOGIC WORK FOR TESTING IF CAPACITY HAS BEEN BREACHED'''
def input_controls(attribute):
    #allow the user to input the initial design
    current_totals_pre = 0
    current_totals_post = 0
    valid = False
    while not valid:
        try:
            new_attribute = input("Enter your {} value up to {}: ".format(attribute.keys(), Ship._total_points_per))
            current_totals_pre+=int(new_attribute)
            if 1 <= new_attribute <= Ship._total_points_per and new_attribute <= current_totals_pre:
                valid = True
                current_totals_post+=new_attribute
            else:
                print "Value entered is not valid - please enter a value between 1 and {}: ".format(Ship._total_points_per)
        except ValueError:
            "Value entered is not valid - please enter a value between 1 and {}: ".format(Ship._total_points_per)
    valid = False
    new_attribute = int(new_attribute)
    return new_attribute

def set_ship_design(ship):
    # #allow the user to input the initial design
    attack = {'attack': []}
    defense = {'defense': []}
    mobility = {'mobility': []}
    accuracy = {'accuracy': []}
    attack = input_controls(attack)
    defense = input_controls(defense)
    mobility = input_controls(mobility)
    accuracy = input_controls(accuracy)

    ship.grow(attack,defense, mobility, accuracy)


def main():
    #instantiate the class
    new_ship = Ship()
    set_ship_design(new_ship)
    print new_ship.report()

if __name__ == "__main__":
    main()