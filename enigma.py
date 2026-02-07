import json
class Enigma:
    def __init__(self, hash_map, wheels, reflector_map):
        self.hash_map = hash_map
        self.wheels = wheels[:]
        self.initial_wheels = wheels[:]
        self.rev_hash_map = {v: k for k, v in self.hash_map.items()}
        self.reflector_map = reflector_map
        pass
#TODO nothing
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
            i += 1
        else:
            i += shift
                

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

        map_hash = data["hash_map"]
        wheels = data["wheels"]
        map_reflector = data["reflector_map"]

        return Enigma(map_hash, wheels, map_reflector)

    except Exception:
        raise JSONFileException()


import sys

USAGE_MSG = "Usage: python3 enigma.py -c <config_file> -i <input_file> -o <output_file>"
ERROR_MSG = "The enigma script has encountered an error"

def main():
    try:
        args = sys.argv[1:]

        config_file = None
        input_file = None
        output_file = None

        i = 0
        while i < len(args):
            if args[i] == "-c":
                config_file = args[i + 1]
            elif args[i] == "-i":
                input_file = args[i + 1]
            elif args[i] == "-o":
                output_file = args[i + 1]
            else:
                print(USAGE_MSG, file=sys.stderr)
                exit(1)
            i += 2

        if config_file is None or input_file is None:
            print(USAGE_MSG, file=sys.stderr)
            exit(1)

        enigma = load_enigma_from_path(config_file)

        with open(input_file, "r") as f:
            lines = f.readlines()

        encrypted_lines = []
        for line in lines:
            encrypted_lines.append(enigma.encrypt(line.rstrip("\n")))

        if output_file is not None:
            with open(output_file, "w") as f:
                for line in encrypted_lines:
                    f.write(line + "\n")
        else:
            for line in encrypted_lines:
                print(line)

    except Exception:
        print(ERROR_MSG)
        exit(1)


if __name__ == "__main__":
    main()
