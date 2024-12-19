
import struct


PROLOGUE = """
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
"""

EPILOGUE = r"""
int main(int argc, const char *argv[]) {
	if (argc != 2) {
		printf("Usage: %%s <flag>\n", argv[0]);
		return 0;
	}

	if (strlen(argv[1]) == %i && %s) {
		printf("Correct!\n");
	}
	else {
		printf("Wrong :(\n");
	}
	return 0;
}
"""

FUNCTION_HEADER = """
bool check%i(__int128 flag) {
	float v[1000];
	for (int i = 0; i < 128; i++) {
		int x = (!(flag & 1)) << 31;
		v[i] = *(float *)&x;
		flag >>= 1;
	}
"""


class Random:
	def __init__(self, state):
		self.state = state
	
	def u32(self):
		temp = self.state[0]
		temp = (temp ^ (temp << 11)) & 0xFFFFFFFF
		temp ^= temp >> 8
		temp ^= self.state[3]
		temp ^= self.state[3] >> 19
		self.state[0] = self.state[1]
		self.state[1] = self.state[2]
		self.state[2] = self.state[3]
		self.state[3] = temp
		return temp


class CodeGenerator:
	def __init__(self):
		self.index = 0
		self.level = 0
		self.code = ""
	
	def alloc(self):
		self.index += 1
		return self.index
	
	def indent(self): self.level += 1
	def unindent(self): self.level -= 1

	def get(self): return self.code

	def write(self, code):
		self.code += code
	
	def writeline(self, code):
		self.write("\t" * self.level + code + "\n")
	
	def assign(self, target, source):
		for i in range(len(target)):
			x, y = target[i], source[i]
			flip = (x < 0) ^ (y < 0)
			self.writeline(f"v[{abs(x) - 1}] = {"-" * flip}v[{abs(y) - 1}];")

	def not_(self, x):
		return -x
	
	def or_(self, x, y):
		d = self.alloc()
		x = f"{"-" * (x < 0)}v[{abs(x) - 1}]"
		y = f"{"-" * (y >= 0)}v[{abs(y) - 1}]"
		self.writeline(f"v[{d - 1}] = {x} - {y};")
		return d
	
	def nor(self, x, y):
		return -self.or_(x, y)

	def and_(self, x, y):
		return self.nor(-x, -y)
	
	def nand(self, x, y):
		return -self.and_(x, y)
	
	def xor(self, x, y):
		return self.nor(self.nor(x, y), self.and_(x, y))

	def return_(self, x):
		self.writeline(f"return {"!" * (x >= 0)}*(int *)&v[{abs(x) - 1}];")


FLAG = b"wwf{doe5_Z3ro_EQu4L_M1nuS_Zero?}"

code = PROLOGUE

for index in range(len(FLAG) // 16):
	block = FLAG[index*16:(index+1)*16][::-1]

	state = list(struct.unpack(">4I", block))
	rng = Random(state)

	for i in range(16):
		rng.u32()

	output = struct.pack(">4I", *rng.state)
	expected_result = int.from_bytes(output, "big")

	generator = CodeGenerator()
	generator.write(FUNCTION_HEADER %(index + 1))
	generator.indent()

	generator.writeline("for (int i = 0; i < 16; i++) {")
	generator.indent()

	state = []
	for i in range(4):
		vars = []
		for j in range(32):
			vars.append(generator.alloc())
		state.append(vars[::-1])
	state = state[::-1]

	temp = list(state[0])
	for i in range(21):
		temp[i] = generator.xor(temp[i], temp[i + 11])
	for i in range(24):
		temp[31 - i] = generator.xor(temp[31 - i], temp[31 - i - 8])
	for i in range(32):
		temp[i] = generator.xor(temp[i], state[3][i])
	for i in range(13):
		temp[i + 19] = generator.xor(temp[i + 19], state[3][i])
	generator.assign(state[0], state[1])
	generator.assign(state[1], state[2])
	generator.assign(state[2], state[3])
	generator.assign(state[3], temp)

	generator.unindent()
	generator.writeline("}")

	bits = []
	for s in state:
		bits += s

	mask = bits[0]
	if not expected_result & (1 << 127):
		mask = generator.not_(mask)
	expected_result <<= 1

	for bit in bits[1:]:
		if not expected_result & (1 << 127):
			bit = generator.not_(bit)
		expected_result <<= 1
		mask = generator.and_(mask, bit)

	generator.return_(mask)

	generator.unindent()
	generator.writeline("}")
	
	code += generator.get()

checks = " && ".join(f"check{i+1}(*((__int128 *)argv[1] + {i}))" for i in range(len(FLAG) // 16))
code += EPILOGUE %(len(FLAG), checks)

with open("challenge.c", "w") as f:
	f.write(code)
