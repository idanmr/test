import math
from typing import List, Optional

from consts import stress_test_values_by_coin
from resources.base import BaseResource
from resources.kafka import KafkaResource
from resources.nifi import NifiResource
from sampler.prometheus import PrometheusAPI
from sampler.victoria_metrics import VictoriaMetricsAPI
from wallets.models import BaseCoin


class Controller:
    def __init__(self, desired_throughput: float, coin: BaseCoin):
        self.desired_throughput = desired_throughput
        self.coin = coin
        self.resource_list: List[BaseResource] = [self.__get_kafka_resource(), self.__get_nifi_resource()]

    def calculate_needed_resources(self) -> List[BaseResource]:
        needed_resource_list: List[BaseResource] = []
        for resource in self.resource_list:
            needed_resource_list.append(resource.calculate_needed_resources(self.desired_throughput))
        return needed_resource_list

    def get_current_throughput(self) -> float:
        min_throughput: float = math.inf
        for resource in self.resource_list:
            resource_throughput: float = resource.get_current_resource_throughput()
            if resource_throughput < min_throughput:
                min_throughput: float = resource_throughput
        return min_throughput

    def get_current_resources(self) -> List[BaseResource]:
        return self.resource_list

    def get_missing_resources(self) -> List[BaseResource]:
        missing_resource_list: List[BaseResource] = []
        for resource in self.resource_list:
            missing_resource_list.append(resource.get_missing_resources(desired_throughput=self.desired_throughput))
        return missing_resource_list

    def __get_kafka_resource(self) -> KafkaResource:
        src_cluster_storage: float = VictoriaMetricsAPI.get_kafka_storage(network=self.coin.src_network,
                                                                          cluster_name=self.coin.resources.src_kafka_cluster)
        dst_cluster_storage: float = VictoriaMetricsAPI.get_kafka_storage(network=self.coin.dst_network,
                                                                          cluster_name=self.coin.resources.dst_kafka_cluster)

        src_num_of_brokers: int = VictoriaMetricsAPI.get_number_of_brokers(network=self.coin.src_network,
                                                                           cluster_name=self.coin.resources.src_kafka_cluster)
        dst_num_of_brokers: int = VictoriaMetricsAPI.get_number_of_brokers(network=self.coin.dst_network,
                                                                           cluster_name=self.coin.resources.dst_kafka_cluster)

        return KafkaResource(src_cluster_storage=src_cluster_storage, dst_cluster_storage=dst_cluster_storage,
                             src_num_of_brokers=src_num_of_brokers, dst_num_of_brokers=dst_num_of_brokers)

    def __get_nifi_resource(self) -> NifiResource:
        src_storage: float = PrometheusAPI.get_nifi_storage(network=self.coin.src_network,
                                                            name=self.coin.resources.src_naas)
        dst_storage: Optional[float] = None

        if self.coin.resources.dst_naas:
            dst_storage = PrometheusAPI.get_nifi_storage(
                network=self.coin.dst_network,
                name=self.coin.resources.dst_naas
            )

        stress_testing_throughput: float = stress_test_values_by_coin[self.coin.__class__.__name__]

        return NifiResource(src_storage=src_storage, dst_storage=dst_storage,
                            stress_testing_throughput=stress_testing_throughput, sla=self.coin.nifi_sla)
