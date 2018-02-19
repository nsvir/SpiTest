SpiTest
=======

A framework, implemented with python3,
to easily assert the expected behavior of a software in real time,
using log files

![scientific_poster](https://raw.githubusercontent.com/nsvir/SpiTest/master/poster/Nicolas%20SVIRCHEVSKY.png)

## QuickStart

### RocketChat
Inflate ElasticSearch with RocketChat logs

```
cd ./rocketchat
cat README.md
```

### SpiTest
```
virtualenv -p python3 venv
source ./venv/bin/activate
pip install -r requierments.txt
PYTHONPATH=./src python rocketchat/rocketchat_test.py
```

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
- [Nicolas SVIRCHEVSKY](https://github.com/nsvir)
- [Lakhdar MEFTAH](https://github.com/m3ftah)
