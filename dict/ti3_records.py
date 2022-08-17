from main_run import *
import os

def record_battle_history(battle_results):
    #creates a folder called TI3 Tactical in the Users folder if necessary
    #writes battle results to the CSV
    home_dir = os.path.expanduser("~")
    program_folder = "\TI3 Tactical"
    home_dir = home_dir+program_folder
    if not os.path.exists(home_dir):
        os.makedirs(home_dir)
    battle_results_file = '\combat_records.csv'
    home_dir = home_dir+battle_results_file
    with open(home_dir,'a',newline="") as fp:
        a = csv.writer(fp,delimiter=',')
        data = battle_results
        with open(home_dir,'r',newline="") as reading:
            b = csv.reader(reading,delimiter=',')
            headers = ['You','Opponent']
            first_time_write = [headers,data]
            print('first_time_write',first_time_write)
            if headers in b:
                a.writerow(data)
            else:
                a.writerows(first_time_write)


# combat = [100,200]
# #
# record_battle_history(combat)


#for later, when I understand conditional csv writing more. will need to use csv.DictReader/Writer
# headers = ['a', 'b', 'd', 'g']
#
# with open('in.csv', 'rb') as _in, open('out.csv', 'wb') as out:
#     reader = csv.DictReader(_in)
#     writer = csv.DictWriter(out, headers, extrasaction='ignore')
#     writer.writeheader()
#     for line in reader:
#         writer.writerow(line)

# if data[0][0] in b: #if player 1 is in the sheet
#     if data[0][1] in b: #if player 2 is also in the sheet, then just write the results
#         a.writerow(data[1])
#     else:
#         a.writerow(data[0][1],data[1])
# else:
#     if data[0][1] in b:
#         a.writerow(data[0][0],data[1])
#     else:
#         a.writerows(data)