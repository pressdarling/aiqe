# Integration Examples for AI Query Enhancer

## Claude Code Hook Integration

### Setup
1. Make the script executable:
   ```bash
   chmod +x claude_year_hook.py
   ```

2. Configure Claude Code to use the hook:
   ```bash
   # Add to your Claude Code configuration
   claude config set hooks.preToolUse ./claude_year_hook.py
   ```

### Usage
The hook automatically activates when using search tools in Claude Code:
```bash
claude search "python async patterns"
# Automatically becomes: "python async patterns 2025"
```

## OpenAI Codex CLI Integration

### Wrapper Script
```bash
#!/bin/bash
# codex_enhanced.sh
query="$*"
enhanced=$(python3 ai_query_enhancer.py --tool codex --mode year-append "$query")
echo "$enhanced" | openai api completions.create --model code-davinci-002 --stdin
```

### Usage
```bash
./codex_enhanced.sh "how to handle async errors in JavaScript"
```

## Gemini CLI Integration

### Via Alias
```bash
# Add to ~/.zshrc or ~/.bashrc
alias gemini-enhanced='f() { 
    python3 ai_query_enhancer.py --tool gemini --mode tech-focus "$1" | gemini-cli --stdin
}; f'
```

### Usage
```bash
gemini-enhanced "best way to structure TypeScript project"
```

## Cursor IDE Integration

### Via Extension or Script
```typescript
// cursor-extension.ts
import { exec } from 'child_process';

export function enhanceQuery(query: string, context?: string): Promise<string> {
    return new Promise((resolve, reject) => {
        const cmd = `python3 ai_query_enhancer.py --tool cursor --mode context-inject --context "${context}" "${query}"`;
        exec(cmd, (error, stdout) => {
            if (error) reject(error);
            else resolve(JSON.parse(stdout).query);
        });
    });
}
```

## GitHub Copilot Integration

### Via Git Hook
```bash
#!/bin/bash
# .git/hooks/pre-commit-copilot-enhance
# Enhance commit messages with context

commit_msg=$(cat .git/COMMIT_EDITMSG)
enhanced=$(python3 ai_query_enhancer.py --tool copilot --mode technical-focus "$commit_msg")
echo "$enhanced" > .git/COMMIT_EDITMSG
```

## Universal Shell Function

### Add to your shell profile
```bash
# ~/.zshrc
ai_ask() {
    local tool=${1:-claude}
    local mode=${2:-year-append}
    local query="${@:3}"

    case $tool in
        claude)
            echo "$query" | python3 ai_query_enhancer.py --tool claude --mode $mode --stdin-json
            ;;
        codex)
            python3 ai_query_enhancer.py --tool codex --mode $mode "$query"
            ;;
        gemini)
            python3 ai_query_enhancer.py --tool gemini --mode $mode "$query" | gemini-cli --stdin
            ;;
        *)
            echo "Supported tools: claude, codex, gemini"
            ;;
    esac
}
```

### Usage Examples
```bash
ai_ask claude year-append "latest React patterns"
ai_ask codex tech-focus "error handling in Node.js"
ai_ask gemini au-context "tax implications of cryptocurrency"
```
