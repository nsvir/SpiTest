class ExpectAgentEntry:
    """
    Class used has a container
    go to get_expected_list for explanations
    """

    def __init__(self, agent, expected) -> None:
        super().__init__()
        self.agent = agent
        self.expected = expected
