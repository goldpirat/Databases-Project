import os
import re
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter, defaultdict
from user_agents import parse
import seaborn as sns

def parse_access_logs(log_path):
    """Enhanced access log parser with detailed statistics"""
    access_data = []
    log_format = re.compile(
        r'(?P<ip>\S+) - - \[(?P<datetime>[^\]]+)\] "(?P<request_method>\S+) (?P<url>\S+) (?P<protocol>[^"]+)" (?P<status>\d+) (?P<size>\S+) "(?P<referrer>[^"]+)" "(?P<user_agent>[^"]+)"'
    )
    
    # Statistics containers
    page_counts = Counter()
    ip_access = defaultdict(list)
    browser_stats = Counter()
    hourly_stats = defaultdict(int)
    
    with open(log_path, 'r') as file:
        for line in file:
            match = log_format.match(line)
            if match:
                entry = match.groupdict()
                entry["datetime"] = datetime.strptime(entry["datetime"], "%d/%b/%Y:%H:%M:%S %z")
                
                # Collect statistics
                page_counts[entry['url']] += 1
                ip_access[entry['ip']].append(entry['datetime'])
                
                # Parse user agent for browser information
                try:
                    ua = parse(entry['user_agent'])
                    browser_stats[f"{ua.browser.family} {ua.browser.version_string}"] += 1
                except:
                    browser_stats["Unknown"] += 1
                
                # Collect hourly statistics
                hour = entry['datetime'].strftime('%Y-%m-%d %H:00')
                hourly_stats[hour] += 1
                
                access_data.append(entry)
    
    return {
        'raw_data': access_data,
        'page_counts': dict(page_counts),
        'ip_access': dict(ip_access),
        'browser_stats': dict(browser_stats),
        'hourly_stats': dict(hourly_stats)
    }

def parse_error_logs(log_path):
    """Enhanced error log parser with detailed statistics"""
    error_data = []
    error_stats = defaultdict(lambda: defaultdict(int))
    ip_errors = defaultdict(list)
    
    error_format = re.compile(
        r'\[(?P<datetime>[^\]]+)\] \[(?P<level>[^\]]+)\] \[pid (?P<pid>\d+)\] \[client (?P<client_ip>\S+):\d+\] (?P<message>.+)'
    )
    
    with open(log_path, 'r') as file:
        for line in file:
            match = error_format.match(line)
            if match:
                entry = match.groupdict()
                entry["datetime"] = datetime.strptime(entry["datetime"], "%a %b %d %H:%M:%S.%f %Y")
                
                # Collect error statistics
                error_stats[entry['level']][entry['client_ip']] += 1
                ip_errors[entry['client_ip']].append({
                    'datetime': entry['datetime'],
                    'level': entry['level'],
                    'message': entry['message']
                })
                
                error_data.append(entry)
    
    return {
        'raw_data': error_data,
        'error_stats': dict(error_stats),
        'ip_errors': dict(ip_errors)
    }

def plot_access_timeline(access_data):
    """Enhanced access timeline visualization"""
    try:
        # Create DataFrame from raw data
        df = pd.DataFrame(access_data['raw_data'])
        df['datetime'] = pd.to_datetime(df['datetime'])
        
        # Create subplots
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(15, 18))
        
        # Plot 1: Access Timeline
        df.set_index('datetime').resample('1H').size().plot(ax=ax1)
        ax1.set_title("Hourly Access Timeline")
        ax1.set_xlabel("Time")
        ax1.set_ylabel("Access Count")
        
        # Plot 2: Top 10 Pages
        pd.Series(access_data['page_counts']).nlargest(10).plot(kind='bar', ax=ax2)
        ax2.set_title("Top 10 Accessed Pages")
        ax2.set_xlabel("URL")
        ax2.set_ylabel("Access Count")
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # Plot 3: Browser Distribution
        pd.Series(access_data['browser_stats']).plot(kind='pie', ax=ax3)
        ax3.set_title("Browser Distribution")
        
        plt.tight_layout()
        
        # Save the plot
        img_dir = "/home/kflori/public_html/server/templates/static/img"
        os.makedirs(img_dir, exist_ok=True)
        plt.savefig(os.path.join(img_dir, "access_analysis.png"))
        plt.close()
        
    except Exception as e:
        print(f"An error occurred while plotting access timeline: {e}")

def plot_error_timeline(error_data):
    """Enhanced error timeline visualization"""
    try:
        # Create DataFrame from raw data
        df = pd.DataFrame(error_data['raw_data'])
        df['datetime'] = pd.to_datetime(df['datetime'])
        
        # Create subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12))
        
        # Plot 1: Error Timeline
        df.set_index('datetime').resample('1H').size().plot(ax=ax1)
        ax1.set_title("Hourly Error Timeline")
        ax1.set_xlabel("Time")
        ax1.set_ylabel("Error Count")
        
        # Plot 2: Error Distribution by Level and IP
        error_matrix = pd.DataFrame(error_data['error_stats']).fillna(0)
        sns.heatmap(error_matrix, ax=ax2, cmap='YlOrRd', annot=True, fmt='g')
        ax2.set_title("Error Distribution by Level and IP")
        
        plt.tight_layout()
        
        # Save the plot
        img_dir = "/home/kflori/public_html/server/templates/static/img"
        os.makedirs(img_dir, exist_ok=True)
        plt.savefig(os.path.join(img_dir, "error_analysis.png"))
        plt.close()
        
    except Exception as e:
        print(f"An error occurred while plotting error timeline: {e}")
