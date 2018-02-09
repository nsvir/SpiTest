
class LogAgent(object):

    def get_expected_list(self):
        """
        this method is called from SpiCore
        it should return a list of string
        where each string is supposed to match, partially, a log entry
        ex: ["sendMessage"] will match the log entry: user:XXX sendMessageTo(user=YYY)
        :return: a list of the expected string in the log entry
        """
        raise NotImplementedError

    def notify_match_expected(self, timestamp, log):
        """
        This method is called from SpiCore
        when the log entry did match with one element of get_expected_list
        :param timestamp: when the log happened
        :param log: the log entry
        :return:
        """
        raise NotImplementedError

    def notify_not_match(self, timestamp):
        """
        This method is called from the SpiCore
        anytime it does a request to the database
        this has been implemented to allow the agent to assert a timeout
        :param timestamp: when nothing happened before the last notification
        """
        raise NotImplementedError
