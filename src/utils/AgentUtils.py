from utils.ExpectAgentEntry import ExpectAgentEntry


def map_agent_with_expected(log_agents: "list of LogAgent") -> "list of ExpectAgentEntry":
    """
    :param log_agents: the list of LogAgent
    :return: a list of ExpectAgentEntry
    """
    result = []
    for agent in log_agents:
        for expected in agent.get_expected_list():
            element = ExpectAgentEntry(agent=agent, expected=expected)
            result.append(element)
    return result
