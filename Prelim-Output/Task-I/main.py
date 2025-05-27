# Tagle, Marc Neil V. - M001

from guitar import Guitar
from electric_guitar import ElectricGuitar
from bass_guitar import BassGuitar

def main() -> None:
    g = Guitar("red", "Epiphone")
    print(g)
    print()

    eg = ElectricGuitar("blue", "Fender", "Stratocaster", "single-coil")
    print(eg)
    print()

    bg = BassGuitar("black", "Cort", "Action", "PJ")
    print(bg)
    print()

    g.color = "sunburst"
    print(g.play_a_song("Ang Huling El Bimbo"))
    print(g.tune())
    print(g.play_a_chord())
    print()

    eg.model = "Telecaster"
    print(eg.tune())
    print(eg.shred())
    print(eg.solo())
    print()

    bg.pickups = "humbucker"
    print(bg.tune())
    print(bg.slide())
    print(bg.slap_and_pop())

    print(g)
    print()
    print(eg)
    print()
    print(bg)
    print()

if __name__ == "__main__":
    main()