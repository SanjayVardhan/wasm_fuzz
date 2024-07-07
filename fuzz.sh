#!/bin/bash

export PYTHONPATH=/home/sefcom/AFLplusplus/custom_mutators/wasm_fuzz
export AFL_PYTHON_MODULE=wuzz
export AFL_CUSTOM_MUTATOR_ONLY=1

INSTANCES=$1
SESSION_NAME="afl"

# Function to create a new window with 4 panes and run fuzzers
create_fuzzer_window() {
  local window_index=$1
  local start_index=$2

  tmux new-window -t $SESSION_NAME -n "fuzzers_$window_index"

  for ((i=0; i<4; i++)); do
    local fuzzer_index=$((start_index + i))
    if [ $fuzzer_index -ge $INSTANCES ]; then
      break
    fi

    if [ $i -eq 0 ]; then
      tmux send-keys "./AFLplusplus/afl-fuzz -S fuzzer$fuzzer_index -i testcases -o out -- ./wabt/build/wat2wasm @@" C-m
    else
      tmux split-window -t "$SESSION_NAME:fuzzers_$window_index"
      tmux send-keys "./AFLplusplus/afl-fuzz -S fuzzer$fuzzer_index -i testcases -o out -- ./wabt/build/wat2wasm @@" C-m
    fi
  done
  tmux select-layout -t "$SESSION_NAME:fuzzers_$window_index" tiled
}

# Create a new tmux session with the first window for fuzzer stats
tmux new-session -d -s $SESSION_NAME -n "stats"
tmux send-keys "watch -n 1 ./AFLplusplus/afl-whatsup out" C-m

# Start creating windows with 4 panes each for the fuzzer instances
window_index=1
instance_index=0

while [ $instance_index -lt $INSTANCES ]; do
  create_fuzzer_window $window_index $instance_index
  window_index=$((window_index + 1))
  instance_index=$((instance_index + 4))
done

# Attach to the tmux session
tmux attach-session -t $SESSION_NAME

# Wait for user input to stop the fuzzers
read -p "Press 'k' to stop all fuzzers and end the session... " input

# Check if the input is 'k'
if [ "$input" == "k" ]; then
  # Send SIGINT to all panes in the session
  for pane in $(tmux list-panes -s -F '#{pane_id}'); do
    tmux send-keys -t $pane C-c
  done

  # Kill the tmux session
  tmux kill-session -t $SESSION_NAME
fi
