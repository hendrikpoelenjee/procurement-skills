#!/bin/bash
set -e

# Removes only skills listed in manifest/p9t-pack-skills.txt (this pack).
# Other directories under ~/.claude/skills/ named p9t-* are left untouched.

SKILLS_DIR="${HOME}/.claude/skills"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MANIFEST="${SCRIPT_DIR}/manifest/p9t-pack-skills.txt"

echo ""
echo "TPO Procurement Skills — uninstaller"
echo "======================================"
echo ""

if [ ! -f "${MANIFEST}" ]; then
  echo "ERROR: Manifest not found: ${MANIFEST}"
  echo "Run this script from the procurement-skills repository (clone), e.g.:"
  echo "  cd procurement-skills && bash uninstall.sh"
  exit 1
fi

removed=0
while IFS= read -r skill_name || [ -n "${skill_name}" ]; do
  [ -z "${skill_name}" ] && continue
  target="${SKILLS_DIR}/${skill_name}"
  if [ -d "${target}" ]; then
    rm -rf "${target}"
    echo "  - removed ${skill_name}"
    removed=$((removed + 1))
  fi
done < <(grep -v '^[[:space:]]*#' "${MANIFEST}" | grep -v '^[[:space:]]*$')

VALIDATOR_MARKER="${HOME}/.claude/tools/validators/.installed_by_tpo_procurement_pack"
if [ -f "${VALIDATOR_MARKER}" ]; then
  echo ""
  echo "Removing validators + eval suites installed by this pack (marked at ${VALIDATOR_MARKER}) ..."
  rm -rf "${HOME}/.claude/tools/validators"
  echo "  - removed ~/.claude/tools/validators/"
fi

while IFS= read -r skill_name || [ -n "${skill_name}" ]; do
  [ -z "${skill_name}" ] && continue
  eval_dir="${HOME}/.claude/evals/${skill_name}"
  if [ -d "${eval_dir}" ]; then
    rm -rf "${eval_dir}"
    echo "  - removed ~/.claude/evals/${skill_name}"
  fi
done < <(grep -v '^[[:space:]]*#' "${MANIFEST}" | grep -v '^[[:space:]]*$')

rmdir "${HOME}/.claude/evals" 2>/dev/null || true
rmdir "${HOME}/.claude/tools" 2>/dev/null || true

if [ "${removed}" -eq 0 ]; then
  echo "No installed pack skills found under ${SKILLS_DIR} — nothing removed."
  echo "(Other p9t-* folders, if any, were not touched.)"
else
  echo ""
  echo "Removed ${removed} pack skill(s). Restart Claude Code to apply."
fi
echo ""
