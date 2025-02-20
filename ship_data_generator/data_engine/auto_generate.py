import random
import pandas


class Automatically:  # Initializes the class. Creates an empty dictionary ship_params and fills it by calling generation methods.
    def __init__(self):
        self.ship_params = {}
        self.get_ship_name()
        self.get_imo_number()
        self.get_ship_flag()
        self.get_ship_tech_params()

    def get_ship_name(self):  # Generates a random ship name by selecting it from a CSV file with names.
        ship_names = pandas.read_csv('../data_storage/ship_names.csv', encoding='utf-8', header=None).squeeze('columns').tolist()
        self.ship_params['name'] = random.choice(ship_names)

    def get_imo_number(self):  # Generates a random IMO number for the ship using a standard formula.
        imo = []
        checker = []
        for num in range(7, 1, -1):
            number = random.randint(1, 9)
            checker.append(num * number)
            imo.append(number)
        imo.append(sum(checker) % 10)
        self.ship_params['imo'] = ''.join(map(str, imo))

    def get_ship_flag(self):  # Selects a random ship flag from a CSV file containing a list of flags.
        ship_flags = pandas.read_csv('../data_storage/ship_flags.csv', header=None).squeeze('columns').tolist()
        self.ship_params['flag'] = random.choice(ship_flags)

    def get_ship_tech_params(self):  # Generates random technical parameters for the ship by selecting values from a CSV file.
        ship_params = pandas.read_csv('../data_storage/ship_params.csv').to_dict(orient='list')
        index = random.randint(0, 990)
        self.ship_params.update({key: value[index] for key, value in ship_params.items()})

    def get_params(self):
        return self.ship_params


if __name__ == "__main__":
    vessel_data = Automatically()
    print("\nVessel summary data_storage:", vessel_data.get_params())
