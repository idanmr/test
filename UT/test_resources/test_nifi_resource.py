import pytest

from resources.nifi import NifiResource


@pytest.fixture
def mock_nifi_resource():
    return NifiResource(
        src_storage=100.0,
        dst_storage=200.0,
        stress_testing_throughput=50.0,
        sla=10.0
    )


def test_calculate_needed_resources(mock_nifi_resource):
    desired_throughput = 100.0
    result = mock_nifi_resource.calculate_needed_resources(desired_throughput)

    assert result.src_storage == pytest.approx(desired_throughput / mock_nifi_resource.sla)
    assert result.dst_storage == pytest.approx(desired_throughput / mock_nifi_resource.sla)
    assert result.stress_testing_throughput == desired_throughput


def test_get_current_resource_throughput_src_only():
    resource = NifiResource(src_storage=100.0, stress_testing_throughput=20.0, sla=10.0)
    # storage throughput = 100 / 10 = 10
    # min(10, 20) = 10
    assert resource.get_current_resource_throughput() == 10.0


def test_get_current_resource_throughput_with_dst():
    resource = NifiResource(src_storage=100.0, dst_storage=50.0, stress_testing_throughput=20.0, sla=10.0)
    # src_throughput = 100/10 = 10
    # dst_throughput = 50/10 = 5
    # min(5, 10) = 5
    # min(5, 20) = 5
    assert resource.get_current_resource_throughput() == 5.0


def test_get_missing_resources(mock_nifi_resource):
    desired_throughput = 200.0
    result = mock_nifi_resource.get_missing_resources(desired_throughput)

    needed = mock_nifi_resource.calculate_needed_resources(desired_throughput)
    assert result.src_storage == max(0, needed.src_storage - mock_nifi_resource.src_storage)
    assert result.dst_storage == max(0, needed.dst_storage - mock_nifi_resource.dst_storage)
    assert result.stress_testing_throughput == max(
        0, needed.stress_testing_throughput - mock_nifi_resource.stress_testing_throughput
    )


def test_no_missing_resources(mock_nifi_resource):
    desired_throughput = 10.0
    result = mock_nifi_resource.get_missing_resources(desired_throughput)

    assert result.src_storage == 0
    assert result.dst_storage == 0
    assert result.stress_testing_throughput == 0
