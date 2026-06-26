#!/usr/bin/env python3
from datetime import datetime
"""Plot exploration timeline for BPFOptBench paper."""

import json
import re
from datetime import datetime
from pathlib import Path
from collections import defaultdict

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

plt.rcParams.update({
    'font.size': 13,
    'font.family': 'serif',
    'axes.labelsize': 15,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'legend.fontsize': 10,
    'figure.figsize': (9, 3),
    'axes.grid': True,
    'grid.alpha': 0.3,
})

BASE_DIR = Path('/home/yunwei37/workspace/bpf-benchmark')
SOURCE_OPT_DIR = BASE_DIR / 'docs/source-opt'
CORPUS_DIR = BASE_DIR / 'corpus/results'
MICRO_DIR = BASE_DIR / 'micro/results'

app_colors = {
    'cilium': '#1f77b4',
    'tetragon': '#ff7f0e',
    'katran': '#2ca02c',
    'micro_x86': '#d62728',
    'micro_arm64': '#9467bd',
}

def parse_timestamp(dirname):
    match = re.search(r'(\d{8})_(\d{6})', dirname)
    if match:
        date_str = match.group(1)
        if date_str.startswith('1970'):
            return None
        return datetime.strptime(f'{date_str}_{match.group(2)}', '%Y%m%d_%H%M%S')
    return None

def extract_pps(stdout):
    match = re.search(r'(\d+)pps', stdout)
    return int(match.group(1)) if match else 0

def load_corpus_data():
    app_runs = defaultdict(list)
    
    for result_dir in sorted(CORPUS_DIR.iterdir()):
        if not result_dir.is_dir():
            continue
        if 'kprog' in result_dir.name.lower() or 'kinsn' in result_dir.name.lower():
            continue
        
        ts = parse_timestamp(result_dir.name)
        if not ts:
            continue
        
        apps_dir = result_dir / 'details/apps'
        if not apps_dir.exists():
            continue
        
        for app_json in apps_dir.glob('*.json'):
            app_name = app_json.stem.replace('__', '/').split('/')[0].lower()
            if app_name not in ['cilium', 'tetragon', 'katran']:
                continue
            
            try:
                with open(app_json) as f:
                    data = json.load(f)
                
                baseline = data.get('baseline', {})
                workloads = baseline.get('workloads', [])
                
                metric = None
                for w in workloads:
                    for c in w.get('components', []):
                        pps = extract_pps(c.get('stdout', ''))
                        if pps > 0:
                            metric = pps
                            break
                
                if metric and metric > 0:
                    app_runs[app_name].append((ts, metric))
            except:
                continue
    
    data = defaultdict(list)
    for app, runs in app_runs.items():
        if len(runs) < 3:
            continue
        runs.sort(key=lambda x: x[0])
        baseline = np.median([r[1] for r in runs[:3]])
        
        for ts, metric in runs:
            improvement = ((metric - baseline) / baseline) * 100
            if -40 <= improvement <= 40:
                data[app].append({'timestamp': ts, 'improvement': improvement})
    
    return data

def load_micro_data():
    """Load micro benchmark data - correct structure"""
    data = {'micro_x86': [], 'micro_arm64': []}
    
    for result_dir in sorted(MICRO_DIR.iterdir()):
        if not result_dir.is_dir():
            continue
        if 'kprog' in result_dir.name.lower() or 'kinsn' in result_dir.name.lower():
            continue
        
        ts = parse_timestamp(result_dir.name)
        if not ts:
            continue
        
        if 'x86' in result_dir.name or 'kvm' in result_dir.name:
            platform = 'micro_x86'
        elif 'arm64' in result_dir.name:
            platform = 'micro_arm64'
        else:
            continue
        
        result_json = result_dir / 'details/result.json'
        if not result_json.exists():
            continue
        
        try:
            with open(result_json) as f:
                result = json.load(f)
            
            benchmarks = result.get('benchmarks', [])
            exec_times = []
            
            for bench in benchmarks:
                for run in bench.get('runs', []):
                    # Only use kernel runtime
                    if run.get('runtime') != 'kernel':
                        continue
                    for sample in run.get('samples', []):
                        exec_ns = sample.get('exec_ns', 0)
                        if exec_ns > 0:
                            exec_times.append(exec_ns)
            
            if exec_times:
                avg_exec = np.mean(exec_times)
                data[platform].append((ts, avg_exec))
        except Exception as e:
            continue
    
    result = defaultdict(list)
    for platform, runs in data.items():
        if len(runs) < 3:
            print(f"  {platform}: only {len(runs)} runs")
            continue
        runs.sort(key=lambda x: x[0])
        baseline = np.median([r[1] for r in runs[:3]])
        
        for ts, metric in runs:
            # Lower exec time is better
            improvement = ((baseline - metric) / baseline) * 100
            if -40 <= improvement <= 40:
                result[platform].append({'timestamp': ts, 'improvement': improvement})
    
    return result

def load_source_opt_data():
    data = defaultdict(list)
    
    for app_dir in SOURCE_OPT_DIR.iterdir():
        if not app_dir.is_dir() or app_dir.name in ['README.md']:
            continue
        
        app_name = app_dir.name.split('-')[0].lower()
        if 'kprog' in app_dir.name.lower() or 'otel' in app_dir.name.lower():
            continue
        if app_name not in ['cilium', 'tetragon', 'katran']:
            continue
        
        summary = app_dir / 'SUMMARY.md'
        if not summary.exists():
            continue
        
        with open(summary) as f:
            content = f.read()
        
        for line in content.split('\n'):
            if 'corpus_' not in line:
                continue
            
            ts_match = re.search(r'corpus_(\d{8})_(\d{6})', line)
            if not ts_match:
                continue
            
            for pattern in [r'([+-]?\d+\.?\d*)%\s*vs', r'\(([+-]?\d+\.?\d*)%', r'`([+-]?\d+\.?\d*)%`']:
                imp_match = re.search(pattern, line)
                if imp_match:
                    ts = datetime.strptime(f'{ts_match.group(1)}_{ts_match.group(2)}', '%Y%m%d_%H%M%S')
                    improvement = float(imp_match.group(1))
                    if -40 <= improvement <= 40:
                        data[app_name].append({'timestamp': ts, 'improvement': improvement})
                    break
    
    return data

def main():
    print("Loading data...")
    corpus_data = load_corpus_data()
    source_data = load_source_opt_data()
    micro_data = load_micro_data()
    
    all_data = defaultdict(list)
    for app, pts in corpus_data.items():
        all_data[app].extend(pts)
    for app, pts in source_data.items():
        all_data[app].extend(pts)
    for platform, pts in micro_data.items():
        all_data[platform].extend(pts)
    
    for app in all_data:
        all_data[app].sort(key=lambda x: x['timestamp'])
    
    total = 0
    for app, pts in all_data.items():
        if pts:
            imps = [p['improvement'] for p in pts]
            print(f"{app}: {len(pts)} pts, [{min(imps):.1f}%, {max(imps):.1f}%]")
            total += len(pts)
    print(f"Total: {total} points")
    
    fig, ax = plt.subplots()
    
    display_names = {
        'cilium': 'Cilium',
        'tetragon': 'Tetragon', 
        'katran': 'Katran',
        'micro_x86': 'Micro x86',
        'micro_arm64': 'Micro ARM64',
    }
    
    for app, pts in all_data.items():
        if app not in app_colors or not pts:
            continue
        times = [p['timestamp'] for p in pts]
        imps = [p['improvement'] for p in pts]
        ax.plot(times, imps, 'o-', color=app_colors[app], 
                label=display_names.get(app, app), alpha=0.7, markersize=4, linewidth=1)
    
    ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.8, alpha=0.6)
    
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO, interval=2))
    plt.gcf().autofmt_xdate()
    
    # ax.set_xlabel('Date (2026)')
    ax.set_ylabel('Improvement (%)')
    ax.set_ylim(-40, 40)
    ax.set_xlim(datetime(2026, 5, 1), datetime(2026, 6, 30))
    
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.25), ncol=5, fontsize=11)
    plt.tight_layout()
    
    out_dir = Path('/home/yunwei37/workspace/bpf-benchmark/docs/ebpf27-bpfoptbench')
    plt.savefig(out_dir / 'timeline.pdf', dpi=300, bbox_inches='tight')
    plt.savefig(out_dir / 'timeline.png', dpi=150, bbox_inches='tight')
    print("\nSaved timeline.pdf and timeline.png")

if __name__ == '__main__':
    main()
