# Phase 1 Demo Test Files

This folder contains demo-ready artifacts for the Code/PR stage.

## What is included

- `diffs/pr_with_secrets_and_patterns.diff`:
  PR-style unified diff with secret leak + risky patterns.
- `payloads/github_pull_request_opened.json`:
  GitHub webhook sample payload (`pull_request.opened`).
- `payloads/gitlab_merge_request_opened.json`:
  GitLab webhook sample payload (`Merge Request Hook`, open).
- `config/repo_mapping.example.json`:
  Placeholder mapping from `owner/repo` to local checked-out path.
- `config/.env.phase1.example`:
  Placeholder credentials/tokens for demo setup.
- `config/known_secret_hashes.example.txt`:
  Placeholder known hashes for Secrets Vault MCP adapter.
- `config/policy_rules.example.json`:
  Placeholder policy rules for Policy Rules MCP adapter.
- `target_repo_stub/app.py`:
  Tiny vulnerable code sample.

## Recommended demo flow

1. Copy and edit placeholders in `config/`.
2. Run direct diff scan:
   ```bash
   .venv/bin/python source_code/main_security_scan_entrypoint.py change-guard \
     --diff-file test_files/phase1_demo/diffs/pr_with_secrets_and_patterns.diff \
     --no-semgrep \
     --output-dir /tmp/change-guard-demo-output \
     --known-secret-hashes-file test_files/phase1_demo/config/known_secret_hashes.example.txt \
     --policy-rules-file test_files/phase1_demo/config/policy_rules.example.json
   ```
3. Run webhook payload simulation:
   ```bash
   .venv/bin/python source_code/main_security_scan_entrypoint.py change-guard-event \
     --provider github \
     --payload-file test_files/phase1_demo/payloads/github_pull_request_opened.json \
     --diff-file test_files/phase1_demo/diffs/pr_with_secrets_and_patterns.diff \
     --repo-map-file test_files/phase1_demo/config/repo_mapping.example.json \
     --no-semgrep
   ```
