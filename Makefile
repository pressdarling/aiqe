# Makefile for AI Query Enhancer Setup

.PHONY: install setup-claude setup-shell test clean

# Install dependencies and make scripts executable
install:
	pip install click pydantic
	chmod +x claude_year_hook.py
	chmod +x ai_query_enhancer.py

# Setup Claude Code hook integration
setup-claude: install
	@echo "Setting up Claude Code hook..."
	@if command -v claude >/dev/null 2>&1; then \
		claude config set hooks.preToolUse ./claude_year_hook.py; \
		echo "✅ Claude hook configured"; \
	else \
		echo "❌ Claude Code not found. Install Claude Code first."; \
	fi

# Add shell functions to profile
setup-shell:
	@echo "Adding ai_ask function to shell profile..."
	@if [ -f ~/.zshrc ]; then \
		echo "\n# AI Query Enhancer Function" >> ~/.zshrc; \
		echo "source $$(pwd)/shell_functions.sh" >> ~/.zshrc; \
		echo "✅ Added to ~/.zshrc"; \
	elif [ -f ~/.bashrc ]; then \
		echo "\n# AI Query Enhancer Function" >> ~/.bashrc; \
		echo "source $$(pwd)/shell_functions.sh" >> ~/.bashrc; \
		echo "✅ Added to ~/.bashrc"; \
	else \
		echo "❌ No shell profile found"; \
	fi

# Test the enhancer with different modes
test:
	@echo "Testing year-append mode..."
	python3 ai_query_enhancer.py --tool claude --mode year-append "python tutorials"
	@echo "\nTesting tech-focus mode..."
	python3 ai_query_enhancer.py --tool codex --mode tech-focus "error handling"
	@echo "\nTesting context-inject mode..."
	python3 ai_query_enhancer.py --tool gemini --mode context-inject --context "TypeScript project" "best practices"

# Clean up generated files
clean:
	rm -f claude_year_hook.py ai_query_enhancer.py integration_examples.md shell_functions.sh
