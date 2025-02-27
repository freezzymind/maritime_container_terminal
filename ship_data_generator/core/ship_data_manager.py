from data_engine import Automatically, Manually
from services import ShipDataFormatter, ShipDataProducer

class Manager:
    def __init__(self):
        self.answer = ''
        self.ship_data = {}
        self.formatter = ShipDataFormatter()
        self.producer = ShipDataProducer()

    def get_answer(self):
        while True:
            self.answer = input('Type "1" if you want to save your own data,\n \
                           or type "2" if you want to generate it automatically.')
            if self.answer in ('1', '2'):
                break
            else:
                print('It`s wrong! Use only "1" or "2" for the answer.\n')

    def get_ship_data(self):
        generator = Manually() if self.answer == '1' else Automatically()
        self.ship_data = generator.get_params()
        self.ship_data = self.formatter.json_format(self.ship_data)

    def send_ship_data(self):
        self.producer.ship_data_sending(self.ship_data)
        print('Your ship_data was sent.')

    def show_status(self):
        self.answer = input("Type '1' to view failed entries (final_error list) \n"
                            "or type '2' to view active entries (in process). ")
        if self.answer == '1':
            for imo, data in self.producer.status.dead_storage.items():
                print(f"IMO: {imo}, Status: {data['status']}")

        elif self.answer == '2':
            for imo, data in self.producer.status.storage.items():
                print(f"IMO: {imo}, Status: {data['status']}")

    def clean_storage(self):
        pass

    def del_selected_entry(self):
        pass

    def main_menu(self):
        print('Hello, and welcome to the ship_data_generator system.\n')
        while True:
            command = input("Type '1' for continuing or type '2' for exiting: \n")
            if command == '1':
                self.get_answer()
                self.get_ship_data()
                self.send_ship_data()
                self.show_status()
            elif command == '2':
                print("Exiting program...")
                exit(0)
            else:
                print("Use only '1' or '2' for input.")







