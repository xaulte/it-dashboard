# ── Application Metadata ──────────────────────────────────
APP_NAME = "Zoo Lab"
VERSION = "0.1.0"
CREATOR_NAME = "Austin Windorski"
PROF_NAME = "Prof. Frank Mora"
COURSE_NAME = "COP1034C - Python for IT"

# Import specific classes from each file
from animals import Dog, Bird, Fish, Bear, Lion  # noqa: E402
from habitat import Habitat # noqa: E402
from zookeeper import Zookeeper # noqa: E402
from zoo import Zoo # noqa: E402

# Create zookeeper
sarah = Zookeeper("Sarah", "Marine Biology")
max = Zookeeper("Max", "Arctic Wildlife")

# Create animals
rex    = Dog("Rex", "German Shepherd")
tweety = Bird("Tweety", "Canary", can_fly=True)
nemo   = Fish("Nemo", "Clownfish", "salt")
marcus = Bear("Marcus", "Polar Bear", 7)
ned    = Bird("Ned", "Penguin", can_fly=False)
simba  = Lion("Simba", 5)

# Create habitat and add animals
savannah = Habitat("Savannah", "tropical", 5)
savannah.add_animal(rex)
savannah.add_animal(tweety)
savannah.add_animal(simba)

arctic = Habitat("Arctic", "polar", 3)
arctic.add_animal(marcus)
arctic.add_animal(ned)

aquarium = Habitat("Aquarium", "marine", 10)
aquarium.add_animal(nemo)

# Build and run
zoo = Zoo("Hexworth Wildlife Park")
zoo.add_habitat(savannah)
zoo.add_habitat(arctic)
zoo.add_habitat(aquarium)

zoo.hire_keeper(sarah)
zoo.hire_keeper(max)

# Assign zookeeper to habitat
sarah.assign(savannah)
sarah.assign(aquarium)
max.assign(arctic)  

zoo.full_report()
sarah.daily_report()
max.daily_report()