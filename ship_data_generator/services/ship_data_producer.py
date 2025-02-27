import json
import confluent_kafka
from services import ShipDataStatus

class ShipDataProducer:
    def __init__(self):
        self.producer = confluent_kafka.Producer({
            'bootstrap.servers': 'localhost:9092',
            'message.send.max.retries': 3,
            'retry.backoff.ms': 30000
        })
        self.retry_count = {}
        self.status = ShipDataStatus()

    def ship_data_sending(self, ship_data):
        self.producer.produce(topic='ships', value=ship_data, callback=self.waiting_answer)
        self.status.save_new_data(ship_data)
        self.producer.flush()

    def waiting_answer(self, err, msg):
        imo = json.loads(msg.value().decode('utf-8'))['imo']
        if err:
            self.retry_count[imo] = self.retry_count.get(imo, 0) + 1
            self.status.change_status(imo, err)
            if self.retry_count[imo] > 2:
                self.status.move_to_dead_storage(imo)
        else:
            self.status.change_status(imo, "Successfully sent to Kafka.")
            self.retry_count.pop(imo, None)