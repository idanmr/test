from consts import GB

# TODO: add logic
class PrometheusAPI:
    @staticmethod
    def get_nifi_storage(network: str, name: str) -> float:
        return 700 * GB

    @staticmethod
    def get_s3_storage(network, name):
        return 700 * GB
