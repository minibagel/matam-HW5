import json
class Enigma:
    def __init__(self, hash_map, wheels, reflector_map):
        self.hash_map = hash_map
        self.wheels = wheels[:]
        self.initial_wheels = wheels[:]
        self.rev_hash_map = {v: k for k, v in self.hash_map.items()}
        self.reflector_map = reflector_map
        pass

    def encrypt(self, message):
        count = 0
        result = []

        for ch in message:
            encrypt, count = self._encrypt_char(ch, count)
            self.change_wheels(count)
            result.append(encrypt)

        self.wheels = self.initial_wheels[:]
        return "".join(result)
        pass

    def change_wheels(self, count):
        w1 = self.wheels[0]
        w2 = self.wheels[1]
        w3 = self.wheels[2]

        w1 += 1

        if w1 > 8:
            w1 = 1

        if count % 2 == 0:
            w2 = w2 * 2
        else:
            w2 -= 1

        if count % 10 == 0:
            w3 = 10
        elif count % 3 == 0:
            w3 = 5
        else:
            w3 = 0

        self.wheels = [w1, w2, w3]


    def _encrypt_char(self, ch, count):

        if not ch.islower():
            return ch, count

        count += 1

        w1, w2, w3 = self.wheels

        i = self.hash_map[ch]

        shift = ((2*w1) - w2 + w3) % 26

        if shift == 0:
            i += shift
        else:
            i += 1

        i = i % 26


        c1 = self.rev_hash_map[i]
        c2 = self.reflector_map[c1]

        i = self.hash_map[c2]

        shift = ((2*w1) - w2 + w3) % 26

        if shift == 0:
            i -= 1
        else:
            i -= shift

        i = i % 26

        self.wheels = [w1, w2, w3]

        return self.rev_hash_map[i], count

    pass


class JSONFileException(Exception):
    pass


def load_enigma_from_path(path):
    try:
        with open(path, "r") as f:
            data = json.load(f)

        map_hash = data["map_hash"]
        wheels = data["wheels"]
        map_reflector = data["map_reflector"]

        return Enigma(map_hash, wheels, map_reflector)

    except Exception:
        raise JSONFileException()


