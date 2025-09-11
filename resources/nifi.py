from typing import Optional

from resources.base import BaseResource


class NifiResource(BaseResource):
    src_storage: float
    dst_storage: Optional[float]
    stress_testing_throughput: float

    def calculate_needed_resources(self, desired_throughput: float) -> BaseResource:
        pass

    def get_current_resource_throughput(self):
        pass

    def get_missing_resources(self, desired_throughput: float):
        pass
