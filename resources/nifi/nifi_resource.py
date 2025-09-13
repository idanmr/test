from typing import Optional

from consts import MB
from resources.base import BaseResource


class NifiResource(BaseResource):
    src_storage: float
    dst_storage: Optional[float] = None
    stress_testing_throughput: float
    sla: Optional[float] = None

    def calculate_needed_resources(self, desired_throughput: float) -> BaseResource:
        needed_storage: float = self.__get_storage_by_throughput_and_sla(throughput=desired_throughput)

        return NifiResource(
            src_storage=needed_storage,
            dst_storage=needed_storage,
            stress_testing_throughput=desired_throughput,
        )

    def get_current_resource_throughput(self) -> float:
        storage_throughput: float = self.__get_storage_throughput()
        return min(storage_throughput, self.stress_testing_throughput)

    def get_missing_resources(self, desired_throughput: float):
        needed: BaseResource = self.calculate_needed_resources(desired_throughput)

        missing_src_storage = max(0, needed.src_storage - self.src_storage)
        missing_dst_storage = max(0, needed.dst_storage - self.dst_storage)
        missing_stress_testing_throughput = max(0, needed.stress_testing_throughput - self.stress_testing_throughput)
        return NifiResource(
            src_storage=missing_src_storage,
            dst_storage=missing_dst_storage,
            stress_testing_throughput=missing_stress_testing_throughput,
            sla=None
        )

    def __get_storage_by_throughput_and_sla(self, throughput: float) -> float:
        # TODO: add logic
        return throughput / self.sla

    def __get_storage_throughput(self) -> float:
        src_throughput: float = self.src_storage / self.sla
        if self.dst_storage:
            dst_throughput: float = self.dst_storage / self.sla
            return min(src_throughput, dst_throughput)
        return src_throughput

    def to_human_readable(self) -> str:
        dst = f"{self.dst_storage:.2f} " if self.dst_storage is not None else "N/A"
        return (
            f"NiFi Resource:\n"
            f"  - Source Storage: {self.src_storage:.2f} \n"
            f"  - Destination Storage: {dst}\n"
            f"  - Stress Test Throughput: {self.stress_testing_throughput:.2f}\n"
            f"  - SLA: {self.sla}"
        )