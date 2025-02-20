import random
import pandas
import time


class Manually:
    def __init__(self):  # Initialize manual data_storage entry mode
        print('Manual data_storage entry mode activated. Please fill in the ship information.')
        self.ship_params = {}
        self.get_ship_name()
        self.get_imo_number()
        self.get_ship_flag()
        self.get_ship_tech_params()

    def get_ship_name(self):  # Prompt user for ship name input
        self.ship_params['name'] = input('Enter the ship name (up to 100 characters): ')
        print(f'The name "{self.ship_params["name"]}" has been successfully saved.')

    def get_imo_number(self): # Prompt user for IMO number and validate or generate automatically
        answer = None
        print('\nPlease provide the IMO number of the ship.')
        print('\nThe IMO number will be validated according to SOLAS XI-1/3.')
        print('\nYou can also generate a valid IMO number using the program.')

        while answer not in ('1', '2'):
            answer = input('\nEnter "1" to provide your own IMO number or "2" to generate it automatically: ').strip()

            if answer == '1':  # Manual entry of IMO number
                imo_number = input('\nEnter a 7-digit IMO number (numeric only) according to SOLAS XI-1/3: ').strip()
                print('\nValidating the number...')
                time.sleep(3)

                if imo_number.isdigit() and len(imo_number) == 7:  # Validate IMO number using checksum formula
                    checker = [int(imo_number[i]) * (7 - i) for i in range(6)]
                    control_digit = sum(checker) % 10
                    if control_digit == int(imo_number[-1]):
                        self.ship_params['imo'] = imo_number
                        print('\nThe IMO number has been validated and saved successfully.')
                    else:
                        print('\nError! The IMO number did not pass validation.')
                        answer = None
                else:
                    print('\nError! The IMO number must be 7 digits long.')
                    answer = None

            elif answer == '2':  # Automatically generate a valid IMO number
                print('\nAutomatically generating the IMO number...')
                time.sleep(1)
                print('\nGenerating...')
                time.sleep(2)

                imo = [random.randint(1, 9) for _ in range(6)]
                control_digit = sum(imo[i] * (7 - i) for i in range(6)) % 10
                imo.append(control_digit)

                self.ship_params['imo'] = ''.join(map(str, imo))
                print(f'\nGenerated IMO number {self.ship_params["imo"]} and saved successfully.')

            else:
                print('\nInvalid input. Please enter "1" or "2".')
                answer = None

    def get_ship_flag(self):  # Prompt user for country flag code
        print('\nEnter the country flag code under which the ship operates.')

        while True:
            selected_flag = input('\nUse three uppercase Latin letters (e.g., "USA"): ').strip()

            if not (selected_flag.isupper() and len(selected_flag) == 3 and selected_flag.isalpha()):
                print('\nError! The flag code must be 3 uppercase Latin letters (e.g., "USA").')
                continue

            ship_flags = pandas.read_csv('../data_storage/ship_flags.csv', header=None).squeeze('columns').tolist()

            if selected_flag not in ship_flags:
                print(f'\nFlag "{selected_flag}" not found in the list.')
                time.sleep(1)
                print('\nWould you like to add it to the list or enter another flag?')
                answer = input('\nEnter "1" to add the flag to the list.\n\
Enter "2" to provide a different flag.\n\
Enter "3" to select a random flag from the list: ').strip()

                if answer == '1':
                    pandas.DataFrame([[selected_flag]]).to_csv('../data_storage/ship_flags.csv', mode='a', index=False, header=False)
                    self.ship_params['flag'] = selected_flag
                    print(f'\nFlag "{selected_flag}" added to the list and saved successfully.')
                    break

                elif answer == '3':
                    selected_flag = random.choice(ship_flags)
                    self.ship_params['flag'] = selected_flag
                    print(f'\nRandomly selected flag "{selected_flag}" has been saved.')
                    break

                else:
                    continue

            else:
                self.ship_params['flag'] = selected_flag
                print(f'\nFlag "{selected_flag}" saved successfully.')
                break

    def get_ship_tech_params(self):  # Prompt user for ship technical specifications based on gross tonnage
        while True:
            try:
                answer = int(input('\nEnter the ship gross tonnage (between 1000 and 100000, step 100).\n\
The remaining characteristics will be automatically determined based on this value: '))
                if 1000 <= answer <= 100000 and answer % 100 == 0:
                    ship_params = pandas.read_csv('../data_storage/ship_params.csv')
                    index = (answer - 1000) // 100
                    ship_params = ship_params.iloc[index]
                    ship_params = ship_params.to_dict()
                    ship_params['gross_tonnage'] = int(ship_params['gross_tonnage'])
                    self.ship_params.update(ship_params)
                    break
                else:
                    print('\nError! Enter a number between 1000 and 100000 with a step of 100.')

            except ValueError:
                print('\nError! Please enter a numeric value.')

    def get_params(self):
        return self.ship_params


if __name__ == '__main__':
    vessel_data = Manually()
    print('\nVessel summary data_storage:', vessel_data.get_params())
