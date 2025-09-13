from typing import Optional, List

from pydantic import BaseModel, Field

from consts import LilA2B_SRC_NIFI, LilA2B_DST_NIFI, LilA2B_DST_KAFKA_CLUSTER, LilA2B_SRC_KAFKA_CLUSTER, \
    stress_test_values_by_coin, sla_by_coin
from resources.base import BaseResource
from resources.kafka.kafka_factory import KafkaResourceFactory
from resources.nifi.nifi_factory import NifiResourceFactory
from wallets.enums import Coins


class BaseCoinResources(BaseModel):
    src_kafka_cluster: str
    dst_kafka_cluster: str
    src_naas: str
    dst_naas: Optional[str] = None
    stress_test: float


class BaseCoin(BaseModel):
    src_network: str = "A"
    dst_network: str = "B"
    nifi_sla: float
    resources: BaseCoinResources

    def get_resources(self) -> list[BaseResource]:
        """Return all resources for this coin."""
        raise NotImplementedError()


class LilA2BResources(BaseCoinResources):
    src_kafka_cluster: str = LilA2B_SRC_KAFKA_CLUSTER
    dst_kafka_cluster: str = LilA2B_DST_KAFKA_CLUSTER
    src_naas: str = LilA2B_SRC_NIFI
    dst_naas: str = LilA2B_DST_NIFI
    stress_test: float = stress_test_values_by_coin[Coins.LilA2BThroughput]


class LilA2BThroughput(BaseCoin):
    src_network: str = "A"
    dst_network: str = "B"
    nifi_sla: float = sla_by_coin[Coins.LilA2BThroughput]
    resources: LilA2BResources = Field(default_factory=LilA2BResources)

    def get_resources(self) -> list[BaseResource]:
        """Return instantiated resources for this coin."""
        resources: List[BaseResource] = [
            KafkaResourceFactory().create(src_network=self.src_network, dst_network=self.dst_network,
                                          src_cluster=self.resources.src_kafka_cluster,
                                          dst_cluster=self.resources.dst_kafka_cluster),
            NifiResourceFactory().create(src_network=self.src_network, dst_network=self.dst_network,
                                         src_naas=self.resources.src_naas,
                                         dst_naas=self.resources.dst_naas,
                                         stress_testing_throughput=self.resources.stress_test,
                                         sla=self.nifi_sla)
        ]
        return resources
