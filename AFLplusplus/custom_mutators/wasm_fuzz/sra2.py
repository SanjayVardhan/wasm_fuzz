def stack_repair(wat_instructions):
    # Define the expected stack effects for each instruction
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
    def repair_stack(op, stack):
        expected_inputs, outputs = stack_effects.get(op, ([], []))
        inserted_instructions = []
        while len(stack) < len(expected_inputs):
            # Determine the missing type
            missing_type = expected_inputs[len(stack)]
            # some sus values which can trigger corner cases}
            if missing_type == "i32":
                inserted_instructions.append("i32.const 0")
                stack.append("i32")
            elif missing_type == "i64":
                inserted_instructions.append("i64.const 0")
                stack.append("i64")
            elif missing_type == "f32":
                inserted_instructions.append("f32.const 0.0")
                stack.append("f32")
            elif missing_type == "f64":
                inserted_instructions.append("f64.const 0.0")
                stack.append("f64")

        # Perform the operation assuming all inputs are now available
        if len(stack) >= len(expected_inputs):
            # Remove the inputs from the stack
            stack = stack[:-len(expected_inputs)]
            # Push the outputs to the stack
            stack.extend(outputs)
        
        return stack, inserted_instructions

    virtual_stack = []
    repaired_instructions = []

    for instr in wat_instructions:
        op = instr.split()[0]
        virtual_stack, insert_instrs = repair_stack(op, virtual_stack)
        repaired_instructions.extend(insert_instrs)
        repaired_instructions.append(instr)

    return repaired_instructions

# Example usage
# wat_instructions = [
#     "local.get 0",
#     "i32.add",
#     "i32.const 10",
#     "i32.mul"
# ]

# # Call the stack repair function
# repaired = stack_repair(wat_instructions)
# for instr in repaired:
#     print(instr)
