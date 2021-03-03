# parser-streamer

## setting requirements
- python package **coverage** for unittest
- **Docker** for builds
- **git** for CM

## setting for kafka, hadoop, spark
for host setting
```
vim /etc/hosts
127.0.0.1 localhost kafka
```

hadoop & spark
```
git clone https://github.com/segulee/docker-scripts.git
cd docker-scripts/spark
./start.sh
docker exec -it master /bin/bash
start-all.sh
exit()

(default hadoop slave 2)
(for N slave, ./start.sh N)
```
kafka (run spark container first for network settings)
```
git clone https://github.com/segulee/docker-scripts.git
cd docker-scripts/kafka
docker-compose -f on_spark.yml up
```

## get emitter (need python3, setup_tools)
```
git clone https://github.com/segulee/logstash_logger.git
cd logstash_logger
make local 
cp dist/emitter-1.0.0.2-py3-none-any.whl {workdir}
cd {workdir}
pip install emitter-1.0.0.2-py3-none-any.whl
```

## setting requirements for local test
```
./install.sh
```

## for local test
```
pip install coverage
pip install pytest

make unittest
```

