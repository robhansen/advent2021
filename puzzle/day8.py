import sys

NUMBERS = {
    0: "abcefg",
    1: "cf",
    2: "acdeg",
    3: "acdfg",
    4: "bcdf",
    5: "abdfg",
    6: "abdefg",
    7: "acf",
    8: "abcdefg",
    9: "abcdfg"
}
class Options:
    def __init__(self):
        self.options = {
            "a": "abcdefg",
            "b": "abcdefg",
            "c": "abcdefg",
            "d": "abcdefg",
            "e": "abcdefg",
            "f": "abcdefg",
            "g": "abcdefg"
        }

    def keep_only(self, to_keep, apply_to):
        for char in apply_to:
            self.options[char] = ''.join(list(set.intersection(set(self.options[char]), set(to_keep))))

    def invert(self, to_invert):
        return ''.join(list(set("abcdefg").difference(set(to_invert))))

    def apply_signal(self, signal):
        matching_numbers = [] # list of sets
        for number, segments in NUMBERS.items():
            if len(segments) == len(signal):
                matching_numbers.append(set(segments))
        chars_in_all = ''.join(list(set.intersection(*matching_numbers)))
        chars_in_some = ''.join(list(set.union(*matching_numbers)))
        
        self.keep_only(signal, chars_in_all) # remove all options but signal from chars_in_all
        self.keep_only(self.invert(signal), self.invert(chars_in_some))

        for letter, options in self.options.items(): # uniquify
            if len(options) == 1:
                self.keep_only(self.invert(options), self.invert(letter))

    def get_corrected_wire(self, input):
        for actual, wrong in self.options.items():
            if input == wrong:
                return actual
        return 'X'
    def get_corrected_signal(self, signal):
        corrected = []
        for char in signal:
            corrected.append(self.get_corrected_wire(char))
        return ''.join(corrected)
    def get_number(self, signal):
        corrected = set(self.get_corrected_signal(signal))
        for number, wires in NUMBERS.items():
            if corrected == set(wires):
                return number
        return None
    def debug(self):
        print(self.options)

if len(sys.argv) != 2:
    print("Help: {} <filename>".format(sys.argv[0]))
    sys.exit(0)

digits = []
output_values = []
with open(sys.argv[1]) as file:
    for line in file:
        portions = line.split(" | ")
        signals = portions[0].strip().split(" ")
        outputs = portions[1].strip().split(" ")
        to_eval = Options()
        for signal in signals:
            to_eval.apply_signal(signal)
        output_val_string = ""
        for output in outputs: 
            digits.append(to_eval.get_number(output))
            output_val_string+=str(to_eval.get_number(output))
        output_values.append(int(output_val_string))

print("1, 4, 7 or 8 appear {} times".format(digits.count(1)+digits.count(4)+digits.count(7)+digits.count(8)))
print("Sum of output values = {}".format(sum(output_values)))