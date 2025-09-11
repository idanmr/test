from typing import Optional

from pydantic import BaseModel, Field
from consts import LilA2B_SRC_NIFI, LilA2B_DST_NIFI, LilA2B_DST_KAFKA_CLUSTER, LilA2B_SRC_KAFKA_CLUSTER, \
    stress_test_values_by_coin, sla_by_coin
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
