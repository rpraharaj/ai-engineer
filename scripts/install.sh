#!/bin/sh
# Symlink this pack's skills into ~/.agents/skills (one source of truth).
set -e

PACK_ROOT=$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)
SRC="$PACK_ROOT/skills"
DEST="${HOME}/.agents/skills"

if [ ! -d "$SRC" ]; then
  echo "install.sh: no skills directory at $SRC" >&2
  exit 1
fi

mkdir -p "$DEST"

linked=0
skipped=0
for skill in "$SRC"/*; do
  [ -d "$skill" ] || continue
  [ -f "$skill/SKILL.md" ] || continue
  name=$(basename "$skill")
  target="$DEST/$name"
  if [ -e "$target" ] && [ ! -L "$target" ]; then
    echo "skip $name: $target exists and is not a symlink"
    skipped=$((skipped + 1))
    continue
  fi
  ln -sfn "$skill" "$target"
  echo "linked $name -> $target"
  linked=$((linked + 1))
done

echo "done: $linked linked, $skipped skipped"
echo "If an agent ignores ~/.agents/skills, symlink individual skills into that agent's skills directory."
