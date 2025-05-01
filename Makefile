.PHONY: pulsar

pulsar:
	docker-compose -f src/examples/pulsar_/docker-compose.yaml up -d