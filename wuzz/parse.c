#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

// Function to read the content of a file into a string
char* read_file(const char* filename) {
    FILE *file = fopen(filename, "r");
    if (!file) {
        fprintf(stderr, "Could not open file %s for reading\n", filename);
        return NULL;
    }
    fseek(file, 0, SEEK_END);
    long length = ftell(file);
    fseek(file, 0, SEEK_SET);
    char *content = malloc(length + 1);
    if (content) {
        fread(content, 1, length, file);
    }
    fclose(file);
    content[length] = '\0';
    return content;
}

// Function to extract function bodies from WAT file content
char* extract_function_body(const char* wat_file_content) {
    char *function_bodies = malloc(strlen(wat_file_content) + 1);
    function_bodies[0] = '\0';

    int in_function = 0;
    int brace_depth = 0;
    char current_function[8192] = {0};

    char *line = strtok(strdup(wat_file_content), "\n");
    while (line != NULL) {
        line = strtok(line, " \t");
        if (strstr(line, "(func")) {
            in_function = 1;
            brace_depth = 1;
            if (line[strlen(line) - 1] == '(' || line[strlen(line) - 1] == ')') {
                line = strtok(NULL, "\n");
                continue;
            }
        } else if (in_function) {
            if (line[0] == '(') brace_depth += 1;
            if (line[strlen(line) - 1] == ')') brace_depth -= 1;

            if (brace_depth > 1) {
                strcat(current_function, line);
                strcat(current_function, "\n");
            } else if (brace_depth == 1 && line[0] != ')') {
                strcat(current_function, line);
                strcat(current_function, "\n");
            }

            if (brace_depth == 0) {
                in_function = 0;
                strcat(function_bodies, current_function);
                strcat(function_bodies, "\n\n");
                current_function[0] = '\0';
            }
        }
        line = strtok(NULL, "\n");
    }

    return function_bodies;
}

// List of tokens
const char *token_list[] = {
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
    "f64.min", "f64.max", "f64.copysign"
};

// Function to tokenize function body and store them in a list
void tokenize(const char* function_code) {
    char *line = strtok(strdup(function_code), "\n");
    while (line != NULL) {
        char *token = strtok(line, " \t");
        while (token != NULL) {
            for (int i = 0; i < sizeof(token_list) / sizeof(token_list[0]); i++) {
                if (strcmp(token, token_list[i]) == 0) {
                    printf("%s\n", token);
                    break;
                }
            }
            token = strtok(NULL, " \t");
        }
        line = strtok(NULL, "\n");
    }
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <wat_file>\n", argv[0]);
        return EXIT_FAILURE;
    }

    const char *wat_filename = argv[1];
    char *wat_file_content = read_file(wat_filename);
    if (!wat_file_content) {
        return EXIT_FAILURE;
    }

    char *function_code = extract_function_body(wat_file_content);
    free(wat_file_content);

    tokenize(function_code);

    free(function_code);

    return EXIT_SUCCESS;
}
