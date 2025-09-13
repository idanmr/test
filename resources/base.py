from abc import ABC, abstractmethod

from pydantic import BaseModel


class BaseResource(BaseModel):
    def calculate_needed_resources(self, desired_throughput: float):
        raise NotImplementedError

    def get_current_resource_throughput(self):
        raise NotImplementedError

    def get_missing_resources(self, desired_throughput: float):
        raise NotImplementedError


class BaseResourceFactory(ABC):
    """
    Base class for resource factories.
    Factories should accept only the minimal parameters needed to create the resource.
    """

    @abstractmethod
    def create(self, *args, **kwargs) -> BaseResource:
        pass
