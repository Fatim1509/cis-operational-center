#!/usr/bin/env python3
"""
CIS Intelligence Processor

Processes incoming intelligence data and updates the master database.
"""

import json
import logging
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List

logger = logging.getLogger(__name__)

class IntelligenceProcessor:
    """Processes incoming intelligence data"""
    
    def __init__(self):
        self.master_data = {
            'last_updated': datetime.utcnow().isoformat(),
            'version': '1.0.0',
            'signals': [],
            'metadata': {}
        }
    
    def load_master_intel(self, filepath: str) -> Dict:
        """Load existing master intelligence data"""
        try:
            if Path(filepath).exists():
                with open(filepath, 'r') as f:
                    return json.load(f)
            else:
                logger.info("No existing master intel found, creating new")
                return self.master_data.copy()
        except Exception as e:
            logger.error(f"Error loading master intel: {e}")
            return self.master_data.copy()
    
    def process_incoming_intel(self, incoming_data: Dict) -> List[Dict]:
        """Process incoming intelligence data"""
        signals = []
        
        # Extract signals from different payload formats
        if 'signals' in incoming_data:
            signals.extend(incoming_data['signals'])
        elif 'verified_items' in incoming_data:
            # From consensus engine
            for item in incoming_data['verified_items']:
                signals.append({
                    'id': f"intel_{datetime.utcnow().timestamp()}",
                    'title': item.get('title', 'Unknown'),
                    'sentiment': item.get('sentiment', 'neutral'),
                    'confidence': item.get('confidence', 0.5),
                    'source': item.get('source', 'unknown'),
                    'timestamp': item.get('timestamp', datetime.utcnow().isoformat()),
                    'processed': True
                })
        else:
            # Direct payload
            signals.append({
                'id': f"intel_{datetime.utcnow().timestamp()}",
                'title': incoming_data.get('message', 'Unknown intelligence'),
                'sentiment': incoming_data.get('sentiment', 'neutral'),
                'confidence': incoming_data.get('confidence', 0.5),
                'source': incoming_data.get('source', 'unknown'),
                'timestamp': incoming_data.get('timestamp', datetime.utcnow().isoformat()),
                'processed': True
            })
        
        return signals
    
    def merge_signals(self, existing_signals: List[Dict], new_signals: List[Dict]) -> List[Dict]:
        """Merge new signals with existing ones"""
        # Remove duplicates based on title
        existing_titles = {signal.get('title', '') for signal in existing_signals}
        
        merged_signals = existing_signals.copy()
        
        for signal in new_signals:
            title = signal.get('title', '')
            if title and title not in existing_titles:
                merged_signals.append(signal)
                existing_titles.add(title)
        
        # Keep only recent signals (last 100)
        merged_signals.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        return merged_signals[:100]
    
    def generate_summary(self, signals: List[Dict]) -> Dict:
        """Generate summary statistics"""
        if not signals:
            return {
                'total_signals': 0,
                'sentiment_breakdown': {'positive': 0, 'negative': 0, 'neutral': 0},
                'avg_confidence': 0.0,
                'sources': []
            }
        
        # Sentiment breakdown
        sentiments = [signal.get('sentiment', 'neutral') for signal in signals]
        sentiment_breakdown = {
            'positive': sentiments.count('positive'),
            'negative': sentiments.count('negative'),
            'neutral': sentiments.count('neutral')
        }
        
        # Average confidence
        confidences = [signal.get('confidence', 0.5) for signal in signals]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
        
        # Unique sources
        sources = list(set(signal.get('source', 'unknown') for signal in signals))
        
        return {
            'total_signals': len(signals),
            'sentiment_breakdown': sentiment_breakdown,
            'avg_confidence': round(avg_confidence, 3),
            'sources': sources,
            'last_updated': datetime.utcnow().isoformat()
        }
    
    def process(self, incoming_intel_path: str, master_intel_path: str) -> bool:
        """Process incoming intelligence"""
        try:
            logger.info(f"📥 Processing intelligence from {incoming_intel_path}")
            
            # Load incoming data
            with open(incoming_intel_path, 'r') as f:
                incoming_data = json.load(f)
            
            # Load existing master data
            master_data = self.load_master_intel(master_intel_path)
            existing_signals = master_data.get('signals', [])
            
            # Process new signals
            new_signals = self.process_incoming_intel(incoming_data)
            logger.info(f"🔄 Processing {len(new_signals)} new signals")
            
            # Merge signals
            merged_signals = self.merge_signals(existing_signals, new_signals)
            
            # Generate summary
            summary = self.generate_summary(merged_signals)
            
            # Update master data
            master_data.update({
                'signals': merged_signals,
                'summary': summary,
                'last_updated': datetime.utcnow().isoformat(),
                'metadata': {
                    'version': '1.0.0',
                    'processor': 'cis-intelligence-processor',
                    'processed_count': len(new_signals),
                    'total_count': len(merged_signals)
                }
            })
            
            # Save updated master data
            with open(master_intel_path, 'w') as f:
                json.dump(master_data, f, indent=2, default=str)
            
            logger.info(f"✅ Intelligence processed: {len(merged_signals)} total signals")
            logger.info(f"📊 Summary: {summary['sentiment_breakdown']}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Intelligence processing failed: {e}")
            return False

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Process CIS intelligence data')
    parser.add_argument('--input', required=True, help='Input intelligence file')
    parser.add_argument('--output', required=True, help='Output master intel file')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    
    args = parser.parse_args()
    
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    
    processor = IntelligenceProcessor()
    success = processor.process(args.input, args.output)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()