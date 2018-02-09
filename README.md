SpiTest
=======

A framework, implemented with python3,
to easily assert the expected behavior of a software in real time,
using log files

## QuickStart

### RocketChat



## How to use it


## How does it work

SpiTest works in 3 parts:
- Agents
- Core
- Database queries (ElasticSearch)

The interaction with SpiTest is from the implementation of an Agent.

### Agent
An agent, called `LogAgent`, is an interface that tells the core
when to be called based on the content of the expected log.

### Input
Log file are parsed with LogStash and injected into ElasticSearch

The required fields are:
- `@timestamp` with the timestamp of the registered log
- `log` the message inside the log

Have a look at `./rocketchat/elastic/logsstash/logstash.conf` for an exemple


## Author
This work is born in Spirals