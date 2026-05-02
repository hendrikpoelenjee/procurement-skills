#!/bin/bash
set -e

SKILLS_DIR="$HOME/.claude/skills"
CLAUDE_MD="$HOME/.claude/CLAUDE.md"
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo ""
echo "TPO Procurement Skills — installer"
echo "==================================="

# 1. Check Claude Code is present
if [ ! -d "$HOME/.claude" ]; then
  echo ""
  echo "ERROR: ~/.claude not found."
  echo "Claude Code must be installed first: https://claude.ai/code"
  exit 1
fi

# 2. Install standards
echo ""
echo "Installing interaction standards to ~/.claude/standards/ ..."
mkdir -p "$HOME/.claude/standards"
rsync -a "$REPO_DIR/standards/" "$HOME/.claude/standards/"
echo "  + standards/interaction-patterns.md"
echo "  + standards/artifact-placement.md"

# 3. Install skills
echo ""
echo "Installing skills to $SKILLS_DIR ..."
mkdir -p "$SKILLS_DIR"

for skill_dir in "$REPO_DIR"/skills/p9t-*/; do
  skill_name=$(basename "$skill_dir")
  rsync -a "$skill_dir" "$SKILLS_DIR/$skill_name/"
  echo "  + $skill_name"
done

# 3a. Deploy validators + eval suites (needed for scripts/validate.py in each skill)
echo ""
echo "Installing validators + eval suites to \$HOME/.claude/ ..."
echo "  (Per-skill scripts/validate.py calls ~/.claude/tools/validators/validate_skill.py;"
echo "   eval checks use ~/.claude/evals/<skill>/cases.json — same layout as repo.)"
mkdir -p "$HOME/.claude/tools/validators"
rsync -a --delete "$REPO_DIR/tools/validators/" "$HOME/.claude/tools/validators/"
# Marker so uninstall can remove validator tree without nuking unrelated tools
touch "$HOME/.claude/tools/validators/.installed_by_tpo_procurement_pack"
mkdir -p "$HOME/.claude/evals"
# No --delete: preserve any non-pack eval folders a user may keep under ~/.claude/evals/
rsync -a "$REPO_DIR/evals/" "$HOME/.claude/evals/"
echo "  + ~/.claude/tools/validators/"
echo "  + ~/.claude/evals/"

# 3b. Deploy path config
echo ""
echo "Deploying path config to $SKILLS_DIR/skills-config.yaml ..."
cp "$REPO_DIR/skills-config.yaml" "$SKILLS_DIR/skills-config.yaml"
echo "  + skills-config.yaml"

# 4. Install CLAUDE.md (guided execution mode instruction)
echo ""
echo "Installing CLAUDE.md (conversational interview mode) ..."

MARKER="# Skill Execution Standard"

if [ -f "$CLAUDE_MD" ] && grep -qF "$MARKER" "$CLAUDE_MD"; then
  echo "  CLAUDE.md already contains skill conversation rules — skipping."
else
  if [ -f "$CLAUDE_MD" ]; then
    echo "" >> "$CLAUDE_MD"
    echo "---" >> "$CLAUDE_MD"
    echo "" >> "$CLAUDE_MD"
    cat "$REPO_DIR/CLAUDE.md" >> "$CLAUDE_MD"
    echo "  Appended to existing $CLAUDE_MD"
  else
    cp "$REPO_DIR/CLAUDE.md" "$CLAUDE_MD"
    echo "  Created $CLAUDE_MD"
  fi
fi

# 5. Register paths in global CLAUDE.md so they are always in context
echo ""
echo "Registering sourcing paths in $CLAUDE_MD ..."

PATH_MARKER="# Sourcing Skills — Path Configuration"

if grep -qF "$PATH_MARKER" "$CLAUDE_MD" 2>/dev/null; then
  echo "  Path block already present in CLAUDE.md — skipping."
else
  CONFIG_FILE="$SKILLS_DIR/skills-config.yaml"
  PROJECT_ROOT=$(grep "^project_root:" "$CONFIG_FILE" | awk '{print $2}')
  ORG_CONFIG=$(grep "^org_config_path:" "$CONFIG_FILE" | awk '{print $2}')

  cat >> "$CLAUDE_MD" <<EOF

---

$PATH_MARKER
Sourcing project root: $PROJECT_ROOT
Org config (standing constraints, approval authority, must-haves): $ORG_CONFIG
Skills config: $SKILLS_DIR/skills-config.yaml
EOF
  echo "  Appended path block to $CLAUDE_MD"
fi

# 6. Done
echo ""
echo "Done. Restart Claude Code and try:"
echo ""
echo "  /p9t-intake-and-brief"
echo "  /p9t-complexity-triage"
echo "  /p9t-run-sourcing-workflow"
echo ""
