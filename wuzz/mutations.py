# Input is a binary string
# import wat_to_token
import random

mutation_rate = 0.1

def check_8bit(binary_string):
    if len(binary_string) % 8 == 0:
        return True
    else:
        # add the remaining bits to make it 8 bit alligned
        for i in range(8 - (len(binary_string) % 8)):
            binary_string = '0' + binary_string
        return binary_string

# pick 8bits in random from the string and add it in the random position
def add_mutation(binary_string):
    binary_string = list(binary_string)
    for i in range(len(binary_string)):
        if random.random() < mutation_rate:
            binary_string.insert(i, str(random.randint(0, 1)))
    return check_8bit(''.join(binary_string))

def remove_mutation(binary_string):
    binary_string = list(binary_string)
    for i in range(len(binary_string)):
        if random.random() < mutation_rate:
            binary_string.pop(i, str(random.randint(0, 1)))
    # check if the string is 8 bit alligned and return the string


    return check_8bit(''.join(binary_string))

# check if the string is 8 bit alligned

# Bit flip mutation
def bit_flip_mutation(binary_string):
    binary_string = list(binary_string)
    for i in range(len(binary_string)):
        if random.random() < mutation_rate:
            if binary_string[i] == '0':
                binary_string[i] = '1'
            else:
                binary_string[i] = '0'
    return ''.join(binary_string)

# Insertion mutation
def insertion_mutation(binary_string):
    binary_string = list(binary_string)
    for i in range(len(binary_string)):
        if random.random() < mutation_rate:
            binary_string.insert(i, str(random.randint(0, 1)))
    return check_8bit(''.join(binary_string))

# left shift mutation
def left_shift_mutation(binary_string):
    binary_string = list(binary_string)
    for i in range(len(binary_string)):
        if random.random() < mutation_rate:
            binary_string = binary_string[1:] + [binary_string[0]]
        else:
            i += 1
    return check_8bit(''.join(binary_string))