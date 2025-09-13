from typing import Optional
from resources.base import BaseResourceFactory, BaseResource
from resources.nifi.nifi_resource import NifiResource
from sampler.prometheus import PrometheusAPI


class NifiResourceFactory(BaseResourceFactory):
    def create(self, src_network: str, dst_network: str, src_naas: str, dst_naas: Optional[str] = None,
               stress_testing_throughput: float = 0, sla: Optional[float] = None
               ) -> BaseResource:
        src_storage: float = PrometheusAPI.get_nifi_storage(network=src_network, name=src_naas)
        dst_storage: Optional[float] = None

        if dst_naas:
            dst_storage = PrometheusAPI.get_nifi_storage(network=dst_network, name=dst_naas)

        return NifiResource(
            src_storage=src_storage,
            dst_storage=dst_storage,
            stress_testing_throughput=stress_testing_throughput,
            sla=sla
        )
