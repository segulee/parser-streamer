VERSION=$(shell cat version)
TEST_REPORTS=$(shell pwd)/../../test-reports
USER=segulee
APP=streamer

unittest:
	coverage run -m pytest tests -v --junitxml="$(TEST_REPORTS)/unittest.xml"
	coverage report

publish:
	docker push $(USER)/$(APP):$(VERSION)
	docker push $(USER)/$(APP):latest

local:
	docker build --network host --no-cache -t $(USER)/$(APP):$(VERSION) -f ../../build/Dockerfile .
	docker tag $(USER)/$(APP):$(VERSION) $(USER)/$(APP):$(VERSION)
	docker tag $(USER)/$(APP):$(VERSION) $(USER)/$(APP):latest

save:
	docker save -o $(APP)-$(VERSION).tar $(USER)/$(APP):$(VERSION)
