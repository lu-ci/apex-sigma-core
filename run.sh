#!/usr/bin/env bash

set -e

# Don't let CDPATH interfere with the cd command
unset CDPATH
cd "$(dirname "$0")"

# activate the python virtualenv
source ".venv/bin/activate"

# Execute the bot
#exec python ./run.py

if [ -z "$SIGMA_SHARD_COUNT" ] || [ -z "$SIGMA_SHARD_GROUP" ]; then
  echo "Environment variables not set. Running script with no arguments..."
  exec python ./run.py
  exit 0
fi

total_count=$SIGMA_SHARD_COUNT
group_size=$SIGMA_SHARD_GROUP

num_groups=$((total_count / group_size))

for ((i = 0; i < num_groups; i++)); do
  start=$((i * group_size))
  end=$((start + group_size - 1))
  shard_ids=$(seq -s, $start $end)

  exec python ./run.py --count "$total_count" --group "$shard_ids" &
done

wait