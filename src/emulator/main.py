from random import uniform


def main() -> None:
    while True:
        cmd = input("MMP-14>")
        if cmd == "ostatus":
            print(f"""
            -------------------------------------------------------------------------------
            |     Outlet       |True RMS|Peak RMS|True RMS |Average | Volt-  |   Outlet   |
            |      Name        | Current| Current| Voltage | Power  | Amps   |   State    |
            -------------------------------------------------------------------------------
            | MOD 1 Outlet 1   |  {uniform(0.1, 0.9)} A |  0.9 A | 223.6 V |   49 W | 195 VA | On         |
            | MOD 1 Outlet 2   |  0.0 A |  0.0 A | 223.6 V |    0 W |   3 VA | On         |
            | MOD 1 Outlet 3   |  0.6 A |  0.6 A | 223.6 V |  119 W | 146 VA | On         |
            | MOD 1 Outlet 4   |  0.7 A |  0.7 A | 223.6 V |  132 W | 162 VA | On         |
            | MOD 1 Outlet 5   |  0.0 A |  0.0 A | 223.6 V |    0 W |   3 VA | On         |
            | MOD 2 Outlet 1   |  0.0 A |  0.0 A | 220.6 V |    0 W |   3 VA | On         |
            | MOD 2 Outlet 2   |  0.0 A |  0.0 A | 220.6 V |    0 W |   3 VA | On         |
            | MOD 2 Outlet 3   |  0.0 A |  0.0 A | 220.6 V |    0 W |   3 VA | On         |
            | MOD 2 Outlet 4   |  0.0 A |  0.0 A | 220.6 V |    0 W |   3 VA | On         |
            | MOD 2 Outlet 5   |  0.2 A |  0.2 A | 220.6 V |   12 W |  55 VA | On         |
            | MOD 3 Outlet 1   |  0.1 A |  0.1 A | 223.0 V |    0 W |  32 VA | On         |
            | MOD 3 Outlet 2   |  0.0 A |  0.0 A | 223.0 V |    0 W |   3 VA | On         |
            | MOD 3 Outlet 3   |  0.0 A |  0.0 A | 223.0 V |    0 W |   3 VA | On         |
            | MOD 3 Outlet 4   |  0.0 A |  0.0 A | 223.0 V |    0 W |   3 VA | On         |
            | MOD 3 Outlet 5   |  0.5 A |  0.5 A | 223.0 V |   92 W | 109 VA | On         |
            | MOD 4 Outlet 1   |  0.0 A |  0.0 A | 222.0 V |    0 W |   3 VA | On         |
            | MOD 4 Outlet 2   |  0.0 A |  0.0 A | 222.0 V |    0 W |   3 VA | On         |
            | MOD 4 Outlet 3   |  0.1 A |  0.1 A | 222.0 V |    2 W |  32 VA | On         |
            | MOD 4 Outlet 4   |  0.1 A |  0.2 A | 222.0 V |    4 W |  41 VA | On         |
            | MOD 4 Outlet 5   |  1.5 A |  1.7 A | 222.0 V |  287 W | 336 VA | Off        |
            -------------------------------------------------------------------------------""")


if __name__ == "__main__":
    main()
