# Foreign Currency Deposit Tool Research Handoff

Last updated: 2026-06-25

This document summarizes the product and market research for a small tool website about fixed deposit returns across currencies. It is intended as a handoff file so the discussion can continue from another computer or Codex session.

## 1. Product Direction

Initial product:

```text
Foreign Currency Fixed Deposit Calculator
外币定存收益与汇率风险计算器
```

The first version should be a single web page with one high-quality tool, not a large multi-page site.

Core user flow:

1. User enters an amount in one currency.
2. User selects or enters the original currency deposit rate.
3. User selects a target currency.
4. User enters or later selects the target currency fixed deposit rate.
5. User enters the current exchange rate and expected maturity exchange rate.
6. The page calculates the original-currency deposit return, target-currency deposit return, exchange-rate gain/loss, break-even exchange rate, and downside scenarios.

The tool should work for any major currency pair, not only RMB/USD.

Initial currencies:

```text
USD, CAD, HKD, SGD, CNY, EUR, GBP, AUD, JPY
```

Recommended positioning:

```text
Multi-Currency Deposit Return Calculator
Currency Deposit Return and FX Risk Calculator
外币定存收益计算器
多币种定存收益与汇率风险计算器
```

Avoid positioning it as:

```text
最佳投资路线
稳赚方案
最高收益推荐
```

Use safer wording:

```text
收益测算
风险比较
保本汇率
汇率情景分析
仅供参考，不构成投资建议
```

## 2. Target Users

The likely audience is ordinary retail users who hold or consider holding cash in more than one currency.

Useful user segments:

- Overseas Chinese users
- East Asian users with USD, HKD, SGD, CNY, CAD, AUD, or JPY exposure
- Families planning tuition, migration, or overseas living costs
- Conservative savers who prefer deposits over stocks
- Users who are attracted by high foreign-currency deposit rates but do not understand exchange-rate risk
- Female personal-finance users on social platforms such as Xiaohongshu, but the product should not be framed as exclusively for women

Preferred tone:

```text
clear, practical, risk-first, non-trading, non-hype
```

Avoid a trader-style interface with charts, leverage language, or aggressive return claims.

## 3. Core Calculation Outputs

Required outputs:

```text
Original-currency maturity value
Target-currency maturity value
Target-currency value converted back to original currency
Extra gain or loss vs staying in original currency
Break-even maturity exchange rate
Maximum exchange-rate drop before the target-currency route loses its advantage
Scenario table for exchange-rate movement: -10%, -5%, -3%, -1%, 0%, +1%, +3%, +5%, +10%
Estimated cost from bid/ask spread if available
```

Basic formula:

```text
Original maturity amount = original principal * original deposit factor

Target principal = original principal / buy FX rate
Target maturity amount = target principal * target deposit factor
Converted-back amount = target maturity amount * maturity sell FX rate

Break-even maturity FX rate =
  original principal * original deposit factor / target maturity amount

Equivalent simplified form =
  initial buy FX rate * original deposit factor / target deposit factor
```

Important note:

For real bank transactions, users should use the bank's sell rate when buying the foreign currency and the bank's buy rate when converting back. Mid-market rates are only reference rates.

## 4. Competitor Research

### Closest Tool Pages

Moneyland Break-Even Exchange Rate Calculator:

```text
https://www.moneyland.ch/en/break-even-exchange-rate-calculator
```

Strength:

```text
Calculates the break-even exchange rate between two currency investment routes.
```

Gap:

```text
Not a bank-rate aggregation tool and not framed as a fixed deposit decision tool.
```

Moneyland Foreign Investment Comparison Calculator:

```text
https://www.moneyland.ch/en/foreign-investment-comparison-calculator
```

Strength:

```text
Compares investment returns across currencies with exchange-rate assumptions.
```

Gap:

```text
Generic investment model, not focused on retail fixed deposits or bank rates.
```

Maybank Foreign Currency Time Deposit e-Calculator:

```text
https://sslsecure.maybank.com.sg/scripts/mbb_fctd_input.jsp
```

Strength:

```text
Calculates foreign-currency time deposit interest and breakeven rate.
```

Gap:

```text
Bank-specific and Singapore-focused.
```

E.SUN FX Deposit Calculator:

```text
https://www.esunbank.com/en/personal/deposit/rate/foreign/deposit-trial-calculation
```

Strength:

```text
Foreign-currency deposit trial calculation with many currencies.
```

Gap:

```text
Does not compare two currency routes across banks.
```

Small independent Taiwan-focused calculator:

```text
https://freelifeofoctopus.com/forex-deposit-tool/
```

Strength:

```text
Very close to the desired concept: interest contribution, exchange-rate impact, and break-even rate.
```

Gap:

```text
Focused on Taiwan/TWD and does not connect to broad bank-rate data.
```

### Content and Rate Comparison Sites

Hong Kong:

```text
StashAway HK USD time deposit pages
MoneySmart HK
MoneyHero HK
HKET
```

Singapore:

```text
StashAway SG
Beansprout
Syfe
MoneySmart SG
```

Canada:

```text
Ratehub USD GIC rates
Forbes Canada
WOWA
```

United States:

```text
NerdWallet CD Calculator
Bankrate CD Calculator
Forbes Advisor
Calculator.net
```

Observation:

Existing sites usually cover one side of the problem:

- Banks have real rates but only for their own products.
- Content sites list rates but often do not calculate exchange-rate downside.
- Generic calculators compute returns but do not link to bank-rate sources.

Market gap:

```text
Bank-rate facts + two-currency deposit comparison + FX risk + break-even exchange rate
```

## 5. Geographic Scope

Planned site audience:

```text
Asia + North America
```

Best first markets:

```text
Hong Kong
Singapore
Canada
United States
```

Reasons:

- Hong Kong and Singapore have active foreign-currency deposit markets.
- Canada has CAD vs USD GIC demand.
- The United States has strong CD calculator traffic, but mainly USD-only and very competitive.

Secondary markets:

```text
Mainland China
Taiwan
Malaysia
Japan
South Korea
```

Mainland China should be handled carefully because of financial-content compliance, domestic ad-platform requirements, and potential ICP filing needs if using mainland hosting.

## 6. Keyword Research Direction

### English Keywords

Primary:

```text
foreign currency fixed deposit calculator
foreign currency deposit calculator
currency deposit return calculator
multi currency deposit calculator
break-even exchange rate calculator
currency deposit exchange rate risk
```

Long-tail:

```text
USD vs SGD fixed deposit calculator
USD vs HKD time deposit calculator
CAD vs USD GIC calculator
USD fixed deposit exchange rate risk
is foreign currency fixed deposit worth it
how much exchange rate drop will erase deposit interest
```

High-competition terms to avoid as the first target:

```text
CD calculator
best CD rates
fixed deposit calculator
best fixed deposit rates
```

### Chinese Keywords

Primary:

```text
外币定存收益计算器
外币定存汇率风险
外币定存保本汇率
美元定存收益计算器
美元定存汇率风险
```

Long-tail:

```text
美元定存划算吗
美元定存会亏吗
美元定存汇率跌多少会亏
外币定存利率高为什么会亏
外币定存保本汇率怎么算
美元定期存款利率比较
香港美元定存利率
新加坡美元定存利率
加拿大美元GIC利率
美国CD利率计算器
```

Traditional Chinese / Hong Kong / Taiwan variants:

```text
外幣定存報酬試算器
外幣定存收益試算
美元定期存款利率比較
美元定存邊間銀行最高息
外幣定存匯率風險
保本匯率
```

Keyword strategy:

Start with calculator and risk terms, not broad rate-list terms.

Good first-page targets:

```text
外币定存收益计算器
foreign currency fixed deposit calculator
外币定存保本汇率
break-even exchange rate fixed deposit
美元定存汇率跌多少会亏
```

## 7. Domestic Chinese Search Platforms

Main platforms:

```text
Baidu
360 Search
Sogou / WeChat Search
Shenma / Quark
```

Key findings:

- Baidu can index overseas-hosted sites, but mainland access speed and stability matter.
- Overseas hosting does not require ICP filing, but mainland hosting generally does.
- Baidu SEO should be treated separately from Google SEO.
- For domestic ad platforms, ICP filing and content compliance may become important.

Baidu strategy:

```text
Submit sitemap and URLs through Baidu Search Resource Platform.
Use simplified Chinese pages.
Avoid thin pages and duplicated programmatic pages.
Make the tool usable on mobile.
Use original explanation text, formulas, and examples.
```

360 / Sogou / Shenma:

```text
Useful secondary channels.
Focus on mobile page speed and simple pages.
```

WeChat Search:

```text
Better for content and mini-program discovery than for pure web ad monetization.
```

## 8. Advertising and Monetization

### Web Ads

Potential ad options:

```text
Google AdSense
Baidu Union
360 Union
Other domestic ad networks
Direct affiliate or CPA later
```

AdSense:

- Better for overseas users, Hong Kong, Taiwan, Singapore, Canada, and the United States.
- May be unstable for mainland China users because Google ad scripts can fail to load.
- Do not rely on AdSense as the main monetization method if the traffic is mostly mainland China.

Domestic ads:

- More suitable if mainland traffic grows.
- Usually more likely to require ICP filing, site review, and stricter content compliance.

Ad placement for the first page:

```text
Top or below-header ad slot
Result-section ad slot
In-article ad slot inside the explanation section
Fallback content if ads fail to load
```

Do not:

```text
encourage ad clicks
place ads too close to calculator buttons
buy low-quality traffic to force ad impressions
disguise ads as calculator results
```

### Social Traffic

Use social platforms for cold start and topic testing, not for ad arbitrage.

Recommended channels:

```text
Xiaohongshu
TikTok
YouTube Shorts
Zhihu
WeChat official account
Reddit
Quora
```

Content topics:

```text
美元定存 5% 真的赚钱吗？
外币定存汇率跌多少会亏？
高息外币定存为什么可能亏？
USD vs SGD 定存怎么比较？
CAD vs USD GIC 哪个更稳？
外币定存的保本汇率怎么算？
```

## 9. Legal and Compliance Notes

This is not legal advice. Use this as product-risk guidance only.

Safer content model:

```text
Calculator
Public bank-rate source links
Structured facts manually or automatically collected from public bank pages
Original explanations
Short news summaries with source links
Risk disclaimers
```

Avoid:

```text
copying full financial news articles
copying large parts of bank pages
copying media images
presenting the site as official bank content
claiming guaranteed returns
personalized investment advice
```

For bank rates:

- Linking to public bank pages is generally lower risk.
- Extracting factual fields is safer than copying full tables or page copy.
- Record the source URL and last update time.
- Respect login walls, robots restrictions, and terms where relevant.

For news:

- Use headline/source/date/link plus original short summary.
- Explain why the news may affect deposit rates, exchange rates, or user risk.
- Do not republish full articles.

Suggested disclaimer:

```text
This tool is for educational and calculation purposes only. It does not provide investment, tax, legal, or financial advice. Bank rates, exchange rates, eligibility rules, taxes, fees, and early-withdrawal terms may change. Always verify information with the bank or a qualified professional before making financial decisions.
```

Chinese version:

```text
本工具仅用于学习和测算，不构成投资、税务、法律或财务建议。银行利率、汇率、资格条件、税费和提前支取规则可能随时变化。做出决定前，请以银行官网、柜台、App 或专业人士意见为准。
```

## 10. Hosting and Technical Route

Recommended first route:

```text
Buy own .com domain
Use Cloudflare DNS
Deploy static site to Cloudflare Pages or Netlify
Use plain HTML/CSS/JavaScript or a light static framework
No VPS for the first version
```

Why:

- Low cost
- Low maintenance
- Fast pages
- Easy to move later
- Works well for a single calculator
- Can add AdSense later

Avoid at first:

```text
VPS server maintenance
heavy CMS
platform-locked website builders
free subdomains
```

If mainland China becomes the main traffic source:

```text
Consider ICP filing
Consider mainland CDN or hosting
Consider domestic ad networks
Consider WeChat or Baidu mini-program
```

## 11. Future Mini-Program Route

If web traffic validates demand, build:

```text
WeChat mini-program
Baidu smart mini-program
Alipay mini-program
```

Priority:

1. WeChat mini-program for social sharing and domestic user retention.
2. Baidu smart mini-program if Baidu search traffic grows.
3. Alipay mini-program if the financial-tool angle becomes strong enough.

Design the first web version so logic can be reused:

```text
separate calculation functions
separate currency metadata
separate rate-source data
URL-shareable input parameters
clean JSON-like calculation results
```

Example future URL parameters:

```text
?base=USD&target=SGD&amount=10000&baseRate=4.2&targetRate=3.6&term=12
```

## 12. First MVP Page Structure

Recommended single-page structure:

1. Hero / tool title

```text
Foreign Currency Fixed Deposit Calculator
外币定存收益与汇率风险计算器
```

2. Calculator inputs

```text
Principal amount
Original currency
Target currency
Original currency deposit rate
Target currency deposit rate
Term
Current exchange rate
Expected maturity exchange rate
Optional bid/ask spread
```

3. Results

```text
Original-currency route
Target-currency route
Difference
Break-even FX rate
FX downside buffer
Scenario table
```

4. Explanation

```text
What is foreign-currency deposit risk?
What is break-even exchange rate?
Why bank buy/sell rates matter
How the calculator works
```

5. Bank-rate source links

```text
Hong Kong bank rate pages
Singapore bank rate pages
Canada GIC pages
US CD pages
```

6. FAQ

```text
Can foreign-currency deposits lose money?
Why can a high interest rate still lose after exchange-rate movement?
Is this investment advice?
Which exchange rate should I use?
```

7. Disclaimer

## 13. Suggested First 10 Pages After MVP

Only expand after the first page is indexed and usage data is available.

```text
1. Foreign Currency Fixed Deposit Calculator
2. 外币定存收益计算器
3. Break-Even Exchange Rate Calculator
4. 外币定存保本汇率怎么算
5. USD vs SGD Fixed Deposit Calculator
6. USD vs HKD Time Deposit Calculator
7. CAD vs USD GIC Calculator
8. 美元定存汇率跌多少会亏
9. 美元定存划算吗
10. 外币定存有风险吗
```

Do not create hundreds of near-duplicate currency-pair pages before collecting Search Console or Baidu data.

## 14. Open Questions

These should be decided before development:

1. Site language order:

```text
English first, Chinese first, or bilingual from day one?
```

2. Domain name:

```text
generic tool brand vs finance-specific brand
```

3. First market focus:

```text
Hong Kong/Singapore overseas Chinese vs North America users
```

4. Data strategy:

```text
manual input only first vs curated bank-rate source links vs weekly collected bank-rate table
```

5. Ad strategy:

```text
AdSense first vs no ads until search traffic starts vs domestic ads later
```

6. Compliance boundary:

```text
calculator only vs rate aggregation vs news summaries
```

## 15. Recommended Next Prompt for Another Codex Session

Use this prompt on the other computer:

```text
Read docs/foreign-currency-deposit-tool-research.md first. Continue planning the MVP for a single-page Foreign Currency Fixed Deposit Calculator. We are still in research/planning mode unless I explicitly ask you to build. Focus on keyword strategy, landing-page structure, data sources, SEO, ad placement, and compliance-safe wording.
```

If ready to build later:

```text
Read docs/foreign-currency-deposit-tool-research.md first. Build a static single-page Foreign Currency Fixed Deposit Calculator with reusable calculation logic, SEO-friendly content sections, disclaimer, and placeholder ad slots. Do not integrate live bank-rate scraping yet.
```
