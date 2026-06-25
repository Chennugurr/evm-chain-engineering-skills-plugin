from __future__ import annotations

import re
from pathlib import Path

from .reports import Finding

SAFE_PLACEHOLDERS = {
    "<INJECT_FROM_SECURE_SIGNER_AT_RUNTIME>",
    "<USE_KMS_OR_HARDWARE_WALLET>",
    "<SET_IN_CI_SECRET_STORE_NOT_IN_REPO>",
    "<REDACTED_DO_NOT_COMMIT>",
    "<DO_NOT_COMMIT_REAL_SECRET>",
    "<PIN_DIGEST_BEFORE_USE>",
    "<ASSIGN_UNIQUE_CHAIN_ID_AFTER_COLLISION_CHECK>",
}
SECRET_NAME_RE = re.compile(r"(?i)\b(PRIVATE_KEY|DEPLOYER_PRIVATE_KEY|ADMIN_PRIVATE_KEY|BATCHER_PRIVATE_KEY|PROPOSER_PRIVATE_KEY|SEQUENCER_PRIVATE_KEY|VALIDATOR_PRIVATE_KEY|MNEMONIC|SEED_PHRASE|WALLET_SEED|KEYSTORE_PASSWORD|API_SECRET)\b\s*[:=]")
SECRET_VALUE_RE = re.compile(r"0x[a-fA-F0-9]{64}|-----BEGIN (?:EC |RSA |OPENSSH )?PRIVATE KEY-----")
MNEMONIC_RE = re.compile(r"(?i)(mnemonic|seed phrase)\s*[:=]\s*['\"]?[a-z]+(?:\s+[a-z]+){11,}")
PRIVATE_FLAG_RE = re.compile(r"(?i)--(private-key|mnemonic|seed|deployer-secret)(?:=|\s+)\S+")
MAINNET_RE = re.compile(r"(--broadcast|cast send|cast publish|forge script|hardhat run|npx hardhat run|truffle migrate|brownie run|sendTransaction|eth_sendRawTransaction).{0,160}(mainnet|ethereum-mainnet|eth-mainnet|arb1|arbitrum-one|optimism-mainnet|base-mainnet|polygon-mainnet|bsc-mainnet|avalanche-mainnet|zksync-mainnet)|(mainnet|ethereum-mainnet|eth-mainnet|arb1|arbitrum-one|optimism-mainnet|base-mainnet|polygon-mainnet|bsc-mainnet|avalanche-mainnet|zksync-mainnet).{0,160}(--broadcast|cast send|forge script|hardhat run|npx hardhat run|eth_sendRawTransaction)", re.I)
ADMIN_RPC_RE = re.compile(r"(?i)(--http\.addr\s+0\.0\.0\.0|--authrpc\.addr\s+0\.0\.0\.0|--ws\.addr\s+0\.0\.0\.0).{0,120}\b(admin|debug|personal|engine)\b|\b(admin|debug|personal|engine)\b.{0,120}(0\.0\.0\.0|public)")
LATEST_IMAGE_RE = re.compile(r"(?i)image\s*:\s*[^\s#]+:latest\b")
UNPINNED_IMAGE_RE = re.compile(r"(?i)image\s*:\s*([\w./-]+)$")


def _safe_line(line: str) -> bool:
    lowered = line.lower()
    return any(marker in line for marker in SAFE_PLACEHOLDERS) or "placeholder only" in lowered or "redacted placeholder" in lowered or "do not commit real secret" in lowered


def scan_text(text: str, path: str) -> list[Finding]:
    findings: list[Finding] = []
    for line_no, line in enumerate(text.splitlines(), 1):
        source = f"{path}:{line_no}"
        if SECRET_VALUE_RE.search(line):
            findings.append(Finding("error", source, "private-key-shaped value detected"))
        if SECRET_NAME_RE.search(line) and not _safe_line(line):
            findings.append(Finding("error", source, "secret-like field assignment is not an approved placeholder"))
        if MNEMONIC_RE.search(line) and not _safe_line(line):
            findings.append(Finding("error", source, "mnemonic or seed phrase assignment detected"))
        if PRIVATE_FLAG_RE.search(line):
            findings.append(Finding("error", source, "private material passed through a CLI flag"))
        if MAINNET_RE.search(line):
            findings.append(Finding("error", source, "mainnet broadcast/send/deploy pattern detected"))
        if ADMIN_RPC_RE.search(line) and not _safe_line(line) and not re.search(r"(?i)(admin_rpc_public:\s*false|must not|do not|no public|not exposed|not proxied|remain private|binds to localhost|private networks)", line):
            findings.append(Finding("warning", source, "public admin/debug RPC exposure pattern detected"))
        if LATEST_IMAGE_RE.search(line):
            findings.append(Finding("error", source, "latest image tag detected"))
    return findings


def scan_path(path: Path, root: Path) -> list[Finding]:
    findings: list[Finding] = []
    files = [path] if path.is_file() else [item for item in path.rglob("*") if item.is_file()]
    for file_path in files:
        if any(part in {".git", "__pycache__", ".pytest_cache"} for part in file_path.parts):
            continue
        try:
            text = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        try:
            rel = str(file_path.relative_to(root))
        except ValueError:
            rel = str(file_path)
        findings.extend(scan_text(text, rel))
    return findings


def has_unsafe_command(text: str) -> bool:
    return bool(MAINNET_RE.search(text) or PRIVATE_FLAG_RE.search(text) or SECRET_VALUE_RE.search(text))


def approved_placeholder(value: object) -> bool:
    return isinstance(value, str) and value in SAFE_PLACEHOLDERS
