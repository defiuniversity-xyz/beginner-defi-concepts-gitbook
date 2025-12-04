{% embed url="https://storage.googleapis.com/beginner-defi-concepts-media/lesson-05/audio/lesson5%20Wallets_and_Self-Custody.m4a" %}

{% embed url="https://storage.googleapis.com/beginner-defi-concepts-media/lesson-05/video/lesson5%20Your_Keys_Your_Crypto.mp4" %}

# Lesson 5: Wallets and Self-Custody

## 🎯 Core Concept: Self-Custody and Private Keys

The shift to self-custody is the highest barrier to entry for mainstream adopters. Unlike traditional finance where you can reset passwords or call customer support, in crypto, **you are your own bank**. If you lose your private keys, your funds are gone forever. Understanding wallets and self-custody is fundamental to safely participating in DeFi.

## 📚 Public vs. Private Key Cryptography

### Public Key: Your "Mailbox" Address

The public key (or wallet address, like `0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb`) is like your mailbox address. It's safe to share publicly—this is where people send you crypto.

**Key Point**: You can share your public address freely. It's how you receive funds.

### Private Key: Your "Key" to the Mailbox

The private key is like the key to your mailbox. It signs transactions to prove ownership without revealing the key itself. **Never share your private key with anyone.**

**Key Point**: Whoever has your private key controls your funds. If someone gets it, they can steal everything.

### Seed Phrases: The Human-Readable Backup

Seed phrases (usually 12-24 words) are the human-readable backup of your private key. **This phrase IS your wallet**. The hardware or software is merely a window to view the blockchain.

**Critical Understanding**:
- If your device is destroyed but your phrase is saved → funds are safe
- If your phrase is lost → funds are unrecoverable
- If someone sees your phrase → they can steal your funds

## 📚 Wallet Typology and Risk Hierarchies

### Hot Wallets (Browser Extensions/Mobile Apps)

These are connected to the internet (e.g., MetaMask, Phantom). They are convenient for daily DeFi interaction but vulnerable to malware, screen scrapers, and clipboard hijacking.

**Best Practice**: Treat hot wallets like a physical wallet—carry only "walking around money." Never store significant amounts in hot wallets.

### Cold Wallets (Hardware Wallets)

These devices (e.g., Ledger, Trezor) keep private keys air-gapped from the internet. Transaction signing happens inside the device. These are **mandatory for significant asset storage**.

**Best Practice**: Use hardware wallets for any amount you can't afford to lose.

### Smart Contract Wallets (Account Abstraction)

Emerging technology that improves UX by allowing features like social recovery, daily spending limits, and bundled transactions. This represents the future of user interaction, abstracting away raw private key management.

## 🔑 Key Takeaways

1. **Your Keys, Your Crypto**: If you don't control the keys, you don't own the crypto.
2. **Seed Phrase = Wallet**: The phrase is more important than the device.
3. **Hot for Daily, Cold for Savings**: Use hot wallets for small amounts, hardware wallets for significant holdings.
4. **Never Share Private Keys**: Legitimate services never ask for your private key or seed phrase.
5. **Backup Your Seed Phrase**: Store it securely, offline, in multiple safe locations.

## 📖 Beginner's Corner

**What's the difference between a wallet and an exchange?**
- Wallet: You control the keys (self-custody)
- Exchange: They control the keys (custodial)

**How do I set up my first wallet?**
1. Download MetaMask (hot wallet) for daily use
2. Buy a Ledger or Trezor (cold wallet) for savings
3. Write down your seed phrase on paper (never digital)
4. Store it in a safe place

**What if I lose my seed phrase?**
- Unfortunately, your funds are lost forever. This is why backups are critical.

## ⚠️ Important Warnings

- **Phishing Scams**: Scammers will try to trick you into giving your seed phrase. Never enter it on any website.
- **Screenshot Risk**: Never screenshot your seed phrase—malware can steal it.
- **Social Engineering**: Legitimate services never ask for your private key or seed phrase.

---

**Next Lesson**: In Lesson 6, we'll explore security fundamentals, including token approvals and operational security best practices.
