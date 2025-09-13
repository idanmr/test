import tkinter
from tkinter import ttk, messagebox, StringVar

from controller.controller import Controller
from resources.base import BaseResource
from wallets.coins_factory import CoinsFactory
from wallets.enums import Coins
from wallets.models import BaseCoin


class ResourceUI:
    def __init__(self, root: tkinter.Tk) -> None:
        self.root: tkinter.Tk = root
        self.root.title("Resource Calculator")

        # Throughput input
        tkinter.Label(root, text="Desired Throughput:").grid(row=0, column=0, padx=10, pady=10)
        self.throughput_entry: tkinter.Entry = tkinter.Entry(root)
        self.throughput_entry.grid(row=0, column=1, padx=10, pady=10)

        # Coin dropdown
        tkinter.Label(root, text="Coin:").grid(row=1, column=0, padx=10, pady=10)
        self.coin_var: StringVar = tkinter.StringVar()
        self.coin_dropdown: ttk.Combobox = ttk.Combobox(root, textvariable=self.coin_var, state="readonly")
        self.coin_dropdown['values'] = [coin.value for coin in Coins]  # Use enum values
        self.coin_dropdown.grid(row=1, column=1, padx=10, pady=10)

        self.calc_button: tkinter.Button = tkinter.Button(root, text="Calculate", command=self.calculate)
        self.calc_button.grid(row=2, column=0, columnspan=2, pady=20)

    def calculate(self) -> None:
        try:
            desired_throughput: float = float(self.throughput_entry.get())
            coin_name: str = self.coin_var.get()

            if not coin_name:
                raise ValueError("Please select a coin.")

            coin_enum: Coins = Coins(coin_name)
            coin: BaseCoin = CoinsFactory.create_coin(coin_enum)

            controller: Controller = Controller(desired_throughput=desired_throughput, coin=coin)

            needed: list[BaseResource] = controller.calculate_needed_resources()
            current: list[BaseResource] = controller.get_current_resources()
            missing: list[BaseResource] = controller.get_missing_resources()
            current_throughput: float = controller.get_current_throughput()

            result_msg: str = (
                f"Coin: {coin_enum.value}\n\n"
                f"Desired Throughput: {desired_throughput}\n"
                f"Current Throughput: {current_throughput}\n\n"
                f"Needed Resources:\n{needed}\n\n"
                f"Current Resources:\n{current}\n\n"
                f"Missing Resources:\n{missing}"
            )

            messagebox.showinfo("Calculation Result", result_msg)

        except ValueError as e:
            messagebox.showerror("Error", str(e))
