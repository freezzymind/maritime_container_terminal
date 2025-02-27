import json

class ShipDataStatus:
    def __init__(self):
        self.storage = {}
        self.dead_storage = {}

    def save_new_data(self, ship_data):
        ship_data = json.loads(ship_data).decode('utf-8')
        ship_data['status'] = "Sending to Kafka."
        self.storage[ship_data['imo']] = ship_data

    def change_status(self, imo, current_status):
        if imo in self.storage:
            self.storage[imo]["status"] = current_status

    def move_to_dead_storage(self, imo):
        self.dead_storage[imo] = self.storage[imo]
        self.storage.pop(imo, None)

    def del_storage_obj(self, imo):
        return self.storage.pop(f'DELETED {imo}.', "Imo-number not found")

    def del_dead_storage_obj(self, imo):
        return self.dead_storage.pop(f'DELETED {imo}.', "Imo-number not found")

    def clean_storage(self):
        self.storage.clear()

    def clean_dead_storage(self):
        self.dead_storage.clear()


