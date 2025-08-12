# cli.py
import argparse
import os
import sys
import json
from typing import Optional
from auto_responder import process_emails

def handle_errors(config_path: str, log_path: str, verbose: bool = False) -> Optional[str]:
    """Centralized error handler with user-friendly messages"""
    try:
        # Config file validation
        if not os.path.exists(config_path):
            available_files = "\n- ".join([f for f in os.listdir('.') 
                                        if f.endswith('.json') and f != 'credentials.json'])
            return (
                f"Error: Config file '{config_path}' not found.\n\n"
                f"Available config files in this directory:\n- {available_files or 'None found'}\n\n"
                "Tip: Create a new config file by copying config.json:\n"
                "cp config.json my_config.json"
            )
            
        # Log file permissions check
        log_dir = os.path.dirname(log_path) or '.'
        if not os.path.exists(log_dir):
            return f"Error: Log directory '{log_dir}' does not exist"
        if os.path.exists(log_path) and not os.access(log_path, os.W_OK):
            return f"Error: No write permissions for log file '{log_path}'"
            
        # Process emails with optional verbose output
        if verbose:
            print("\n🔍 Debug Mode Activated")
            print("----------------------")
            process_emails(config_path, log_path)
        else:
            process_emails(config_path, log_path)
            
    except json.JSONDecodeError as e:
        return (
            f"Invalid JSON in '{config_path}':\n"
            f"Line {e.lineno}: {e.msg}\n\n"
            "Tip: Validate your JSON at https://jsonlint.com/"
        )
    except Exception as e:
        error_type = type(e).__name__
        return (
            f"🚨 {error_type} occurred during processing:\n"
            f"- {str(e)}\n\n"
            "Debug Tips:\n"
            "1. Run with --verbose for details\n"
            "2. Check Google OAuth permissions at https://console.cloud.google.com/\n"
            "3. Validate your config.json syntax\n"
            "4. Ensure token.json exists in your project directory"
        )
    return None

def show_help_tips():
    """Additional help information"""
    print("\n💡 Usage Tips:")
    print("- First run: python auth.py to set up authentication")
    print("- Test config: python cli.py --verbose")
    print("- Custom logs: python cli.py --log /path/to/custom_log.csv")

def main():
    parser = argparse.ArgumentParser(
        description="📧 Gmail Auto-Responder: Automated email replies based on rules",
        epilog="Example: python cli.py --config custom_config.json --verbose",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '--config', 
        default='config.json',
        help='Path to config JSON file\n(default: config.json)'
    )
    parser.add_argument(
        '--log', 
        default='email_logs.csv',
        help='Path to output log file\n(default: email_logs.csv)'
    )
    parser.add_argument(
        '--verbose', 
        action='store_true',
        help='Show detailed processing information'
    )
    args = parser.parse_args()
    
    print(f"\n⚙️ Starting with:")
    print(f"- Config: {args.config}")
    print(f"- Log: {args.log}")
    if args.verbose:
        print(f"- Mode: Verbose")
    
    if error := handle_errors(args.config, args.log, args.verbose):
        print(f"\n❌ {error}", file=sys.stderr)
        show_help_tips()
        sys.exit(1)
        
    print("\n✅ Processing completed successfully")

if __name__ == '__main__':
    main()