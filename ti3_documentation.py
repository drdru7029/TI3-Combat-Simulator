from main_run import *

def tips_simple():
    print( Fore.LIGHTCYAN_EX + "SIMPLE TIPS BEFORE YOUR FIRST BATTLE:")
    print('')
    print( "The tactical simulation is continually evolving and being added to, but here is some current " \
          "pertinent info.")
    print( '')
    print( "Each ship is defined by several characteristics, and the only (currently) available ship class " \
          "allows a total power capacity of 45. Generally, you are able to allocate a maximum of 10 power per " \
          "subsystem, with some exceptions.")
    print( '')
    print( Fore.LIGHTCYAN_EX + "ATTACK: " + Fore.WHITE + "power limit: 10. This is probably your most important attribute, as it will define how much " \
          "firepower you can muster to the enemy. But be careful, as higher values carry higher risks and a broader " \
          "range of applied variability. Smaller values will have a greater chance of hitting the target and will vary " \
          "less in their applied damage. Also, be warned: attacking with very high power levels carry risks of damaging " \
          "other subsystems.")
    print( '')
    print( Fore.LIGHTCYAN_EX + "DEFENSE: "  + Fore.WHITE + "power limit: 10. After attack, this is the next most important attribute, defining how much damage " \
          "you can absorb before being destroyed. Once you hit 0, you're toast.")
    print( '')
    print( Fore.LIGHTCYAN_EX + "ACCURACY: " + Fore.WHITE +  "power limit: 10. Accuracy defines your chance of hitting your target with each shot. Higher accuracy " \
          "levels will improve (but not guarantee) landing a hit. Further, as mentioned above, extremely high applied attack " \
          "values will lessen your accuracy, while extremely low levels will improve it. You'll have to tackle a balance between " \
          "them.")
    print( '')
    print( Fore.LIGHTCYAN_EX + "MOBILITY: " + Fore.WHITE +  "power limit: 10. This will play a role soon but for now an auto-applied default of 5 is used.")
    print( '')
    print( Fore.LIGHTCYAN_EX + "CAPACITOR: "  + Fore.WHITE + "power limit 20. Currently the only subsystem with a power limit greater than 10. Regulates how much " \
          "attack power can be applied for any given shot. Attacks are strictly limited to their available capacitor, so " \
          "if you've drained it to 0, you won't be able to attack for that round. Capacitors will recharge at a certain " \
          "negligible rate each round. Note that your capacitor will drain by your INPUT attack amount, not your APPLIED " \
          "attack amount. So if you attack with a 10 and miss, your cap will still be drained by 10.")
    print( '')
    print( Fore.LIGHTCYAN_EX + "SIGNATURE: " + Fore.WHITE +  "This is a protected attribute that is modified based on the total value the power applied to all " \
          "subsystems. The value of all successful attacks on your ship will be modified by your ships signature as a " \
          "function of your total applied power divided by your ship class's total available power. So there may be" \
          "incentives, depending on your strategy, not to use all available points when crafting your ship.")
    print( "")
    print( Fore.LIGHTCYAN_EX + "Other pertinent info: ")
    print( "")
    print( Fore.WHITE + "You have the option to fight either a human opponent, or a computer. You'll find the option to set this" \
          "during the ship crafting phase. If you fight the computer, it's advised to let the AI auto-generate its" \
          "own characteristics (which will vary each fight). Be warned, the AI at this stage is a formidable opponent!")
    print( "")
    print( Fore.LIGHTCYAN_EX + "How to start: " + Fore.WHITE + "Choose 1: Craft Ships-->Set your name and attributes-->Allow " \
                                                              "Allow AI to auto-generate his own stats-->Back at the main " \
                                                              "Menu, choose 4: Commence battle-->Select '2' to play against " \
                                                              "the computer-->May the gods be with you!")
    print( "")
    print( Fore.LIGHTCYAN_EX + "COMBAT HISTORY TRACKING NOTE: " + Fore.WHITE + "The first time you run the program and finish a battle, " \
                                                                              "a folder called TI3 Tactical will be created in your Users " \
                                                                              "folder, along with a spreadsheet file (CSV) titled 'combat_records.csv' which will record " \
                                                                              "the results of each battle you fight. I plan to expand this greatly " \
                                                                              "to contain a great deal of stats (you know me), but it's simple for now.")