import math

from consts import KAFKA_RETENTION, KAFKA_BROKER_MAXIMUM_THROUGHPUT
from resources.base import BaseResource


class KafkaResource(BaseResource):
    src_num_of_brokers: int
    dst_num_of_brokers: int
    src_cluster_storage: float
    dst_cluster_storage: float

    def __init__(self, src_num_of_brokers: int, dst_num_of_brokers: int, src_cluster_storage: float,
                 dst_cluster_storage: float) -> None:
        super().__init__(src_num_of_brokers=src_num_of_brokers,
                         dst_num_of_brokers=dst_num_of_brokers,
                         src_cluster_storage=src_cluster_storage,
                         dst_cluster_storage=dst_cluster_storage)

    def get_current_resource_throughput(self):
        storage_throughput: float = self.__get_storage_throughput()
        infrastructure_throughput: float = self.__get_infrastructure_throughput()
        return min(storage_throughput, infrastructure_throughput)

    def calculate_needed_resources(self, desired_throughput: float) -> BaseResource:
        needed_storage: float = KafkaResource.__get_kafka_storage_by_throughput(throughput=desired_throughput)
        needed_brokers: int = KafkaResource.__get_num_of_brokers_by_throughput(throughput=desired_throughput)
        return KafkaResource(src_cluster_storage=needed_storage, dst_cluster_storage=needed_storage,
                             src_num_of_brokers=needed_brokers, dst_num_of_brokers=needed_brokers)

    def get_missing_resources(self, desired_throughput: float) -> BaseResource:
        needed: BaseResource = self.calculate_needed_resources(desired_throughput)

        missing_src_brokers = max(0, needed.src_num_of_brokers - self.src_num_of_brokers)
        missing_dst_brokers = max(0, needed.dst_num_of_brokers - self.dst_num_of_brokers)
        missing_src_storage = max(0, needed.src_cluster_storage - self.src_cluster_storage)
        missing_dst_storage = max(0, needed.dst_cluster_storage - self.dst_cluster_storage)

        return KafkaResource(
            src_num_of_brokers=missing_src_brokers,
            dst_num_of_brokers=missing_dst_brokers,
            src_cluster_storage=missing_src_storage,
            dst_cluster_storage=missing_dst_storage
        )

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
        src_infrastructure_throughput: float = self.src_num_of_brokers * KAFKA_BROKER_MAXIMUM_THROUGHPUT
        dst_infrastructure_throughput: float = self.dst_num_of_brokers * KAFKA_BROKER_MAXIMUM_THROUGHPUT
        return min(src_infrastructure_throughput, dst_infrastructure_throughput)
