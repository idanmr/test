from consts import GB


class PrometheusAPI:
    @staticmethod
    def get_nifi_storage():
        return 700 * GB

    @staticmethod
    def get_s3_storage():
        return 700 * GB
