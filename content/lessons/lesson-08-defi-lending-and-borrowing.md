# Lesson 8: DeFi Lending and Borrowing

## 🎯 Core Concept: Over-Collateralized Lending

DeFi protocols like Aave and Compound allow for permissionless lending and borrowing. Unlike TradFi, which relies on credit scores, DeFi relies on **Over-Collateralization**. To borrow $100 worth of USDC, you might need to deposit $150 worth of ETH as collateral.


![Over-Collateralization Diagram](https://storage.googleapis.com/beginner-defi-concepts-gitbook-images/lessons/lesson_08/bdc08_01_over-collateralization_diagram.png)


## 📚 How It Works

**The Mechanics**:
1. Deposit collateral (e.g., $150 ETH)
2. Borrow against it (e.g., $100 USDC)
3. If collateral value drops near debt value → automatic liquidation

**Use Cases for Borrowing**:
- **Leverage**: Borrow against an asset to buy more of that asset
- **Tax Efficiency**: Access liquidity without selling (avoiding capital gains)
- **Short Selling**: Borrow an asset to sell it, hoping to buy back cheaper


![Lending Protocol Flowchart](https://storage.googleapis.com/beginner-defi-concepts-gitbook-images/lessons/lesson_08/bdc08_03_lending_protocol_flowchart.png)


## 📚 Health Factors

The Health Factor determines loan safety:

$$H_f = \frac{Collateral \times Liquidation\ Threshold}{Debt}$$

- **H_f > 1**: Position is safe
- **H_f < 1**: Position is liquidated


![Health Factor Calculation Visualization](https://storage.googleapis.com/beginner-defi-concepts-gitbook-images/lessons/lesson_08/bdc08_02_health_factor_calculation_visualization.png)

## 🎮 Interactive: Lending Calculator

Calculate your loan health factor and liquidation price with this interactive tool:

{% embed url="https://defi-university-app.web.app/interactives/defi-concepts/lending-calculator.html?courseId=defi-concepts&interactionId=lending-calculator" %}

## 🔑 Key Takeaways

1. **Over-Collateralization**: You must deposit more than you borrow
2. **No Credit Checks**: Access is permissionless, based on collateral only
3. **Automatic Liquidations**: If collateral drops, position is liquidated
4. **Health Factor**: Monitor this metric to avoid liquidation
5. **Interest Rates**: Determined algorithmically by supply and demand

---

**Next Lesson**: In Lesson 9, we'll explore stablecoins and stability mechanisms.
