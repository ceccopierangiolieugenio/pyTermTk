from enum import IntEnum, Flag, Enum, auto

def test_enum_flag():
    class pippo(int, Flag):
        A = 0x01
        B = 0x02
        C = 0x03

    f1 = pippo.A
    f2 = pippo.B
    f3 = pippo.C
    f4 = pippo.A | pippo.B

    print(f1)
    print(f2)
    print(f3)
    print(f4)

    print(f1.value)
    print(f2.value)
    print(f3.value)
    print(f4.value)

    print(bool(pippo.A & f1))
    print(bool(pippo.A & f2))
    print(bool(pippo.A & f3))
    print(bool(pippo.A & f4))

    print(int(f1))
    print(int(f2))
    print(int(f3))
    print(int(f4))

    print(f"{int(f1):03X}")
    print(f"{int(f2):03X}")
    print(f"{int(f3):03X}")
    print(f"{int(f4):03X}")

def test_enum_flag():
    class Pippo(str, Enum):
        A = '0x01'
        B = '0x02'
        C = '0x03'

    a = Pippo.A
    assert isinstance(a,Pippo)
    assert isinstance(a,(Pippo,))




