"""Crypto tag for the exploratory logs (author's decision, 1 Nov 2026).

AI and cryptocurrency get their own section in each report, built from a tag on the existing
logs (the AI attack log, the GitHub and Hugging Face sweeps) rather than a separate measure;
it may become a measure of its own at the March 2027 review if it proves active.
"""
import re

CRYPTO = re.compile(r"crypto|bitcoin|\bbtc\b|ethereum|\beth\b|blockchain|web3|\bdefi\b|smart.?contract|solidity|"
                    r"stablecoin|wallet|drainer|\bnft\b|token (theft|drain)|exchange (hack|heist)|\bmev\b|rug.?pull|"
                    r"pig.?butcher|加密货币|区块链|криптовалют|блокчейн|暗号資産", re.I)


def is_crypto(*texts: str) -> bool:
    return bool(CRYPTO.search(" ".join(t or "" for t in texts)))
