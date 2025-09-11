from controller.controller import Controller


def main():
    desired_throughput = float(input("enter throughput"))
    controller: Controller = Controller(desired_throughput=desired_throughput)

    print("needed: ", controller.calculate_needed_resources())
    print("current: ", controller.get_current_resources())
    print("missing:", controller.get_missing_resources())


if __name__ == '__main__':
    main()
