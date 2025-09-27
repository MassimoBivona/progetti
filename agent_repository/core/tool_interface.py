from abc import ABC, abstractmethod

class ToolInterface(ABC):
    """
    An abstract base class for all tools available to the Autonomous Agent.
    It defines a standard interface for the agent's reasoner to interact with.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """The unique, machine-readable name of the tool."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """A brief description of what the tool does."""
        pass

    @abstractmethod
    def execute(self, **kwargs):
        """
        Executes the tool with the given arguments and returns the result.
        """
        pass