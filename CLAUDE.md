# CLAUDE.md - AI Assistant Guide for aiqe

## Project Overview

**AI Query Enhancer (aiqe)** is a flexible Python tool that enhances queries sent to various AI coding assistants. It automatically adds contextual information like current year references, technical focus, or regional context to improve the relevance and accuracy of AI responses.

**Project Purpose:** "vibecoding ahoy!" - streamline AI interactions by automatically enriching queries with relevant context

**License:** The Unlicense (public domain)

---

## Repository Structure

```
aiqe/
├── ai_query_enhancer.py      # Main CLI tool (primary implementation)
├── claude_year_hook.py        # Claude Code PreToolUse hook
├── aiqe.py                    # Minimal starter script (placeholder)
├── shell_functions.sh         # Bash/Zsh integration functions
├── integration_examples.md    # Detailed integration examples
├── Makefile                   # Setup automation
├── README.md                  # Brief project description
└── LICENSE                    # The Unlicense
```

### File Organization
- **Flat structure**: All source files in root directory
- **No subdirectories**: No tests/, src/, docs/ folders
- **No config files**: No setup.py, pyproject.toml, or requirements.txt
- **PEP 723 metadata**: Dependencies declared in script headers using `# /// script` blocks

---

## Core Architecture

### Main Components

#### 1. ai_query_enhancer.py
**Purpose:** Primary CLI tool for query enhancement across multiple AI platforms

**Key Features:**
- Multi-tool support (Claude, Codex, Gemini, Cursor, Copilot)
- Multiple enhancement modes
- JSON stdin/stdout for hook integration
- Click-based CLI interface

**Supported Tools (ToolType enum):**
- `claude` - Claude Code integration
- `codex` - OpenAI Codex CLI
- `gemini` - Google Gemini CLI
- `cursor` - Cursor IDE
- `copilot` - GitHub Copilot

**Enhancement Modes (EnhancementMode enum):**
- `year-append` - Adds current year if no temporal context exists
- `context-inject` - Injects custom contextual information
- `tech-focus` - Adds modern development practices focus
- `au-context` - Adds Australian regional context

**Key Functions:**
- `has_year_reference()` - Detects year patterns (20XX)
- `has_temporal_keywords()` - Detects recency keywords (latest, recent, current, etc.)
- `enhance_query()` - Applies selected enhancement mode
- `format_for_tool()` - Formats output for specific AI tool

#### 2. claude_year_hook.py
**Purpose:** Claude Code PreToolUse hook implementation

**Behavior:**
- Reads JSON from stdin (Claude hook input)
- Checks for year reference or temporal keywords
- Appends current year if neither exists
- Outputs modified tool input as JSON to stdout
- Gracefully handles errors (passes through unchanged on failure)

**Hook Integration:**
```bash
claude config set hooks.preToolUse ./claude_year_hook.py
```

#### 3. shell_functions.sh
**Purpose:** Bash/Zsh convenience functions

**Functions:**
- `ai_ask <tool> <mode> <query>` - Generic enhancer wrapper
- `claude_ask <query>` - Claude with year-append
- `codex_ask <query>` - Codex with tech-focus
- `gemini_ask <query>` - Gemini with tech-focus
- `au_ask <query>` - Claude with Australian context

---

## Development Workflows

### Making Changes

#### 1. Modifying Enhancement Logic
**Location:** ai_query_enhancer.py:40-94

When adding new enhancement modes:
1. Add enum to `EnhancementMode` class (line 33)
2. Create enhancement function following pattern:
   ```python
   def enhance_with_<name>(query: str) -> str:
       """Description."""
       # Enhancement logic
       return enhanced_query
   ```
3. Add case to `enhance_query()` function (line 84)
4. Update CLI help text and documentation

#### 2. Adding New Tool Support
**Location:** ai_query_enhancer.py:25-31, 97-123

Steps:
1. Add to `ToolType` enum
2. Implement format function in `format_for_tool()`
3. Document output format in integration_examples.md
4. Add shell function shortcut if needed

#### 3. Updating Claude Hook
**Location:** claude_year_hook.py

Critical considerations:
- Must read JSON from stdin
- Must output valid JSON to stdout
- Must handle errors gracefully (pass through unchanged)
- Follow Claude hook spec for PreToolUse event
- Test with: `echo '{"tool_input":{"query":"test"}}' | ./claude_year_hook.py`

### Testing Workflow

#### Manual Testing
```bash
# Test year-append mode
python3 ai_query_enhancer.py --tool claude --mode year-append "python tutorials"

# Test context-inject mode
python3 ai_query_enhancer.py --tool codex --mode context-inject --context "TypeScript project" "error handling"

# Test Claude hook
echo '{"tool_input":{"query":"test query"}}' | ./claude_year_hook.py

# Run all tests via Makefile
make test
```

#### Expected Behaviors
- Queries without years/temporal keywords → year appended
- Queries with "latest", "recent", etc. → unchanged
- Queries with "20XX" patterns → unchanged
- Australian context queries (legal/tax) → "(Australian context)" appended

### Installation & Setup

#### Quick Start
```bash
# Install dependencies and make executable
make install

# Setup Claude Code hook
make setup-claude

# Add shell functions to profile
make setup-shell
```

#### Manual Setup
```bash
# Install Python dependencies
uv pip install click pydantic

# Make scripts executable
chmod +x claude_year_hook.py ai_query_enhancer.py

# Configure Claude hook manually
claude config set hooks.preToolUse ./claude_year_hook.py
```

---

## Key Conventions & Patterns

### Code Style
- **Python version:** 3.8+ (ai_query_enhancer.py), 3.13+ (aiqe.py)
- **Type hints:** Used throughout with `typing` module
- **Docstrings:** Brief one-liners for functions
- **Error handling:** Graceful degradation (pass through on failure)
- **CLI framework:** Click for arguments and options

### Naming Conventions
- **Functions:** snake_case with descriptive names
- **Classes/Enums:** PascalCase
- **Constants:** Implicit (enum values are lowercase strings)
- **Variables:** snake_case

### Design Patterns
1. **Single Responsibility:** Each function has one clear purpose
2. **Enum-based dispatch:** Mode and tool selection via enums
3. **JSON I/O:** Structured input/output for tool integration
4. **Defensive programming:** Check for missing data, handle errors
5. **PEP 723:** Script metadata in comments for dependencies

### Integration Patterns
- **Hook mode:** JSON stdin → process → JSON stdout
- **CLI mode:** Arguments → process → JSON stdout (pretty-printed)
- **Shell wrapper:** Function → Python script → formatted output

---

## Common Tasks for AI Assistants

### 1. Adding a New Enhancement Mode

Example: Adding "security-focus" mode

```python
# In ai_query_enhancer.py

# Step 1: Add enum (line ~33)
class EnhancementMode(str, Enum):
    # ... existing modes ...
    SECURITY_FOCUS = "security-focus"

# Step 2: Create enhancement function (line ~90)
def enhance_with_security_focus(query: str) -> str:
    """Add security and best practices context."""
    security_keywords = ['secure', 'vulnerability', 'encryption', 'auth']
    if not any(kw in query.lower() for kw in security_keywords):
        return f"{query} (focus on security best practices)"
    return query

# Step 3: Add to enhance_query() (line ~84)
def enhance_query(query: str, mode: EnhancementMode, context: Optional[str] = None) -> str:
    # ... existing conditions ...
    elif mode == EnhancementMode.SECURITY_FOCUS:
        return enhance_with_security_focus(query)
    return query
```

### 2. Debugging Hook Issues

Check these areas:
- **JSON format:** Validate input/output structure
- **Tool input extraction:** Verify `tool_input.query` path
- **Error handling:** Check stderr for Python errors
- **Permissions:** Ensure script is executable (`chmod +x`)

Debug command:
```bash
echo '{"tool_input":{"query":"test"}}' | python3 -u ./claude_year_hook.py 2>&1
```

### 3. Extending for New Tools

Template for adding tool support:

```python
# Add enum value
class ToolType(str, Enum):
    NEW_TOOL = "newtool"

# Add format handler
def format_for_tool(enhanced_query: str, tool: ToolType, original_data: Dict[str, Any]) -> Dict[str, Any]:
    # ... existing conditions ...
    elif tool == ToolType.NEW_TOOL:
        return {
            'prompt': enhanced_query,
            'metadata': original_data.get('metadata', {})
        }
```

---

## Technical Details

### Dependencies
- **click** - CLI framework
- **pydantic** - Data validation (imported but not heavily used)
- **Python stdlib:** json, sys, re, datetime, typing, enum

### Package Management
- **Preferred tool:** `uv` (fast Rust-based Python package manager)
- **Install with:** `uv pip install click pydantic`
- **Alternative:** Standard `pip` works but `uv` is faster

### Temporal Detection Logic
**Year reference:** Regex `r'20\d{2}'` matches 2000-2099
**Temporal keywords:**
```python
['latest', 'recent', 'current', 'new', 'now', 'today',
 'this year', 'currently', 'nowadays', 'up to date',
 'modern', 'contemporary', 'updated', 'cutting edge']
```

### Claude Hook Spec Compliance
**Input format:**
```json
{
  "tool_input": {
    "query": "search query here",
    "other": "fields..."
  }
}
```

**Output format:**
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "modifiedToolInput": {
      "query": "enhanced query",
      "other": "preserved fields..."
    }
  }
}
```

---

## Known Limitations & Edge Cases

1. **aiqe.py is minimal:** Just a placeholder "Hello World" script
2. **No test suite:** Only manual testing via `make test`
3. **No CI/CD:** No automated testing or deployment
4. **Single file focus:** Each script is self-contained (good for portability)
5. **Makefile assumes Unix:** Won't work natively on Windows
6. **No configuration file:** All settings via CLI arguments
7. **Simple regex matching:** Year detection doesn't validate actual years

---

## Git Workflow

### Branch Strategy
- Working on: `claude/claude-md-mi40abb6a6cz4ltj-01XBHsWYhQ9WQebz2ZN6hATd`
- Branch must start with `claude/` and end with session ID
- Push with: `git push -u origin <branch-name>`

### Commit Message Style
Based on recent commits:
- `chore:` for non-code changes (README, docs)
- `initial commit` for repository setup
- Keep messages concise and descriptive

---

## Questions to Ask Users

When working on this project, clarify:

1. **Enhancement mode selection:** Which mode is appropriate for their use case?
2. **Tool target:** Which AI tool are they integrating with?
3. **Context requirements:** Do they need custom context injection?
4. **Hook vs CLI:** Are they using Claude hook or standalone CLI?
5. **Shell preference:** Bash or Zsh for shell function integration?

---

## Quick Reference Commands

```bash
# Install and setup
make install                # Install deps + make executable
make setup-claude          # Configure Claude hook
make test                  # Run test suite

# Direct usage
python3 ai_query_enhancer.py --tool claude --mode year-append "query"
python3 ai_query_enhancer.py --tool codex --mode tech-focus "query"
python3 ai_query_enhancer.py --stdin-json < input.json

# Hook testing
echo '{"tool_input":{"query":"test"}}' | ./claude_year_hook.py

# Shell functions (after setup)
ai_ask claude year-append "query"
claude_ask "query"
au_ask "query about Australian regulations"
```

---

## Related Resources

- **Integration docs:** See integration_examples.md for detailed examples
- **Claude hooks:** Claude Code documentation for hook specifications
- **PEP 723:** [Inline script metadata](https://peps.python.org/pep-0723/)

---

*Last updated: 2025-11-18*
*Repository: aiqe (AI Query Enhancer)*
