import pytest
from consts import KAFKA_RETENTION, KAFKA_BROKER_MAXIMUM_THROUGHPUT
from resources.kafka import KafkaResource


@pytest.fixture
def mock_kafka_resource():
    return KafkaResource(num_of_brokers=3, src_cluster_storage=100_000_000, dst_cluster_storage=120_000_000)


def test_current_throughput(mock_kafka_resource):
    throughput = mock_kafka_resource.get_current_resource_throughput()
    storage_throughput = min(mock_kafka_resource.src_cluster_storage / KAFKA_RETENTION,
                             mock_kafka_resource.dst_cluster_storage / KAFKA_RETENTION)
    infra_throughput = mock_kafka_resource.num_of_brokers * KAFKA_BROKER_MAXIMUM_THROUGHPUT
    assert throughput == min(storage_throughput, infra_throughput)


def test_calculate_needed_resources_increases_both(mock_kafka_resource):
    desired_throughput = 10_000_000
    needed = mock_kafka_resource.calculate_needed_resources(desired_throughput)
    expected_storage = KafkaResource._KafkaResource__get_kafka_storage_by_throughput(desired_throughput)
    expected_brokers = KafkaResource._KafkaResource__get_num_of_brokers_by_throughput(desired_throughput)
    assert needed.src_cluster_storage == expected_storage
    assert needed.dst_cluster_storage == expected_storage
    assert needed.num_of_brokers == expected_brokers
