from data_engine import Automatically, Manually
from services import ShipDataFormatter, ShipDataProducer

class Manager:
    def __init__(self):
        self.ship_data = {}
        self.formatter = ShipDataFormatter()
        self.producer = ShipDataProducer()

    def get_ship_data(self):
        command = input('Type "1" if you want to save your own data,\n \
                           or type "2" if you want to generate it automatically.')
        if command == '1':
            generator = Manually()
            self.ship_data = generator.get_params()
            self.ship_data = self.formatter.json_format(self.ship_data)
        elif command == '2':
            generator = Automatically()
            self.ship_data = generator.get_params()
            self.ship_data = self.formatter.json_format(self.ship_data)
        else:
            print('It`s wrong! Use only "1" or "2" for the answer.\n')
            self.get_ship_data()

    def send_ship_data(self):
        self.producer.ship_data_sending(self.ship_data)
        print('Your ship_data was sent in to the waiting list.')

    def show_status(self):
        while True:
            command = input("Type\n \
                            '1' to view failed entries (final_error list)\n \
                            '2' to view active entries (in process)\n \
                            '3' to back in the main_menu")

            if command == '1':
                for imo, data in self.producer.status.dead_storage.items():
                    print(f"IMO: {imo}, Status: {data['status']}")
                print()
                while True:
                    command = input("Type:\n \
                                    '1' for back in the main_menu\n \
                                    '2' for delete all from the dead_storage\n \
                                    '3' for delete entry by IMO\n")
                    if command == '1':
                        self.main_menu()
                    elif command == '2':
                        self.producer.status.clean_dead_storage()
                        self.main_menu()
                    elif command == '3':
                        imo = input()
                        result = self.producer.status.del_dead_storage_obj(imo)
                        print(result)
                        self.main_menu()
                    else:
                        print('It`s wrong! Use only "1", "2" or "3" for the answer.\n')

            elif command == '2':
                for imo, data in self.producer.status.storage.items():
                    print(f"IMO: {imo}, Status: {data['status']}")
                print()
                while True:
                    command = input("Type:\n \
                                    '1' for back in the main_menu\n \
                                    '2' for clear the storage\n \
                                    '3' for delete entry by IMO\n")
                    if command == '1':
                        self.main_menu()
                    elif command == '2':
                        self.producer.status.clean_storage()
                        self.main_menu()
                    elif command == '3':
                        imo = input()
                        result = self.producer.status.del_storage_obj(imo)
                        print(result)
                        self.main_menu()
                    else:
                        print('It`s wrong! Use only "1", "2" or "3" for the answer.\n')

            elif command == '3':
                self.main_menu()

            else:
                print('It`s wrong! Use only "1", "2" or "3" for the answer.\n')

    def main_menu(self):
        while True:
            command = input("Type:\n \
                            '1' for ship_data generate & send,\n \
                            '2' for exiting from the App,\n \
                            '3' for watching status of entries.\n")
            if command == '1':
                self.get_ship_data()
                self.send_ship_data()
            elif command == '2':
                print("Exiting program...")
                exit(0)
            elif command == '3':
                self.show_status()
            else:
                print("Use only '1', '2' or '3' for input.")

    def start(self):
        print('Hello, and welcome to the ship_data_generator system.\n')
        self.main_menu()





