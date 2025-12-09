# Lesson 6: Security Fundamentals

## 🎯 Core Concept: Active Security Hygiene

A critical, often overlooked topic in basic curricula is the mechanism of Token Approvals. Understanding how approvals work and how to manage them is essential for staying safe in DeFi.

## 📚 The Token Approval Model

### The Mechanism

To trade a token on a DEX like Uniswap, you must first sign a transaction "Approving" the smart contract to spend your tokens. This is like giving a store permission to charge your credit card.

**The Process**:
1. You want to swap USDC for ETH on Uniswap
2. First transaction: Approve Uniswap to spend your USDC
3. Second transaction: Execute the swap

### The Risk: Infinite Approval

For convenience, many dApps ask for "Infinite Approval," meaning the contract can withdraw that token from your wallet at any time in the future without further permission.

**The Danger**: If the dApp's contract is later upgraded maliciously or hacked, the attacker can drain the wallets of all users who previously granted approval, even if they haven't used the site in months.

### Mitigation: Regular Approval Audits

The curriculum must integrate the use of tools like Revoke.cash as a standard operating procedure. Users must learn to regularly audit and revoke allowances for dApps they are no longer actively using.

**Best Practice**: 
- Use limited approvals when possible (approve only what you need)
- Regularly review and revoke unused approvals
- Use Revoke.cash or similar tools monthly


![Token Approval Process Diagram](https://storage.googleapis.com/beginner-defi-concepts-gitbook-images/lessons/lesson_06/bdc06_01_token_approval_process_diagram.png)


## 📚 Operational Security Best Practices

### 1. Verify Contract Addresses

Always verify you're interacting with the correct contract. Scammers create fake versions of popular dApps.

**How to Verify**:
- Check official websites/social media
- Use block explorers to verify contract addresses
- Bookmark legitimate sites (don't click random links)

### 2. Start Small

When trying a new protocol, start with small amounts to test. Don't deposit large sums immediately.

### 3. Use Hardware Wallets

For any significant amount, use a hardware wallet. It keeps your private keys offline and secure.

### 4. Be Wary of Airdrops and Free Tokens

If something seems too good to be true, it probably is. Scammers use fake airdrops to trick users into approving malicious contracts.

### 5. Keep Software Updated

Keep your wallet software and browser extensions updated. Updates often include security patches.


![Security Best Practices Checklist](https://storage.googleapis.com/beginner-defi-concepts-gitbook-images/lessons/lesson_06/bdc06_02_security_best_practices_checklist.png)



![Common Attack Vectors Diagram](https://storage.googleapis.com/beginner-defi-concepts-gitbook-images/lessons/lesson_06/bdc06_03_common_attack_vectors_diagram.png)

## 🎮 Interactive: Security Checklist

Complete this interactive security checklist to review all essential DeFi security practices:

{% embed url="https://defi-university-app.web.app/interactives/defi-concepts/security-checklist.html?courseId=defi-concepts&interactionId=security-checklist" %}

## 🔑 Key Takeaways

1. **Approvals Are Permissions**: When you approve a contract, you're giving it permission to spend your tokens.
2. **Infinite Approvals Are Risky**: Revoke unused approvals regularly.
3. **Verify Everything**: Always verify you're on the legitimate site/contract.
4. **Start Small**: Test new protocols with small amounts first.
5. **Hardware Wallets**: Use them for significant holdings.

## 📖 Beginner's Corner

**What is Revoke.cash?**
- A tool that lets you see and revoke token approvals
- Use it monthly to clean up unused approvals
- It's free and safe to use

**How do I know if a dApp is safe?**
- Check if it's audited by reputable firms
- Look for how long it's been running
- Check community reviews
- Start with small amounts

**What should I do if I think I've been hacked?**
- Immediately move remaining funds to a new wallet
- Revoke all approvals
- Report the incident
- Learn from the experience

## ⚠️ Important Warnings

- **Approval Risk**: Unused approvals can be exploited if contracts are compromised.
- **Phishing**: Always verify URLs and contract addresses.
- **Social Engineering**: Never share your seed phrase or private key.
- **FOMO**: Don't rush into new protocols without research.

---

**Next Lesson**: In Lesson 7, we'll explore decentralized exchanges (DEXs) and how automated market makers work.
