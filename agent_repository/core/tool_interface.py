from abc import ABC, abstractmethod

class ToolInterface(ABC):
    """
    An abstract base class for all tools available to the Autonomous Agent.
    It defines a standard interface for the agent's reasoner to interact with.

    This ensures that the core reasoner can handle any tool in a generic way,
    understanding its purpose and how to execute it.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """The unique, machine-readable name of the tool."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """A brief description of what the tool does, for the reasoner to understand its purpose."""
        pass

    @abstractmethod
    def execute(self, *args, **kwargs):
        """
        Executes the tool with the given arguments and returns the result.

        The arguments and return types will be specific to each tool.
        """
        pass