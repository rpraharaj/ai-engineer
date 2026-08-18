#!/bin/sh
# Point this repo's .agents/skills at ../skills so agents opening the pack see them.
set -e

PACK_ROOT=$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)
SRC="$PACK_ROOT/skills"
DEST="$PACK_ROOT/.agents/skills"

mkdir -p "$DEST"

for skill in "$SRC"/*; do
  [ -d "$skill" ] || continue
  [ -f "$skill/SKILL.md" ] || continue
  name=$(basename "$skill")
  ln -sfn "../../skills/$name" "$DEST/$name"
done

echo "linked skills into $DEST"
