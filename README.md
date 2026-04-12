# CIS Operational Center - Command Center

<p align="center">
  <img src="https://img.shields.io/badge/Status-Live-brightgreen" alt="Status">
  <img src="https://img.shields.io/badge/Dashboard-Real--time-blue" alt="Dashboard">
  <img src="https://img.shields.io/badge/Data-JSON%20Storage-orange" alt="Data">
  <img src="https://img.shields.io/badge/Pages-GitHub%20Pages-purple" alt="Pages">
</p>

## 🎯 Overview

The **Operational Center (Command Center)** serves as the central hub for the CIS Center Intelligence System. It stores processed intelligence data, hosts the real-time dashboard, manages cross-repository communication, and provides API access for mobile interfaces.

## 🚀 Features

### Central Intelligence Storage
- **master_intel.json** - Primary intelligence database
- **Real-time Updates** - Automatic data refresh every 30 minutes
- **Historical Tracking** - Timestamp-based data versioning
- **Cross-platform Access** - JSON format for universal compatibility

### Real-time Dashboard
- **Live Intelligence Feed** - Current market insights
- **Sentiment Analytics** - Visual sentiment indicators
- **Source Reliability** - Performance-based scoring
- **Mobile Responsive** - Optimized for all devices

### API Integration
- **Repository Dispatch Receiver** - Accepts data from Repository A
- **Discord Notifications** - Automated intelligence alerts
- **Mobile Command Interface** - Termux integration support
- **Webhook Support** - External system integration

## 📊 Dashboard Access

### Web Interface
```
🔗 Main Dashboard: https://fatim1509.github.io/cis-operational-center/dashboard/
📱 Mobile Optimized: Yes
🔄 Auto-refresh: Every 5 minutes
```

### Dashboard Features
- **Intelligence Timeline** - Chronological intelligence feed
- **Sentiment Heatmap** - Color-coded sentiment indicators
- **Source Performance** - Reliability tracking charts
- **Consensus Scoring** - Weighted intelligence verification
- **Export Options** - CSV/JSON data export

## 📁 Data Structure

### master_intel.json
```json
{
  "last_updated": "2026-04-11T15:30:00Z",
  "intelligence_count": 247,
  "sources": ["reuters", "investing", "tradingeconomics", "finviz", "twitter"],
  "intelligence": [
    {
      "id": "intel_202604111530_001",
      "timestamp": "2026-04-11T15:30:00Z",
      "source": "reuters",
      "headline": "Tech Stocks Show Strong Bullish Momentum",
      "sentiment_score": 0.78,
      "consensus_score": 0.85,
      "reliability": 0.92,
      "category": "technology",
      "urgency": "high",
      "url": "https://reuters.com/article/...",
      "metadata": {
        "author": "Reuters Staff",
        "processing_time": "2.3s",
        "duplicates_removed": 2
      }
    }
  ]
}
```

### Data Schema
| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique intelligence identifier |
| `timestamp` | datetime | Processing timestamp |
| `source` | string | Origin data source |
| `headline` | string | Intelligence headline |
| `sentiment_score` | float | -1.0 to 1.0 sentiment rating |
| `consensus_score` | float | 0.0 to 1.0 verification score |
| `reliability` | float | Source reliability percentage |
| `category` | string | Financial category |
| `urgency` | string | Priority level |

## ⚙️ Repository Integration

### Receiving Data from Repository A
```bash
# Repository A sends data via GitHub API
curl -X POST \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Authorization: token YOUR_GITHUB_TOKEN" \
  https://api.github.com/repos/Fatim1509/cis-operational-center/dispatches \
  -d '{
    "event_type": "intelligence_received",
    "client_payload": {
      "intelligence": [/* processed data */],
      "source": "reuters",
      "timestamp": "2026-04-11T15:30:00Z"
    }
  }'
```

### Processing Workflow (`receive.yml`)
1. **Receive Dispatch** - Accept data from Repository A
2. **Validate JSON** - Ensure data integrity
3. **Update Storage** - Append to master_intel.json
4. **Notify Discord** - Send alerts via webhook
5. **Update Dashboard** - Refresh display data

## 🔔 Discord Integration

### Automatic Notifications
- **New Intelligence** - Real-time alerts for high-priority items
- **System Status** - Daily operational summaries
- **Error Alerts** - Processing failure notifications
- **Threshold Alerts** - Significant sentiment changes

### Webhook Configuration
```json
{
  "webhook_url": "https://discord.com/api/webhooks/YOUR_WEBHOOK",
  "notification_rules": {
    "high_priority": true,
    "sentiment_change": 0.3,
    "system_errors": true,
    "daily_summary": "18:00"
  }
}
```

## 📱 Mobile Interface

### Termux Integration
```bash
# Install and run on Android
pkg install python git
git clone https://github.com/Fatim1509/cis-discord-bot.git
cd cis-discord-bot
pip install -r requirements.txt
python termux.py
```

### Mobile Commands
- `!intel` - Get latest intelligence summary
- `!status` - Check system operational status
- `!approve [id]` - Approve intelligence item
- `!reject [id]` - Reject intelligence item

## 🚀 GitHub Pages Setup

### Enable Pages
```
1. Navigate to: https://github.com/Fatim1509/cis-operational-center/settings/pages
2. Source: Deploy from branch → main
3. Branch: main → /docs folder
4. Click "Save"
5. Wait 2-3 minutes for deployment
```

### Pages Configuration (`pages.yml`)
- **Trigger**: Push to main branch
- **Build**: Static HTML from `/docs`
- **Deploy**: GitHub Pages hosting
- **URL**: `https://fatim1509.github.io/cis-operational-center/`

## 🔗 API Endpoints

### Raw Data Access
```bash
# Get master intelligence
curl https://raw.githubusercontent.com/Fatim1509/cis-operational-center/main/data/master_intel.json

# Get last update timestamp
curl https://raw.githubusercontent.com/Fatim1509/cis-operational-center/main/data/last_update.txt

# Get dashboard data
curl https://fatim1509.github.io/cis-operational-center/dashboard/data/current.json
```

### GitHub API
```bash
# Get repository contents
curl -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/Fatim1509/cis-operational-center/contents/data

# Trigger processing (authenticated)
curl -X POST \
  -H "Authorization: token YOUR_GITHUB_TOKEN" \
  https://api.github.com/repos/Fatim1509/cis-operational-center/dispatches \
  -d '{"event_type":"process_intelligence"}'
```

## 📈 Performance Monitoring

### System Metrics
- **Data Processing**: < 30 seconds per batch
- **Dashboard Load**: < 2 seconds
- **API Response**: < 500ms
- **Uptime**: 99.9% (GitHub Pages reliability)

### Health Checks
```bash
# Check system status
curl -s https://api.github.com/repos/Fatim1509/cis-operational-center/commits/main | 
  jq -r '.commit.author.date'
# Should return recent timestamp
```

## 🔒 Security & Privacy

### Data Protection
- **No Personal Data**: Only processes public financial information
- **HTTPS Only**: All communications encrypted
- **Access Control**: GitHub authentication required
- **Audit Trail**: Complete logging of all operations

### Access Control
- **Repository Access**: Private by default
- **Token-based Auth**: Required for API operations
- **Webhook Security**: Discord webhook validation
- **Rate Limiting**: Respects GitHub API limits

## 🛠️ Configuration

### Environment Variables
```bash
# GitHub Secrets (Settings → Secrets → Actions)
REPO_B_TOKEN=ghp_your_github_token
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
DISCORD_BOT_TOKEN=your_discord_bot_token
```

### Customization Options
- **Update Frequency**: Modify GitHub Actions schedule
- **Notification Rules**: Adjust Discord webhook triggers
- **Dashboard Styling**: Edit `/docs/dashboard/style.css`
- **Data Retention**: Configure cleanup policies

## 📊 Analytics & Reporting

### Built-in Analytics
- **Source Performance**: Reliability tracking per data source
- **Processing Times**: Efficiency monitoring
- **Error Rates**: Failure tracking and alerting
- **Usage Statistics**: Dashboard visit metrics

### Export Options
- **JSON Format**: Raw data for external processing
- **CSV Export**: Spreadsheet-compatible format
- **Real-time Feed**: Live data stream via API
- **Historical Data**: Time-series analysis support

## 🔗 System Integration

This repository is designed to work seamlessly with:
- **[Repository A](https://github.com/Fatim1509/cis-logic-refinery)** - Data processing and scraping
- **[Discord Bot](https://github.com/Fatim1509/cis-discord-bot)** - Mobile command interface

---

<p align="center">
  <b>🎯 Central command for your intelligence operations</b><br>
  <i>Part of the CIS Center Intelligence System</i>
</p>