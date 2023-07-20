SHELL = /bin/bash

.PHONY: zk-up
zk-up:
	docker-compose -f docker-compose.yml up -d

.PHONY: zk-down
zk-down:
	docker-compose -f docker-compose.yml down

.PHONY: setup
setup:
	python3 -m venv ./env && source ./env/bin/activate && pip3 install -r requirements.txt

.PHONY: start-leader
start-leader:
	cd src && python3 leader.py

.PHONY: start-follower
start-follower:
	cd src && python3 follower.py