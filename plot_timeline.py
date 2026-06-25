#!/usr/bin/env python3
"""Generate exploration timeline figure for BPFOptBench paper."""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from datetime import datetime, timedelta

# Session data (aggregated from exploration-process-analysis.md)
data = {
    # (start_date, end_date, platform, config_type, session_count)
    "May 21-24 intensive": ("2026-05-21", "2026-05-24", "x86", "mixed", 515),
    "May 7-8 noise floor": ("2026-05-07", "2026-05-08", "x86", "baseline", 150),
    "May 27-29 stabilization": ("2026-05-27", "2026-05-29", "x86", "pipeline", 200),
    "Jun 2 LEA debug": ("2026-06-02", "2026-06-02", "x86", "debug", 94),
    "Jun 3 kinsn breakthrough": ("2026-06-03", "2026-06-03", "x86", "kinsn", 50),
    "Jun 14-17 ARM64": ("2026-06-14", "2026-06-17", "arm64", "kinsn", 174),
}

# Key discoveries to annotate
discoveries = [
    ("2026-05-08", "Noise floor\n4.3% discovered"),
    ("2026-06-02", "LEA crash\n82% failure"),
    ("2026-06-03", "Kinsn breakthrough\n0.94x (6% speedup)"),
    ("2026-06-06", "ARM64 kinsn\n1.21x (21% speedup)"),
]

# Colors for config types
colors = {
    "baseline": "#808080",  # gray
    "mixed": "#4169E1",     # royal blue
    "pipeline": "#32CD32",  # lime green
    "debug": "#FF4500",     # orange red
    "kinsn": "#9932CC",     # dark orchid
}

fig, ax = plt.subplots(figsize=(10, 4))

# Parse dates
def parse_date(s):
    return datetime.strptime(s, "%Y-%m-%d")

base_date = parse_date("2026-05-01")

y_positions = {"x86": 1, "arm64": 0}

for name, (start, end, platform, config, count) in data.items():
    start_d = parse_date(start)
    end_d = parse_date(end)
    x_start = (start_d - base_date).days
    width = max(1, (end_d - start_d).days + 1)
    y = y_positions[platform]

    # Bar height proportional to session count (normalized)
    height = 0.3 + 0.4 * min(count / 515, 1.0)

    rect = mpatches.FancyBboxPatch(
        (x_start, y - height/2), width, height,
        boxstyle="round,pad=0.02",
        facecolor=colors[config],
        edgecolor="black",
        alpha=0.8
    )
    ax.add_patch(rect)

    # Add session count label
    if count >= 100:
        ax.text(x_start + width/2, y, f"{count}",
                ha='center', va='center', fontsize=8, color='white', fontweight='bold')

# Add discovery annotations
for date_str, text in discoveries:
    d = parse_date(date_str)
    x = (d - base_date).days
    ax.annotate(text, xy=(x, 1.5), xytext=(x, 2.2),
                ha='center', va='bottom', fontsize=7,
                arrowprops=dict(arrowstyle='->', color='black', lw=0.8),
                bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', edgecolor='gray'))

# Formatting
ax.set_xlim(-2, 50)
ax.set_ylim(-0.8, 3)
ax.set_yticks([0, 1])
ax.set_yticklabels(['ARM64', 'x86'])
ax.set_xlabel('Days since May 1, 2026')
ax.set_ylabel('Platform')
ax.set_title('BPFOptBench Exploration Timeline: 2,874 Sessions Across 25 Pass Configurations')

# X-axis labels
tick_positions = [0, 7, 14, 21, 28, 35, 42]
tick_labels = ['May 1', 'May 8', 'May 15', 'May 22', 'May 29', 'Jun 5', 'Jun 12']
ax.set_xticks(tick_positions)
ax.set_xticklabels(tick_labels, fontsize=8)

# Legend
legend_patches = [
    mpatches.Patch(color=colors["baseline"], label="Baseline calibration"),
    mpatches.Patch(color=colors["mixed"], label="Mixed exploration"),
    mpatches.Patch(color=colors["pipeline"], label="Full pipeline"),
    mpatches.Patch(color=colors["debug"], label="Debug iteration"),
    mpatches.Patch(color=colors["kinsn"], label="Kinsn evaluation"),
]
ax.legend(handles=legend_patches, loc='upper right', fontsize=7, ncol=2)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('/home/yunwei37/workspace/bpf-benchmark/docs/ebpf27-bpfoptbench/timeline.pdf',
            bbox_inches='tight', dpi=300)
plt.savefig('/home/yunwei37/workspace/bpf-benchmark/docs/ebpf27-bpfoptbench/timeline.png',
            bbox_inches='tight', dpi=300)
print("Saved timeline.pdf and timeline.png")
