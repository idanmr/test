from pydantic import BaseModel


class BaseResource(BaseModel):
    def calculate_needed_resources(self, desired_throughput: float):
        raise NotImplementedError

    def get_current_resource_throughput(self):
        raise NotImplementedError

    def get_missing_resources(self, desired_throughput: float):
        raise NotImplementedError
