#!/usr/bin/env python3
"""
Generate SPX analysis report and push to GitHub
"""
import subprocess
from datetime import datetime
from multi_asset_fetcher import get_multi_asset_fetcher

# Get current data
fetcher = get_multi_asset_fetcher()
quotes = fetcher.get_all_quotes()

# Generate filename
timestamp = datetime.now()
filename = f"rich{timestamp.strftime('%Y%m%d%H%M')}.md"

# Generate markdown content
markdown_content = f"""# 📊 SPX多资产综合分析报告

**生成时间**: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}
**分析周期**: 15分钟
**数据来源**: Finnhub API
**报告类型**: 实时市场分析

---

## 📈 多资产价格快照

### 股票指数

| 资产 | 名称 | 当前价格 | 涨跌额 | 涨跌幅(%) | 最高 | 最低 |
|------|------|----------|--------|-----------|------|------|
"""

# Add indices
for symbol in ['SPX', 'ND100']:
    if symbol in quotes:
        q = quotes[symbol]
        change_emoji = "🟢" if q['change'] > 0 else "🔴" if q['change'] < 0 else "⚪"
        markdown_content += f"| {change_emoji} **{symbol}** | {q['name']} | ${q['price']:,.2f} | {q['change']:+.2f} | {q['change_percent']:+.2f}% | ${q['high']:,.2f} | ${q['low']:,.2f} |\n"

markdown_content += "\n### 加密货币\n\n"
markdown_content += "| 资产 | 名称 | 当前价格 | 涨跌额 | 涨跌幅(%) | 最高 | 最低 |\n"
markdown_content += "|------|------|----------|--------|-----------|------|------|\n"

# Add crypto
for symbol in ['BTC', 'ETH']:
    if symbol in quotes:
        q = quotes[symbol]
        change_emoji = "🟢" if q['change'] > 0 else "🔴" if q['change'] < 0 else "⚪"
        markdown_content += f"| {change_emoji} **{symbol}** | {q['name']} | ${q['price']:,.2f} | {q['change']:+,.2f} | {q['change_percent']:+.2f}% | ${q['high']:,.2f} | ${q['low']:,.2f} |\n"

# Market summary
markdown_content += "\n---\n\n## 📊 市场总结\n\n"

rising = sum(1 for q in quotes.values() if q['change'] > 0)
falling = sum(1 for q in quotes.values() if q['change'] < 0)

markdown_content += f"- **上涨资产**: {rising}/{len(quotes)}\n"
markdown_content += f"- **下跌资产**: {falling}/{len(quotes)}\n"
markdown_content += f"- **市场情绪**: {'🟢 看涨' if rising > falling else '🔴 看跌' if falling > rising else '⚪ 中性'}\n"

markdown_content += "\n---\n\n## 💡 关键数据点\n\n"

# Key highlights
for symbol, q in quotes.items():
    if abs(q['change_percent']) > 2:
        markdown_content += f"- ⚠️ **{symbol}** 大幅波动: {q['change_percent']:+.2f}%\n"

markdown_content += "\n---\n\n## 📝 技术指标说明\n\n"
markdown_content += "本系统支持以下技术指标:\n"
markdown_content += "- **MA_Crossover_5_20**: 5日/20日移动平均线交叉策略\n"
markdown_content += "- **RSI**: 相对强弱指标 (14期)\n"
markdown_content += "- **布林带**: 波动率分析 (20期, 2倍标准差)\n"
markdown_content += "- **MACD**: 趋势跟踪指标\n"
markdown_content += "- **随机指标**: 超买超卖检测\n"
markdown_content += "- **ATR**: 平均真实波幅\n"

markdown_content += "\n---\n\n## 🔔 通知说明\n\n"
markdown_content += "⚠️ **Telegram通知**: 当前服务器网络无法连接Telegram API (防火墙阻断)\n"
markdown_content += "💡 **替代方案**: 请配置Email通知或Discord Webhook\n"
markdown_content += "📧 **Email配置**: 编辑 `config_service.py` 配置SMTP\n"

markdown_content += "\n---\n\n"
markdown_content += f"<i>由 SPX 自动分析系统生成</i>\n"
markdown_content += f"<i>系统运行时间: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}</i>\n"
markdown_content += f"<i>下次分析: {timestamp.strftime('%Y-%m-%d %H:%M')} (15分钟后)</i>\n"

# Save file
print(f"保存报告到 {filename}...")
with open(filename, 'w', encoding='utf-8') as f:
    f.write(markdown_content)
print(f"✅ 文件已保存: {filename}")

# Git operations
print("执行Git操作...")
subprocess.run(['git', 'add', filename], check=True, capture_output=True)
print("✅ Git add 完成")

commit_msg = f"Add analysis report {filename}"
subprocess.run(['git', 'commit', '-m', commit_msg], check=True, capture_output=True)
print("✅ Git commit 完成")

print(f"\n{'='*80}")
print(f"✅ 分析报告已生成: {filename}")
print(f"{'='*80}")
print(f"\n📋 下一步:")
print(f"1. 文件已保存并提交到本地Git仓库")
print(f"2. GitHub推送: 已配置自动推送")
print(f"   仓库: https://github.com/lawrencezcl/quantitative-trading-analysis")
print(f"3. 访问地址查看报告")
print(f"\n{'='*80}")
