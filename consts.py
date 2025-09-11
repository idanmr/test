from wallets.enums import Coins

BYTE = 1
KB = BYTE * 1024
MB = KB * 1024
GB = MB * 1024
TB = GB * 1024

SECOND = 1
MINUTE = SECOND * 60
HOUR = MINUTE * 60
DAY = HOUR * 24

KAFKA_RETENTION = 3 * HOUR
KAFKA_BROKER_MAXIMUM_THROUGHPUT = 70 * MB
LilA2B_SRC_KAFKA_CLUSTER = "temp"
LilA2B_DST_KAFKA_CLUSTER = "temp"


LilA2B_SRC_NIFI = "temp"
LilA2B_DST_NIFI = "temp"


stress_test_values_by_coin = {
    Coins.LilA2BThroughput: 300 * MB
}

sla_by_coin = {
    Coins.LilA2BThroughput: 15 * SECOND
}
