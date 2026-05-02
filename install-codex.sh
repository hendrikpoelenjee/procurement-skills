#!/bin/bash
# Install TPO skills for OpenAI Codex (CLI / IDE / app).
# Official layout: https://developers.openai.com/codex/skills
set -e

USER_SKILLS_DIR="${HOME}/.agents/skills"
USER_STANDARDS_DIR="${HOME}/.agents/standards"
CODEX_DIR="${HOME}/.codex"
CODEX_AGENTS="${CODEX_DIR}/AGENTS.md"
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

MARKER="# TPO Procurement Skills — Codex"

echo ""
echo "TPO Procurement Skills — Codex installer"
echo "========================================"
echo ""
echo "Target (OpenAI Codex user skills):"
echo "  Skills:    ${USER_SKILLS_DIR}"
echo "  Standards: ${USER_STANDARDS_DIR}"
echo ""

mkdir -p "${USER_SKILLS_DIR}" "${USER_STANDARDS_DIR}"

echo "Installing standards ..."
rsync -a "${REPO_DIR}/standards/" "${USER_STANDARDS_DIR}/"
echo "  + ${USER_STANDARDS_DIR}/ (interaction-patterns, artifact-*, etc.)"

echo ""
echo "Installing validators + eval suites to ~/.agents/ ..."
echo "  (Per-skill scripts/validate.py calls ~/.agents/tools/validators/validate_skill.py;"
echo "   eval checks use ~/.agents/evals/<skill>/cases.json — same layout as repo.)"
mkdir -p "${HOME}/.agents/tools/validators"
rsync -a --delete "${REPO_DIR}/tools/validators/" "${HOME}/.agents/tools/validators/"
touch "${HOME}/.agents/tools/validators/.installed_by_tpo_procurement_pack"
mkdir -p "${HOME}/.agents/evals"
rsync -a "${REPO_DIR}/evals/" "${HOME}/.agents/evals/"
echo "  + ${HOME}/.agents/tools/validators/"
echo "  + ${HOME}/.agents/evals/"

echo ""
echo "Installing skills ..."
for skill_dir in "${REPO_DIR}"/skills/p9t-*/; do
  skill_name="$(basename "${skill_dir}")"
  rsync -a "${skill_dir}" "${USER_SKILLS_DIR}/${skill_name}/"
  echo "  + ${skill_name}"
done

echo ""
echo "Optional: user-level Codex AGENTS.md (${CODEX_AGENTS})"
if [ -d "${CODEX_DIR}" ]; then
  if [ -f "${CODEX_AGENTS}" ] && grep -qF "${MARKER}" "${CODEX_AGENTS}"; then
    echo "  ${CODEX_AGENTS} already contains TPO block — skipping."
  else
    if [ -f "${CODEX_AGENTS}" ]; then
      {
        echo ""
        echo "---"
        echo ""
        cat "${REPO_DIR}/codex/AGENTS-append.md"
      } >> "${CODEX_AGENTS}"
      echo "  Appended TPO block to existing ${CODEX_AGENTS}"
    else
      mkdir -p "${CODEX_DIR}"
      cp "${REPO_DIR}/codex/AGENTS-append.md" "${CODEX_AGENTS}"
      echo "  Created ${CODEX_AGENTS}"
    fi
  fi
else
  echo "  ~/.codex not found — skipping (Codex will still load skills from ${USER_SKILLS_DIR})."
  echo "  To add user-level instructions later, create ~/.codex and re-run this script,"
  echo "  or merge AGENTS.snippet.md into a project AGENTS.md file."
fi

echo ""
echo "Done. Restart Codex if skills do not appear."
echo ""
echo "Invoke skills explicitly (e.g. from skill picker) or by name:"
echo "  p9t-intake-and-brief, p9t-run-sourcing-workflow, ..."
echo ""
echo "Project-level AGENTS.md: copy or merge AGENTS.snippet.md from this repo."
echo ""
