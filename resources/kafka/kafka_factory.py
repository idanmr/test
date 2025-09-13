from resources.base import BaseResourceFactory, BaseResource
from resources.kafka.kafka_resource import KafkaResource
from sampler.victoria_metrics import VictoriaMetricsAPI


class KafkaResourceFactory(BaseResourceFactory):
    def create(self, src_network: str, dst_network: str, src_cluster: str, dst_cluster: str) -> BaseResource:
        src_cluster_storage: float = VictoriaMetricsAPI.get_kafka_storage(
            network=src_network, cluster_name=src_cluster
        )
        dst_cluster_storage: float = VictoriaMetricsAPI.get_kafka_storage(
            network=dst_network, cluster_name=dst_cluster
        )

        src_num_of_brokers: int = VictoriaMetricsAPI.get_number_of_brokers(
            network=src_network, cluster_name=src_cluster
        )
        dst_num_of_brokers: int = VictoriaMetricsAPI.get_number_of_brokers(
            network=dst_network, cluster_name=dst_cluster
        )

        return KafkaResource(
            src_cluster_storage=src_cluster_storage,
            dst_cluster_storage=dst_cluster_storage,
            src_num_of_brokers=src_num_of_brokers,
            dst_num_of_brokers=dst_num_of_brokers
        )
