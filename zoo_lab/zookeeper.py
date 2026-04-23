class Zookeeper:
    def __init__(self, name, specialty):
        self.name = name
        self.specialty = specialty
        self.assigned_habitats = []

    def assign(self, habitat):
        self.assigned_habitats.append(habitat)
        return f"{self.name} now manages {habitat.name}"

    def daily_report(self):
        print(f"Keeper: {self.name}")
        print(f"Specialty: {self.specialty}")
        print(f"Assigned Habitats: {len(self.assigned_habitats)}")
        print()
        for hab in self.assigned_habitats:
            print()
            print(f"  Habitat: {hab.name}")
            print(f"  Climate: {hab.climate}")
            print(f"  Animals ({len(hab.animals)}):")
            hab.roll_call()
            print()