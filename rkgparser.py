class RKG:
    def __init__(self, data: bytes):
        self.data = data
        self.byte_offset = 0
        self.bit_offset = 0

    
    def read_bits(self, bits: int) -> int:
        # bit wizardry
        value = 0

        if bits <= (8 - self.bit_offset):
            value = self.data[self.byte_offset] >> ((8 - bits) - self.bit_offset)
            mask = ~(0xFF << bits) # bit mask to remove unneccesary bits
            value &= mask
            self.bit_offset += bits
            if (self.bit_offset == 8):
                # move to next byte
                self.bit_offset = 0
                self.byte_offset += 1
            return value
        else:
            # read remaining bits if not beginning of byte

            if self.bit_offset != 0:
                bits -= 8 - self.bit_offset
                mask = ~(0xFF << (8 - self.bit_offset))
                value = self.data[self.byte_offset] & mask
                self.bit_offset = 0
                self.byte_offset += 1

            # read all full bytes
            while bits >= 8:
                value = value << 8
                value += self.data[self.byte_offset]
                self.byte_offset += 1
                bits -= 8

            # read remaining bits, if any
            if bits > 0:
                value = value << bits
                value += self.data[self.byte_offset] >> (8-bits)
                self.bit_offset += bits

        return value
    
    def skip_bits(self, bits: int) -> None:
        # skip an amount of bytes
        self.byte_offset += bits // 8
        self.bit_offset += bits % 8
        if self.bit_offset >= 8:
            self.byte_offset += 1
            self.bit_offset -= 8