class Zoo:
    def __init__(self, name):
        self.name = name
        self.habitats = []
        self.keepers = []

    def add_habitat(self, habitat):
        self.habitats.append(habitat)

    def hire_keeper(self, keeper):
        self.keepers.append(keeper)

    def total_animals(self):
        return sum(len(h.animals) for h in self.habitats)

    def full_report(self):
        print("----------------------------------")
        print(f"===++ {self.name} ++===")
        print("----------------------------------")
        print(f"Habitats: {len(self.habitats)}")
        print(f"Animals: {self.total_animals()}")
        print(f"Keepers: {len(self.keepers)}")
        print("==================================")
        for hab in self.habitats:
            print(f"{hab}")
            hab.roll_call()
            print("----------------------------------")