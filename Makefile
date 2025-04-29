.PHONY: pulsar

pulsar:
	docker-compose -f src/examples/pulsar/docker-compose.yaml up -d