# app parser-streamer

## setting requirements
- python package **coverage** for unittest
- **Docker** for builds
- **git** for CM

## setting requirements for local test
```
./install.sh
```

## for local test
```
./install.sh
pip install coverage
pip install pytest

make unittest
```

## get emitter (need python3, setup_tools)
```
git clone https://github.com/segulee/logstash_logger.git
cd logstash_logger
make local 
cp dist/emitter-1.0.0.2-py3-none-any.whl ~{workdir}
pip install emitter-1.0.0.2-py3-none-any.whl
```
