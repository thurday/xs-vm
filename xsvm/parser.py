from pyparsing import *
from instructions import supported_instructions, Instruction

label_definition = Word(alphanums + "_")
mnemonic_definition = oneOf(" ".join(supported_instructions), caseless=True)
register_definition = Combine(CaselessLiteral("r") + Word(nums))
constant_definition = Combine(Literal("#") + Word(nums))


def parse_line(line):
    instruction_definition = Forward()

    instruction_definition << Optional(label_definition.setResultsName("label") + FollowedBy(mnemonic_definition)) + mnemonic_definition.setResultsName("mnemonic") \
                              + Optional(Group(delimitedList(register_definition | label_definition | constant_definition, ","))).setResultsName("operands")

    parsed_line = instruction_definition.parseString(line)

    label = parsed_line.label
    if label == "":
        label = None

    mnemonic = parsed_line.mnemonic
    if mnemonic == "":
        mnemonic = None

    if parsed_line.operands == "":
        operands = None
    else:
        operands = parsed_line.operands[0]

    parsed_instruction = Instruction(label=label, mnemonic=mnemonic, operands=operands)

    return parsed_instruction