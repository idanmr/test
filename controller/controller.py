from typing import List

from resources.base import BaseResource
from resources.kafka import KafkaResource
from resources.nifi import NifiResource
from sampler.victoria_metrics import VictoriaMetricsAPI


class Controller:
    def __init__(self, desired_throughput: float):
        self.desired_throughput = desired_throughput
        self.resource_list: List[BaseResource] = [Controller.get_kafka_resource()]

    def calculate_needed_resources(self) -> List[BaseResource]:
        needed_resource_list: List[BaseResource] = []
        for resource in self.resource_list:
            needed_resource_list.append(resource.calculate_needed_resources(self.desired_throughput))
        return needed_resource_list

    def get_current_resources(self) -> List[BaseResource]:
        return self.resource_list

    def get_missing_resources(self) -> List[BaseResource]:
        missing_resource_list: List[BaseResource] = []
        for resource in self.resource_list:
            missing_resource_list.append(resource.get_missing_resources(desired_throughput=self.desired_throughput))
        return missing_resource_list

    @staticmethod
    def get_kafka_resource() -> KafkaResource:
        src_cluster_storage: float = VictoriaMetricsAPI.get_src_kafka_storage()
        dst_cluster_storage: float = VictoriaMetricsAPI.get_dst_kafka_storage()
        src_num_of_brokers: int = VictoriaMetricsAPI.get_src_number_of_brokers()
        dst_num_of_brokers: int = VictoriaMetricsAPI.get_dst_number_of_brokers()
        return KafkaResource(src_cluster_storage=src_cluster_storage, dst_cluster_storage=dst_cluster_storage,
                             src_num_of_brokers=src_num_of_brokers, dst_num_of_brokers=dst_num_of_brokers)

    def get_nifi_resource(self) -> NifiResource:
        pass
