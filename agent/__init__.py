class BaseAgent(object):
    """
    Base class for Agent

    """
    def get_next_point(self):
        raise NotImplementedError(
            "get_next_point() has to be implemented by subclasses"
        )
