import math

from consts import KAFKA_RETENTION, KAFKA_BROKER_MAXIMUM_THROUGHPUT
from resources.base import BaseResource


class KafkaResource(BaseResource):
    num_of_brokers: int
    src_cluster_storage: float
    dst_cluster_storage: float

    def __init__(self, num_of_brokers: int, src_cluster_storage: float, dst_cluster_storage: float) -> None:
        super().__init__(num_of_brokers=num_of_brokers,
                         src_cluster_storage=src_cluster_storage,
                         dst_cluster_storage=dst_cluster_storage)

    def calculate_needed_resources(self, desired_throughput: float) -> BaseResource:
        needed_storage: float = KafkaResource.__get_kafka_storage_by_throughput(throughput=desired_throughput)
        needed_brokers: int = KafkaResource.__get_num_of_brokers_by_throughput(throughput=desired_throughput)
        return KafkaResource(src_cluster_storage=needed_storage, dst_cluster_storage=needed_storage,
                             num_of_brokers=needed_brokers)

    @staticmethod
    def __get_num_of_brokers_by_throughput(throughput: float) -> int:
        return math.ceil(throughput / KAFKA_BROKER_MAXIMUM_THROUGHPUT)

    @staticmethod
    def __get_kafka_storage_by_throughput(throughput: float) -> float:
        return throughput * KAFKA_RETENTION

    def __get_storage_throughput(self) -> float:
        src_cluster_storage_throughput: float = self.src_cluster_storage / KAFKA_RETENTION
        dst_cluster_storage_throughput: float = self.dst_cluster_storage / KAFKA_RETENTION
        return min(src_cluster_storage_throughput, dst_cluster_storage_throughput)

    def __get_infrastructure_throughput(self) -> float:
        return self.num_of_brokers * KAFKA_BROKER_MAXIMUM_THROUGHPUT

    def get_current_resource_throughput(self):
        storage_throughput: float = self.__get_storage_throughput()
        infrastructure_throughput: float = self.__get_infrastructure_throughput()
        return min(storage_throughput, infrastructure_throughput)
