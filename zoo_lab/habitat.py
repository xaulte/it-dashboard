class Habitat:
    def __init__(self, name, climate, capacity):
        self.name = name
        self.climate = climate
        self.capacity = capacity
        self.animals = []

    def add_animal(self, animal):
        if len(self.animals) >= self.capacity:
            return f"{self.name} is full! ({self.capacity} max)"
        self.animals.append(animal)
        return f"{animal.name} added to {self.name}"

    def roll_call(self):
        for animal in self.animals:
            print(f"  {animal.describe()}")

    def __str__(self):
        return f"[{self.climate}] {self.name} ({len(self.animals)}/{self.capacity})"


if __name__ == "__main__":
    # Test code - only runs when script is executed directly
    savannah = Habitat("Savannah Exhibit", "tropical", 5)
    print(savannah)