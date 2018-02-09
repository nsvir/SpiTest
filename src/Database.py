from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q

from utils import ExpectAgentEntry


class Database:

    def __init__(self, elastic=None):
        self.elastic = elastic
        if self.elastic is None:
            self.elastic = {
                'host': 'localhost',
                'port': '9200',
                'index': "logstash-*"
            }
        self.timestamp_cursor = None
        self.client = Elasticsearch([self.elastic])
        self.search = Search(using=self.client, index=self.elastic["index"])

    def build_query(self, expect_agent_entries: "list of ExpectAgentEntry"):
        """
        build_query, in the ElasticSearch format, like this:
        {
            "sort": [ "@timestamp" ],
            "query": {
                "bool": {
                    "should": [
                        {
                            "query_string": {
                                "analyze_wildcard": true,
                                "query": "log:<expectedlog1>",
                                "split_on_whitespace": false
                            }
                        },
                        {
                            "query_string": {
                                "analyze_wildcard": true,
                                "query": "log:<expectedlog2>",
                                "split_on_whitespace": false
                            }
                        }
                    ],
                    "filter": [ { "range": { "@timestamp": { "gt": <timestamp_cursor> } } } ]
                }
            }
        }
        """
        s = self.search
        s = s.sort("@timestamp")
        expected_match = []
        for expect_agent_entry in expect_agent_entries:
            query_string = Q("query_string",
                             query="log:*%s*" % expect_agent_entry.expected,
                             split_on_whitespace=False,
                             analyze_wildcard=True)
            expected_match.append(query_string)
        s.query = Q('bool', should=expected_match)
        if self.timestamp_cursor is not None:
            s = s.filter("range", **{"@timestamp": {'gt': self.timestamp_cursor}})
        return s

    def update_timestamp(self, timestamp):
        """
        It is important to update the timestamp to the last known
        the timestamp cursor is used in build_query in order to not retrieve passed logs
        """
        self.timestamp_cursor = timestamp

    def get_oldest_timestamp(self):
        """
        Retrieve the last recorded timestamp
        This is used when LogStash is plugged with a File
        """
        return self.search.sort("-@timestamp").execute()[0]["@timestamp"]

    def query(self, expect_agent_entries: "list of ExpectAgentEntry"):
        return self.build_query(expect_agent_entries).execute()
