# cli.py
import argparse
from auto_responder import process_emails

def main():
    parser = argparse.ArgumentParser(
        description="Auto-respond to Gmail emails based on rules"
    )
    parser.add_argument(
        '--config', 
        default='config.json',
        help='Path to config file (default: config.json)'
    )
    parser.add_argument(
        '--log', 
        default='email_logs.csv',
        help='Path to log file (default: email_logs.csv)'
    )
    args = parser.parse_args()
    
    print(f"Starting with config: {args.config}, logs: {args.log}")
    process_emails(config_path=args.config, log_path=args.log)

if __name__ == '__main__':
    main()