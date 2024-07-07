export PYTHONPATH=/home/sefcom/wasm_fuzz/AFLplusplus/custom_mutators/wasm_fuzz
export AFL_PYTHON_MODULE=wuzz
export AFL_CUSTOM_MUTATOR_ONLY=1
#disable afl arithmetics
./AFLplusplus/afl-fuzz -i testcases -o out -- ./wabt/build/wat2wasm @@
