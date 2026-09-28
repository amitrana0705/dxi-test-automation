from abc import ABC, abstractmethod


class ODIClient(ABC):
    """
    Defines the common interface for interacting with ODI.
    """

    @abstractmethod
    def check_connection(self) -> bool:
        """Check whether ODI is reachable."""
        pass

    @abstractmethod
    def start_load_plan(self, load_plan_name: str) -> str:
        """Start an ODI Load Plan and return its execution ID."""
        pass