from consts import GB

# TODO: add logic

class VictoriaMetricsAPI:
    @staticmethod
    def get_number_of_brokers(network: str, cluster_name: str) -> int:
        return 3

    @staticmethod
    def get_dst_number_of_brokers() -> int:
        return 6

    @staticmethod
    def get_kafka_storage(network: str, cluster_name: str) -> float:
        return 500 * GB

    @staticmethod
    def get_dst_kafka_storage() -> float:
        return 300 * GB
