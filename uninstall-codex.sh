#!/bin/bash
# Removes only skills listed in manifest/p9t-pack-skills.txt from ~/.agents/skills.
set -e

USER_SKILLS_DIR="${HOME}/.agents/skills"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MANIFEST="${SCRIPT_DIR}/manifest/p9t-pack-skills.txt"

echo ""
echo "TPO Procurement Skills — Codex uninstaller"
echo "==========================================="
echo ""

if [ ! -f "${MANIFEST}" ]; then
  echo "ERROR: Manifest not found: ${MANIFEST}"
  echo "Run this script from the procurement-skills repository (clone), e.g.:"
  echo "  cd procurement-skills && bash uninstall-codex.sh"
  exit 1
fi

removed=0
while IFS= read -r skill_name || [ -n "${skill_name}" ]; do
  [ -z "${skill_name}" ] && continue
  target="${USER_SKILLS_DIR}/${skill_name}"
  if [ -d "${target}" ]; then
    rm -rf "${target}"
    echo "  - removed ${skill_name}"
    removed=$((removed + 1))
  fi
done < <(grep -v '^[[:space:]]*#' "${MANIFEST}" | grep -v '^[[:space:]]*$')

VALIDATOR_MARKER="${HOME}/.agents/tools/validators/.installed_by_tpo_procurement_pack"
if [ -f "${VALIDATOR_MARKER}" ]; then
  echo ""
  echo "Removing validators + eval suites installed by this pack (marked at ${VALIDATOR_MARKER}) ..."
  rm -rf "${HOME}/.agents/tools/validators"
  echo "  - removed ~/.agents/tools/validators/"
fi

while IFS= read -r skill_name || [ -n "${skill_name}" ]; do
  [ -z "${skill_name}" ] && continue
  eval_dir="${HOME}/.agents/evals/${skill_name}"
  if [ -d "${eval_dir}" ]; then
    rm -rf "${eval_dir}"
    echo "  - removed ~/.agents/evals/${skill_name}"
  fi
done < <(grep -v '^[[:space:]]*#' "${MANIFEST}" | grep -v '^[[:space:]]*$')

rmdir "${HOME}/.agents/evals" 2>/dev/null || true
rmdir "${HOME}/.agents/tools" 2>/dev/null || true

if [ "${removed}" -eq 0 ]; then
  echo "No installed pack skills found under ${USER_SKILLS_DIR} — nothing removed."
  echo "(Other p9t-* folders, if any, were not touched.)"
else
  echo ""
  echo "Removed ${removed} pack skill(s) from ${USER_SKILLS_DIR}. Restart Codex to apply."
  echo "Standards in ~/.agents/standards/ were not removed (may be shared)."
fi
echo ""
