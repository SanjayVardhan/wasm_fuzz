import sra2
import mutations
token_list = [
    "unreachable", "nop", "block", "loop",
    "if", "else", "try", "try_table", "throw_ref",
    "catch", "throw", "rethrow", "catch_all",
    "end", "br", "br_if", "br_table", "return",
    "call", "call_indirect", "return_call",
    "return_call_indirect", "call_ref",
    "return_call_ref", "nop_for_test", "delegate",
    "drop", "select", "select_with_type", "local.get",
    "local.set", "local.tee", "global.get", "global.set",
    "table.get", "table.set", "i32.load", "i64.load",
    "f32.load", "f64.load", "i32.load8_s", "i32.load8_u",
    "i32.load16_s", "i32.load16_u", "i64.load8_s",
    "i64.load8_u", "i64.load16_s", "i64.load16_u",
    "i64.load32_s", "i64.load32_u", "i32.store",
    "i64.store", "f32.store", "f64.store", "i32.store8",
    "i32.store16", "i64.store8", "i64.store16",
    "i64.store32", "memory.size", "memory.grow",
    "i32.const", "i64.const", "f32.const", "f64.const",
    "i32.eqz", "i32.eq", "i32.ne", "i32.lt_s", "i32.lt_u",
    "i32.gt_s", "i32.gt_u", "i32.le_s", "i32.le_u",
    "i32.ge_s", "i32.ge_u", "i64.eqz", "i64.eq", "i64.ne",
    "i64.lt_s", "i64.lt_u", "i64.gt_s", "i64.gt_u",
    "i64.le_s", "i64.le_u", "i64.ge_s", "i64.ge_u",
    "f32.eq", "f32.ne", "f32.lt", "f32.gt", "f32.le",
    "f32.ge", "f64.eq", "f64.ne", "f64.lt", "f64.gt",
    "f64.le", "f64.ge", "i32.clz", "i32.ctz", "i32.popcnt",
    "i32.add", "i32.sub", "i32.mul", "i32.div_s", "i32.div_u",
    "i32.rem_s", "i32.rem_u", "i32.and", "i32.or", "i32.xor",
    "i32.shl", "i32.shr_s", "i32.shr_u", "i32.rol", "i32.ror",
    "i64.clz", "i64.ctz", "i64.popcnt", "i64.add", "i64.sub",
    "i64.mul", "i64.div_s", "i64.div_u", "i64.rem_s", "i64.rem_u",
    "i64.and", "i64.or", "i64.xor", "i64.shl", "i64.shr_s",
    "i64.shr_u", "i64.rol", "i64.ror", "f32.abs", "f32.neg",
    "f32.ceil", "f32.floor", "f32.trunc", "f32.nearest",
    "f32.sqrt", "f32.add", "f32.sub", "f32.mul", "f32.div",
    "f32.min", "f32.max", "f32.copysign", "f64.abs", "f64.neg",
    "f64.ceil", "f64.floor", "f64.trunc", "f64.nearest",
    "f64.sqrt", "f64.add", "f64.sub", "f64.mul", "f64.div",
    "f64.min", "f64.max", "f64.copysign","0x1337"]
token_map = {instr: idx for idx, instr in enumerate(token_list)}

stack_effects = {
    "unreachable": ([], []),
    "nop": ([], []),
    "block": ([], []),
    "loop": ([], []),
    "if": ([], []),
    "else": ([], []),
    "try": ([], []),
    "try_table": ([], []),
    "throw_ref": ([], []),
    "catch": ([], []),
    "throw": ([], []),
    "rethrow": ([], []),
    "catch_all": ([], []),
    "end": ([], []),
    "br": ([], []),
    "br_if": (["i32"], []),
    "br_table": (["i32"], []),
    "return": ([], []),
    "call": ([], []),  # depends on the function signature
    "call_indirect": (["i32"], []),  # depends on the function signature
    "return_call": ([], []),  # depends on the function signature
    "return_call_indirect": (["i32"], []),  # depends on the function signature
    "call_ref": ([], []),  # depends on the function signature
    "return_call_ref": ([], []),  # depends on the function signature
    "nop_for_test": ([], []),
    "delegate": ([], []),
    "drop": (["i32"], []),  # or other types
    "select": (["i32", "i32", "i32"], ["i32"]),  # or other types
    "select_with_type": (["i32", "i32", "i32"], ["i32"]),  # or other types
    "local.get": ([], ["i32"]),  # or other types
    "local.set": (["i32"], []),  # or other types
    "local.tee": (["i32"], ["i32"]),  # or other types
    "global.get": ([], ["i32"]),  # or other types
    "global.set": (["i32"], []),  # or other types
    "table.get": (["i32"], ["i32"]),  # or other types
    "table.set": (["i32", "i32"], []),  # or other types
    "i32.load": (["i32"], ["i32"]),
    "i64.load": (["i32"], ["i64"]),
    "f32.load": (["i32"], ["f32"]),
    "f64.load": (["i32"], ["f64"]),
    "i32.load8_s": (["i32"], ["i32"]),
    "i32.load8_u": (["i32"], ["i32"]),
    "i32.load16_s": (["i32"], ["i32"]),
    "i32.load16_u": (["i32"], ["i32"]),
    "i64.load8_s": (["i32"], ["i64"]),
    "i64.load8_u": (["i32"], ["i64"]),
    "i64.load16_s": (["i32"], ["i64"]),
    "i64.load16_u": (["i32"], ["i64"]),
    "i64.load32_s": (["i32"], ["i64"]),
    "i64.load32_u": (["i32"], ["i64"]),
    "i32.store": (["i32", "i32"], []),
    "i64.store": (["i32", "i64"], []),
    "f32.store": (["i32", "f32"], []),
    "f64.store": (["i32", "f64"], []),
    "i32.store8": (["i32", "i32"], []),
    "i32.store16": (["i32", "i32"], []),
    "i64.store8": (["i32", "i64"], []),
    "i64.store16": (["i32", "i64"], []),
    "i64.store32": (["i32", "i64"], []),
    "memory.size": ([], ["i32"]),
    "memory.grow": (["i32"], ["i32"]),
    "i32.const": ([], ["i32"]),
    "i64.const": ([], ["i64"]),
    "f32.const": ([], ["f32"]),
    "f64.const": ([], ["f64"]),
    "i32.eqz": (["i32"], ["i32"]),
    "i32.eq": (["i32", "i32"], ["i32"]),
    "i32.ne": (["i32", "i32"], ["i32"]),
    "i32.lt_s": (["i32", "i32"], ["i32"]),
    "i32.lt_u": (["i32", "i32"], ["i32"]),
    "i32.gt_s": (["i32", "i32"], ["i32"]),
    "i32.gt_u": (["i32", "i32"], ["i32"]),
    "i32.le_s": (["i32", "i32"], ["i32"]),
    "i32.le_u": (["i32", "i32"], ["i32"]),
    "i32.ge_s": (["i32", "i32"], ["i32"]),
    "i32.ge_u": (["i32", "i32"], ["i32"]),
    "i64.eqz": (["i64"], ["i32"]),
    "i64.eq": (["i64", "i64"], ["i32"]),
    "i64.ne": (["i64", "i64"], ["i32"]),
    "i64.lt_s": (["i64", "i64"], ["i32"]),
    "i64.lt_u": (["i64", "i64"], ["i32"]),
    "i64.gt_s": (["i64", "i64"], ["i32"]),
    "i64.gt_u": (["i64", "i64"], ["i32"]),
    "i64.le_s": (["i64", "i64"], ["i32"]),
    "i64.le_u": (["i64", "i64"], ["i32"]),
    "i64.ge_s": (["i64", "i64"], ["i32"]),
    "i64.ge_u": (["i64", "i64"], ["i32"]),
    "f32.eq": (["f32", "f32"], ["i32"]),
    "f32.ne": (["f32", "f32"], ["i32"]),
    "f32.lt": (["f32", "f32"], ["i32"]),
    "f32.gt": (["f32", "f32"], ["i32"]),
    "f32.le": (["f32", "f32"], ["i32"]),
    "f32.ge": (["f32", "f32"], ["i32"]),
    "f64.eq": (["f64", "f64"], ["i32"]),
    "f64.ne": (["f64", "f64"], ["i32"]),
    "f64.lt": (["f64", "f64"], ["i32"]),
    "f64.gt": (["f64", "f64"], ["i32"]),
    "f64.le": (["f64", "f64"], ["i32"]),
    "f64.ge": (["f64", "f64"], ["i32"]),
    "i32.clz": (["i32"], ["i32"]),
    "i32.ctz": (["i32"], ["i32"]),
    "i32.popcnt": (["i32"], ["i32"]),
    "i32.add": (["i32", "i32"], ["i32"]),
    "i32.sub": (["i32", "i32"], ["i32"]),
    "i32.mul": (["i32", "i32"], ["i32"]),
    "i32.div_s": (["i32", "i32"], ["i32"]),
    "i32.div_u": (["i32", "i32"], ["i32"]),
    "i32.rem_s": (["i32", "i32"], ["i32"]),
    "i32.rem_u": (["i32", "i32"], ["i32"]),
    "i32.and": (["i32", "i32"], ["i32"]),
    "i32.or": (["i32", "i32"], ["i32"]),
    "i32.xor": (["i32", "i32"], ["i32"]),
    "i32.shl": (["i32", "i32"], ["i32"]),
    "i32.shr_s": (["i32", "i32"], ["i32"]),
    "i32.shr_u": (["i32", "i32"], ["i32"]),
    "i32.rol": (["i32", "i32"], ["i32"]),
    "i32.ror": (["i32", "i32"], ["i32"]),
    "i64.clz": (["i64"], ["i64"]),
    "i64.ctz": (["i64"], ["i64"]),
    "i64.popcnt": (["i64"], ["i64"]),
    "i64.add": (["i64", "i64"], ["i64"]),
    "i64.sub": (["i64", "i64"], ["i64"]),
    "i64.mul": (["i64", "i64"], ["i64"]),
    "i64.div_s": (["i64", "i64"], ["i64"]),
    "i64.div_u": (["i64", "i64"], ["i64"]),
    "i64.rem_s": (["i64", "i64"], ["i64"]),
    "i64.rem_u": (["i64", "i64"], ["i64"]),
    "i64.and": (["i64", "i64"], ["i64"]),
    "i64.or": (["i64", "i64"], ["i64"]),
    "i64.xor": (["i64", "i64"], ["i64"]),
    "i64.shl": (["i64", "i64"], ["i64"]),
    "i64.shr_s": (["i64", "i64"], ["i64"]),
    "i64.shr_u": (["i64", "i64"], ["i64"]),
    "i64.rol": (["i64", "i64"], ["i64"]),
    "i64.ror": (["i64", "i64"], ["i64"]),
    "f32.abs": (["f32"], ["f32"]),
    "f32.neg": (["f32"], ["f32"]),
    "f32.ceil": (["f32"], ["f32"]),
    "f32.floor": (["f32"], ["f32"]),
    "f32.trunc": (["f32"], ["f32"]),
    "f32.nearest": (["f32"], ["f32"]),
    "f32.sqrt": (["f32"], ["f32"]),
    "f32.add": (["f32", "f32"], ["f32"]),
    "f32.sub": (["f32", "f32"], ["f32"]),
    "f32.mul": (["f32", "f32"], ["f32"]),
    "f32.div": (["f32", "f32"], ["f32"]),
    "f32.min": (["f32", "f32"], ["f32"]),
    "f32.max": (["f32", "f32"], ["f32"]),
    "f32.copysign": (["f32", "f32"], ["f32"]),
    "f64.abs": (["f64"], ["f64"]),
    "f64.neg": (["f64"], ["f64"]),
    "f64.ceil": (["f64"], ["f64"]),
    "f64.floor": (["f64"], ["f64"]),
    "f64.trunc": (["f64"], ["f64"]),
    "f64.nearest": (["f64"], ["f64"]),
    "f64.sqrt": (["f64"], ["f64"]),
    "f64.add": (["f64", "f64"], ["f64"]),
    "f64.sub": (["f64", "f64"], ["f64"]),
    "f64.mul": (["f64", "f64"], ["f64"]),
    "f64.div": (["f64", "f64"], ["f64"]),
    "f64.min": (["f64", "f64"], ["f64"]),
    "f64.max": (["f64", "f64"], ["f64"]),
    "f64.copysign": (["f64", "f64"], ["f64"]),
}

import sys
import os
import re
import json
import random
import networkx as nx

def parse_wat(wat_file):
    with open(wat_file, 'r') as f:
        lines = f.read()
    return lines

def extract_function_bodies(wat_content):
    """Extracts all function bodies from a WAT file, and stores their positions."""
    function_bodies = []
    start_positions = []
    end_positions = []
    in_function = False
    current_function = []
    brace_depth = 0
    lines = wat_content.split('\n')
    
    for i, line in enumerate(lines):
        stripped_line = line.strip()
        if "(func" in stripped_line:
            if not in_function:
                start_positions.append(i)
                in_function = True
                brace_depth = 1
            current_function.append(line)
        elif in_function:
            if stripped_line.startswith("("):
                brace_depth += stripped_line.count("(")
            if stripped_line.endswith(")"):
                brace_depth -= stripped_line.count(")")
            current_function.append(line)
            if brace_depth == 0:
                end_positions.append(i)
                function_bodies.append("\n".join(current_function))
                current_function = []
                in_function = False

    return function_bodies, start_positions, end_positions

def replace_function_in_wat(original_wat, start, end, new_function_body):
    """Replaces a function in the WAT file with new content."""
    wat_lines = original_wat.split('\n')
    new_wat = wat_lines[:start] + new_function_body.split('\n') + wat_lines[end + 1:]
    return '\n'.join(new_wat)

def replace_function_body_by_index(wat_content, func_index, new_instructions):
    """
    Replace the body of a specific function by index in WAT content.

    :param wat_content: Original WAT content as a string.
    :param func_index: The index (0-based) of the function to target.
    :param new_instructions: List of new instructions as strings to be placed within the function.
    :return: Modified WAT content.
    """
    lines = wat_content.split('\n')
    current_func_index = -1  # Start with -1 to make first function index 0
    inside_target_func = False
    modified_content = []
    start_replace = False

    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith("(func"):
            current_func_index += 1
            modified_content.append(line)
            if current_func_index == func_index:
                inside_target_func = True
        elif stripped_line.startswith(")") and inside_target_func:
            # Insert new instructions before closing the function
            modified_content.extend(["    " + instr for instr in new_instructions])
            modified_content.append(line)
            inside_target_func = False  # Exit function
        elif inside_target_func:
            if stripped_line.startswith("(") and not start_replace:
                # Keep function signature and other configurations intact
                modified_content.append(line)
            # Skip appending old instructions; they will be replaced
            start_replace = True
        else:
            modified_content.append(line)

    return '\n'.join(modified_content)




# token_list = {
# ......
# }
# token_map = {instr: idx for idx, instr in enumerate(sorted(token_list))}

def tokenize_function_body(function_body):

    lines = function_body.split("\n")
    tokens = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        parts = line.split()
        operation = parts[0]

        if operation in token_list:
            operands = parts[1:] if len(parts) > 1 else []
            operands = [int(op, 16) if op.startswith('0x') else
                        int(op) if op.isdigit() else
                        float(op) if op.replace('.', '', 1).isdigit() else
                        op
                        for op in operands]
            tokens.append({"operation": operation, "operands": operands})
        else:
            continue

    return tokens


#   std::string js = "var wasm_code = new Uint8Array([";
#   for(auto it:output) {
#     js += std::to_string((int)(it));
#     js += ',';
#   }

#   js.pop_back();
#   js += "]);\n"
#         "var wasm_module = new WebAssembly.Module(wasm_code);\n"
#         "var wasm_instance = new WebAssembly.Instance(wasm_module);\n"
#         "var f = wasm_instance.exports.main;\n"
#         "f();\n";


def process_numbers(tokens):
    modified_tokens = []
    
    for token in tokens:
        operation = token['operation']
        operands = token['operands']
        modified_operands = []
        
        for op in operands:
            if isinstance(op, int):
                modified_operands.append("0x1337")
            else:
                modified_operands.append(op)
        
        modified_token = {"operation": operation, "operands": modified_operands}
        modified_tokens.append(modified_token)
    
    return modified_tokens

def process_variable_names(tokens):
    modified_tokens = []
    var_map = {}
    
    for token in tokens:
        operation = token['operation']
        operands = token['operands']
        modified_operands = []
        
        for op in operands:
            if isinstance(op, str) and op.startswith('$'):
                if op in var_map:
                    modified_operands.append(var_map[op])
                else:
                    var_count = len(var_map) + 1
                    var_name = f'var{var_count}'
                    var_map[op] = var_name
                    modified_operands.append(var_name)
            else:
                modified_operands.append(op)
        
        modified_token = {"operation": operation, "operands": modified_operands}
        modified_tokens.append(modified_token)
    
    return modified_tokens

def process_wat_file(tokens):
    tokens = process_numbers(tokens)
    tokens = process_variable_names(tokens)
    return tokens

def create_function_graph(function_bodies):
    G = nx.DiGraph()
    for idx, function_body in enumerate(function_bodies):
        function_name = f"func_{idx + 1}"
        G.add_node(function_name, body=function_body)
    
    # Optionally, you can add edges if there are dependencies between functions
    # For example, if func_1 calls func_2, you can add an edge like this:
    # G.add_edge('func_1', 'func_2')
    
    return G

def binary_to_wat(binary_tokens, token_list):
    idx_to_token = {idx: token for idx, token in enumerate(token_list)}
    wat_lines = []
    i = 0
    while i < len(binary_tokens):
        token_idx = binary_tokens[i]
        if token_idx in idx_to_token:
            operation = idx_to_token[token_idx]
            i += 1
            if i < len(binary_tokens) and binary_tokens[i] == 0x1337:
                operand = "0x1337"
                wat_lines.append(f"{operation} {operand}".strip())
                i += 1
            else:
                wat_lines.append(f"{operation}".strip())
        else:
            wat_lines.append(f"0x{token_idx:x}")
            i += 1

    return wat_lines

def format_tokens(token_list):
    # This will store the formatted output
    formatted_tokens = []
    i = 0
    
    # Iterate through the list of tokens
    while i < len(token_list):
        # If this is the last token or if the next token is not a number, simply add it
        if i == len(token_list) - 1 or not token_list[i+1].startswith("0x"):
            formatted_tokens.append(token_list[i])
        else:
            # Otherwise, concatenate this token with the next one and skip the next token
            formatted_tokens.append(f"{token_list[i]} {token_list[i+1]}")
            i += 1  # Skip the next token since it's concatenated
        i += 1
    
    return formatted_tokens


# Example usage
# binary_tokens = [61, 0x1337, 61, 0x1337, 50]  # Example binary tokens
# wat_multiline = binary_to_wat(binary_tokens, token_list)
# print(wat_multiline)


    # return wat_lines


def main():
    wat_file = sys.argv[1]
    wat_file_content = parse_wat(wat_file)
    function_bodies, starts, ends = extract_function_bodies(wat_file_content)

    # Create a graph of functions
    G = create_function_graph(function_bodies)

    # Randomly choose a function from the graph to tokenize
    chosen_function = random.choice(list(G.nodes))
    function_body = G.nodes[chosen_function]['body']

    tokens = tokenize_function_body(function_body)
    tokens = process_wat_file(tokens)
    
    print(f"Chosen Function: {chosen_function}")
    print(json.dumps(tokens, indent=4))

    # convert the tokens to 16bit binary representation
    binary_tokens = []
    for token in tokens:
        operation = token['operation']
        operands = token['operands']
        operation_idx = token_map[operation]
        binary_tokens.append(operation_idx)
        for op in operands:
            if isinstance(op, int):
                binary_tokens.append(op)
            else:
                binary_tokens.append(token_map[op])
            
    print(binary_tokens)


    print("binary tokens -->" + str(binary_tokens))
    
    binary_string = ''.join(format(byte, '08b') for byte in binary_tokens)
    # binary string to raw binary
    # binary_string = bytes([int(binary_string[i:i+8], 2) for i in range(0, len(binary_string), 8)])
    
    print(binary_string)
    if(len(binary_string) % 8 != 0):
        print("Not 16bit aligned")
    def binary_to_int_array(binary_string):
    # Split the binary string into 8-bit chunks
        chunks = [binary_string[i:i+8] for i in range(0, len(binary_string), 8)]
    # Convert each chunk to an integer
        return [int(chunk, 2) for chunk in chunks]

# Reconstruction of the wat file from the binary tokens
    # call the mutation functions in mutations.py randomly on 
    # binary_string = mutations.left_shift_mutation(binary_string)
    # select a mutation function randomly and apply it to the binary string
    random_mutation = random.choice([mutations.add_mutation, mutations.remove_mutation, mutations.bit_flip_mutation, mutations.insertion_mutation])
    binary_string = random_mutation(binary_string)
    print(binary_string)
    int_bin = binary_to_int_array(binary_string)
    print(int_bin)
    wat_lines = binary_to_wat(int_bin, token_list)
    wat_lines = format_tokens(wat_lines)
    stack_repair = sra2.stack_repair(wat_lines)
    print("lol")
    print(stack_repair)
    print(wat_lines)

    idx = int(chosen_function.split('_')[1]) -1
    # chosen_func = f"func_{idx}"
    # print(chosen_func)
    print(idx)
    updated_wat_content = replace_function_body_by_index(wat_file_content, idx, stack_repair)

    print(updated_wat_content)

# place the function body back into the original wat file

if __name__ == "__main__":
    main()
