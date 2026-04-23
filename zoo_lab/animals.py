class Animal:
    def __init__(self, name):
        self.name = name
    
    def describe(self):
        return f"{self.__class__.__name__}: {self.name}"
    
class Lion(Animal):
    def __init__(self, name, age):
        super().__init__(name)
        self.age = age
    
    def describe(self):
        return f"Lion: {self.name} (Age: {self.age} years)"

class Bear(Animal):
    def __init__(self, name, species, age):
        super().__init__(name)
        self.age = age
        self.species = species
    
    def describe(self):
        return f"Bear: {self.name} ({self.species}, Age: {self.age} years)"

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)
        self.breed = breed
    
    def describe(self):
        return f"Dog: {self.name} ({self.breed})"


class Bird(Animal):
    def __init__(self, name, species, can_fly=True):
        super().__init__(name)
        self.species = species
        self.can_fly = can_fly
    
    def describe(self):
        flight_status = "can fly" if self.can_fly else "cannot fly"
        return f"Bird: {self.name} ({self.species}, {flight_status})"


class Fish(Animal):
    def __init__(self, name, species, water_type):
        super().__init__(name)
        self.species = species
        self.water_type = water_type
    
    def describe(self):
        return f"Fish: {self.name} ({self.species}, {self.water_type} water)"