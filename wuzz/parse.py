
token_list = {
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
    "f64.min", "f64.max", "f64.copysign","0x1337"
}
token_map = {instr: idx for idx, instr in enumerate(sorted(token_list))}

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

def extract_function_bodies(wat_file_content):
    function_bodies = []
    in_function = False
    current_function = []
    brace_depth = 0

    lines = wat_file_content.splitlines()
    
    for line in lines:
        line = line.strip()
        if "(func" in line:
            in_function = True
            brace_depth = 1
            current_function.append(line)
            continue
        elif in_function:
            if line.startswith("("):
                brace_depth += line.count("(")
            if line.endswith(")"):
                brace_depth -= line.count(")")
            
            current_function.append(line)

            if brace_depth == 0:
                in_function = False
                function_bodies.append("\n".join(current_function))
                current_function = []

    return function_bodies

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

# convert binary tokens to wat multiline format
def binary_to_wat(binary_tokens):
    wat_lines = []
    for idx, token in enumerate(binary_tokens):
        if idx % 2 == 0:
            operation = token_list[token]
            operands = []
            wat_lines.append(f"{operation} {', '.join(map(str, operands))}")
        else:
            operands = [token]
            wat_lines[-1] = f"{wat_lines[-1]} {', '.join(map(str, operands))}"
    
    return "\n".join(wat_lines)

def main():
    wat_file = sys.argv[1]
    wat_file_content = parse_wat(wat_file)
    function_bodies = extract_function_bodies(wat_file_content)

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
    
    wat_lines = binary_to_wat(binary_tokens)
    print(wat_lines)
    


if __name__ == "__main__":
    main()
