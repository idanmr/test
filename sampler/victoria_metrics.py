from consts import GB


class VictoriaMetricsAPI:
    @staticmethod
    def get_src_number_of_brokers() -> int:
        return 3

    @staticmethod
    def get_dst_number_of_brokers() -> int:
        return 6

    @staticmethod
    def get_src_kafka_storage() -> float:
        return 500 * GB

    @staticmethod
    def get_dst_kafka_storage() -> float:
        return 300 * GB
