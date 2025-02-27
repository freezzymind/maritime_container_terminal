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

    def show_storage(self):
        pass

    def del_storage_obj(self):
        pass

    def move_to_dead_storage(self, imo):
        self.dead_storage[imo] = self.storage[imo]
        self.storage.pop(imo, None)

    def show_dead_storage(self):
        pass

    def del_dead_storage_obj(self):
        pass

    def clean_dead_storage(self):
        pass

#Принять запись о корабле с неизвестным статусом отправки
#Менять статус в соответствии с новыми данными
#В случае необходимости - показывать эти записи
#При получении статуса о том что корабль записан в БД - удалять его
#При трехкратном повторении одной и той же ошибки - переводить записи в другую таблицу
#Сообщать продюсеру, чтобы больше не пытался отправлять
#Сообщать менеджеру чтобы уведомлял юзера и предлагал попробовать снова или изучить проблему
