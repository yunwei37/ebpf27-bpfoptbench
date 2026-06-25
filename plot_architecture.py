#!/usr/bin/env python3
"""Generate architecture figure for BPFOptBench paper."""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.lines as mlines

fig, ax = plt.subplots(figsize=(10, 6))

# Colors
AGENT_COLOR = '#E6F3FF'      # light blue
FRAMEWORK_COLOR = '#FFF3E6'  # light orange
EXEC_COLOR = '#E6FFE6'       # light green
FEEDBACK_COLOR = '#FFE6F3'   # light pink
BORDER_COLOR = '#333333'

def draw_box(ax, x, y, w, h, text, color, fontsize=9, bold=False):
    box = FancyBboxPatch((x, y), w, h,
                         boxstyle="round,pad=0.02,rounding_size=0.1",
                         facecolor=color, edgecolor=BORDER_COLOR, linewidth=1.5)
    ax.add_patch(box)
    weight = 'bold' if bold else 'normal'
    ax.text(x + w/2, y + h/2, text, ha='center', va='center',
            fontsize=fontsize, fontweight=weight, wrap=True)

def draw_arrow(ax, start, end, color='black', style='->', connectionstyle='arc3,rad=0'):
    arrow = FancyArrowPatch(start, end,
                            arrowstyle=style,
                            mutation_scale=15,
                            connectionstyle=connectionstyle,
                            color=color, linewidth=1.5)
    ax.add_patch(arrow)

# === Layer 1: LLM Agent ===
draw_box(ax, 0.5, 5.2, 9, 0.8, '', AGENT_COLOR)
ax.text(5, 5.85, 'LLM Agent Layer', ha='center', fontsize=11, fontweight='bold')

draw_box(ax, 0.8, 5.3, 2.2, 0.6, 'Claude Code\n(267 bash calls)', 'white', 8)
draw_box(ax, 3.2, 5.3, 2.2, 0.6, 'Codex CLI\n(1,651 commits)', 'white', 8)
draw_box(ax, 5.6, 5.3, 1.8, 0.6, 'Pass\nSelection', 'white', 8)
draw_box(ax, 7.6, 5.3, 1.7, 0.6, 'Policy\nAdaptation', 'white', 8)

# === Layer 2: Framework ===
draw_box(ax, 0.5, 3.4, 9, 1.6, '', FRAMEWORK_COLOR)
ax.text(5, 4.75, 'Auto-Research Framework', ha='center', fontsize=11, fontweight='bold')

draw_box(ax, 0.8, 4.0, 1.8, 0.6, 'Docker\nPackaging', 'white', 8)
draw_box(ax, 2.8, 4.0, 1.8, 0.6, 'KVM/AWS\nDeploy', 'white', 8)
draw_box(ax, 4.8, 4.0, 2.0, 0.6, 'Workload\nOrchestration', 'white', 8)
draw_box(ax, 7.0, 4.0, 2.3, 0.6, 'Crash Isolation\n& Recovery', 'white', 8)

draw_box(ax, 0.8, 3.5, 4.0, 0.4, '25 Pass Configs × 6 Apps × 2 Archs', 'white', 7)
draw_box(ax, 5.0, 3.5, 4.3, 0.4, 'Bounded Action Space (A0-A5)', 'white', 7)

# === Layer 3: Execution ===
draw_box(ax, 0.5, 1.6, 9, 1.6, '', EXEC_COLOR)
ax.text(5, 2.95, 'Execution Layer (KVM / AWS)', ha='center', fontsize=11, fontweight='bold')

# Apps
draw_box(ax, 0.7, 2.1, 1.3, 0.6, 'Cilium\nCNI', 'white', 7)
draw_box(ax, 2.1, 2.1, 1.3, 0.6, 'Tetragon\nSecurity', 'white', 7)
draw_box(ax, 3.5, 2.1, 1.3, 0.6, 'Tracee\nRuntime', 'white', 7)
draw_box(ax, 4.9, 2.1, 1.1, 0.6, 'Katran\nLB', 'white', 7)
draw_box(ax, 6.1, 2.1, 1.1, 0.6, 'BCC\nTrace', 'white', 7)
draw_box(ax, 7.3, 2.1, 1.1, 0.6, 'OTEL\nProf', 'white', 7)
draw_box(ax, 8.5, 2.1, 1.0, 0.6, '42\nMicro', 'white', 7)

draw_box(ax, 0.7, 1.7, 8.8, 0.35, '146 BPF Programs  |  ReJIT (kinsn: 305K sites)  |  Workloads: stress-ng, iperf3, hackbench', 'white', 7)

# === Layer 4: Feedback ===
draw_box(ax, 0.5, 0.2, 9, 1.2, '', FEEDBACK_COLOR)
ax.text(5, 1.15, 'Structured Feedback', ha='center', fontsize=11, fontweight='bold')

draw_box(ax, 0.7, 0.35, 2.0, 0.6, 'Verifier Logs\n(reject reason)', 'white', 7)
draw_box(ax, 2.9, 0.35, 2.0, 0.6, 'JIT Output\n(bytes_jited)', 'white', 7)
draw_box(ax, 5.1, 0.35, 2.2, 0.6, 'Runtime Counters\n(run_cnt, ns)', 'white', 7)
draw_box(ax, 7.5, 0.35, 2.0, 0.6, 'Per-Program\nRatio', 'white', 7)

# === Arrows ===
# Agent -> Framework
draw_arrow(ax, (5, 5.2), (5, 5.0), style='->')
# Framework -> Execution
draw_arrow(ax, (5, 3.4), (5, 3.2), style='->')
# Execution -> Feedback
draw_arrow(ax, (5, 1.6), (5, 1.4), style='->')
# Feedback -> Agent (loop back)
ax.annotate('', xy=(0.3, 5.6), xytext=(0.3, 0.8),
            arrowprops=dict(arrowstyle='->', color='#666666', lw=2,
                           connectionstyle='arc3,rad=0.3'))
ax.text(0.1, 3.2, 'Loop', rotation=90, ha='center', va='center', fontsize=9, color='#666666')

# === Stats annotation ===
stats_text = "2,874 sessions\n1,651 agent commits\n515 sessions in 4 days"
ax.text(9.8, 5.6, stats_text, ha='left', va='top', fontsize=8,
        bbox=dict(boxstyle='round', facecolor='lightyellow', edgecolor='gray', alpha=0.9))

# Formatting
ax.set_xlim(-0.2, 11)
ax.set_ylim(-0.1, 6.3)
ax.set_aspect('equal')
ax.axis('off')

plt.tight_layout()
plt.savefig('/home/yunwei37/workspace/bpf-benchmark/docs/ebpf27-bpfoptbench/architecture.pdf',
            bbox_inches='tight', dpi=300)
plt.savefig('/home/yunwei37/workspace/bpf-benchmark/docs/ebpf27-bpfoptbench/architecture.png',
            bbox_inches='tight', dpi=300)
print("Saved architecture.pdf and architecture.png")
