#!/usr/bin/env python3
"""
CIS Discord Notifier

Sends notifications to Discord about intelligence updates.
"""

import json
import logging
import argparse
import requests
from datetime import datetime

logger = logging.getLogger(__name__)

class DiscordNotifier:
    """Handles Discord notifications"""
    
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
    
    def send_notification(self, message: str, embeds: list = None) -> bool:
        """Send notification to Discord"""
        try:
            payload = {
                'content': message,
                'username': 'CIS Intelligence',
                'avatar_url': 'https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png'
            }
            
            if embeds:
                payload['embeds'] = embeds
            
            response = requests.post(self.webhook_url, json=payload)
            
            if response.status_code == 204:
                logger.info("✅ Discord notification sent")
                return True
            else:
                logger.error(f"❌ Discord notification failed: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Discord notification error: {e}")
            return False
    
    def send_intelligence_update(self, summary: dict) -> bool:
        """Send intelligence update notification"""
        try:
            breakdown = summary.get('sentiment_breakdown', {})
            total = summary.get('total_signals', 0)
            avg_confidence = summary.get('avg_confidence', 0)
            
            message = f"🎯 **CIS Intelligence Update**\n"
            message += f"📊 {total} new signals analyzed\n"
            message += f"📈 Positive: {breakdown.get('positive', 0)} | "
            message += f"📉 Negative: {breakdown.get('negative', 0)} | "
            message += f"➡️ Neutral: {breakdown.get('neutral', 0)}\n"
            message += f"🎯 Average confidence: {avg_confidence:.2%}"
            
            embed = {
                'title': 'CIS Intelligence Summary',
                'description': f'Updated at {datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")}',
                'color': 0x00ff00,  # Green
                'fields': [
                    {
                        'name': 'Total Signals',
                        'value': str(total),
                        'inline': True
                    },
                    {
                        'name': 'Avg Confidence',
                        'value': f"{avg_confidence:.1%}",
                        'inline': True
                    }
                ]
            }
            
            return self.send_notification(message, [embed])
            
        except Exception as e:
            logger.error(f"❌ Intelligence update failed: {e}")
            return False

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Send Discord notifications')
    parser.add_argument('--webhook', required=True, help='Discord webhook URL')
    parser.add_argument('--status', choices=['success', 'failure'], default='success', help='Notification status')
    parser.add_argument('--message', help='Custom message')
    
    args = parser.parse_args()
    
    logging.basicConfig(level=logging.INFO)
    
    notifier = DiscordNotifier(args.webhook)
    
    if args.message:
        success = notifier.send_notification(args.message)
    else:
        # Default intelligence update
        summary = {
            'total_signals': 25,
            'sentiment_breakdown': {'positive': 12, 'negative': 5, 'neutral': 8},
            'avg_confidence': 0.75
        }
        success = notifier.send_intelligence_update(summary)
    
    exit(0 if success else 1)

if __name__ == "__main__":
    main()