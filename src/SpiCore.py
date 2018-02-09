from Database import Database
from utils import AgentUtils, SpiExceptions


class SpiCore:

    def __init__(self):
        self.registered_agents = []  # list of LogAgent
        self.database = Database()

    def register(self, log_agents):
        """
        method to register an agent
        """
        self.registered_agents.append(log_agents)

    def run(self):
        """
        The main loop
        """
        while True:
                # map every expected_entry of an agent with himself
                expect_agent_entries = AgentUtils.map_agent_with_expected(self.registered_agents)

                # query ElasticSearch to find the next logs that match the expected_entries
                results = self.database.query(expect_agent_entries)

                # if no results, we reached the end of the file
                if len(results) == 0:
                    self.notify_agents_end(expect_agent_entries)
                    return

                # taking the first log is very important since it is the next from the timestamp_cursor
                first_log = results[0]

                # we update the timestamp_cursor for the next query
                self.database.update_timestamp(first_log["@timestamp"])

                # we notify the agents
                self.notify_agents(expect_agent_entries, first_log["log"], first_log["@timestamp"])

    @staticmethod
    def notify_agents(expect_agent_entries, log, timestamp):
        """
        notify agents if their expected match with 'log'
        else notify them with only the timestamp allowing them to assert a timeout
        :param expect_agent_entries: the list of ExpectAgentEntry
        :param log: the message sent to the agent
        :param timestamp: the timestamp sent to the agent
        :return:
        """
        try:
            for expect_agent_entry in expect_agent_entries:
                if expect_agent_entry.expected.lower() in log.lower():
                    expect_agent_entry.agent.notify_match_expected(timestamp, log)
                else:
                    expect_agent_entry.agent.notify_not_match(timestamp)
        except SpiExceptions.AssertFailedException as e:
            print("Assertion Failed: ", e)

    def notify_agents_end(self, expect_agent_entries):
        """
        Update the timestamp of agents with the last timestamp recorded in the database
        in order to allow them to assert a timeout
        :param expect_agent_entries: the list of ExpectAgentEntry
        :return: void
        """
        try:
            for expect_agent_entry in expect_agent_entries:
                timestamp = self.database.get_oldest_timestamp()
                expect_agent_entry.agent.notify_not_match(timestamp)
        except SpiExceptions.AssertFailedException as e:
            print("Assertion Failed: ", e)
