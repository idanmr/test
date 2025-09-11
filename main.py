from controller.controller import Controller
from wallets.models import LilA2BThroughput


def main():
    desired_throughput = float(input("Enter throughput: "))

    controller = Controller(
        desired_throughput=desired_throughput,
        coin=LilA2BThroughput()
    )

    print("needed:", controller.calculate_needed_resources())
    print("current:", controller.get_current_resources())
    print("missing:", controller.get_missing_resources())
    print("current throughput", controller.get_current_throughput())


if __name__ == '__main__':
    main()
