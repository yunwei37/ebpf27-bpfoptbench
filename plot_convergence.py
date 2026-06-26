#!/usr/bin/env python3
"""
Plot exploration convergence curves for BPFOptBench paper.
Shows how performance improves over exploration sessions.
"""

import matplotlib.pyplot as plt
import numpy as np

# Set up style for paper
plt.rcParams.update({
    'font.size': 9,
    'font.family': 'serif',
    'axes.labelsize': 9,
    'axes.titlesize': 9,
    'xtick.labelsize': 8,
    'ytick.labelsize': 8,
    'legend.fontsize': 8,
    'figure.figsize': (3.5, 2.5),  # Single column width for 2-column paper
    'axes.grid': True,
    'grid.alpha': 0.3,
    'lines.linewidth': 1.5,
    'lines.markersize': 5,
})

# Data extracted from docs/source-opt/README.md
# Format: list of (attempt_number, improvement_percent)
# All values are "vs baseline" from the README

# Cilium: Clear convergence story with a breakthrough at attempt 5
cilium_data = [
    (0, 0.0),      # baseline
    (1, 1.04),     # local-delivery-redirect-peer
    (2, 0.40),     # from-container-error-unlikely
    (3, 1.45),     # cil-lxc-policy-error-unlikely
    (4, 1.48),     # cil-to-container-error-unlikely
    (5, 12.37),    # tail-ipv4-to-endpoint-revalidate-unlikely (BREAKTHROUGH)
    # Phase2 attempts didn't improve further
    (6, 8.69),     # phase2 stacked (regression from best)
    (7, 8.17),     # phase2 policy-ok-fastpath
]

# Tetragon: Early negative, then breakthrough at attempt 3
tetragon_data = [
    (0, 0.0),      # baseline
    (1, -0.57),    # sparse-selector-active-clear
    (2, -0.80),    # filter-args-active-fastpath
    (3, 8.15),     # lazy-ns-cap-selector-state (BREAKTHROUGH)
    (4, 7.69),     # lazy-ns-cap-conditional-cap-sparse
    (5, 8.61),     # lazy-ns-cap-skip-empty-namespace-loop (BEST)
]

# Katran: Gradual improvement in phase2
katran_data = [
    (0, 0.0),      # baseline
    (1, -0.30),    # udp-parse-first
    (2, -0.51),    # icmp-protocol-refresh
    (3, -0.26),    # calc-offset-fastpath
    (4, -0.03),    # quic-connid-no-null-check
    (5, -1.80),    # stable-rt-header-early-return
    # Phase2 - shift to network flow optimizations
    (6, 7.97),     # phase2 udp-flow-migration-require-dst
    (7, 7.42),     # phase2 lru-miss-proto-compare
    (8, 9.40),     # phase2 cache-vip-metadata (BEST)
]

# BCC: Steady incremental improvement
bcc_data = [
    (0, 0.0),      # baseline
    (1, -0.05),    # opensnoop-reuse-pidtgid
    (2, -0.88),    # tcpconnect-lazy-uid-filter
    (3, -0.81),    # tcplife-cache-newstate
    (4, 0.15),     # syscount-interrupt-fast-return
    (5, -0.75),    # runqlat-skip-idle-tgid-read
    # Phase2 - systematic improvements
    (6, 1.09),     # phase2 capable-fexit-syscount-base
    (7, 1.02),     # phase2 tcpconnect-fexit-stack
    (8, 1.99),     # phase2 syscount-raw-tracepoint
    (9, 0.69),     # phase2 syscount-latency-specialized-exit
    (10, 2.70),    # phase2 raw-syscount-tcpconnect-fexit (BEST)
]


def extract_best_so_far(data):
    """Convert raw data to cumulative best performance."""
    attempts = []
    improvements = []
    best_so_far = 0.0

    for attempt, imp in data:
        attempts.append(attempt)
        best_so_far = max(best_so_far, imp)
        improvements.append(best_so_far)

    return attempts, improvements


# Create figure
fig, ax = plt.subplots()

# Plot each app's convergence curve (best-so-far)
colors = {
    'Cilium': '#1f77b4',
    'Tetragon': '#ff7f0e',
    'Katran': '#2ca02c',
    'BCC': '#d62728',
}

markers = {
    'Cilium': 'o',
    'Tetragon': 's',
    'Katran': '^',
    'BCC': 'D',
}

for name, data in [('Cilium', cilium_data), ('Tetragon', tetragon_data),
                    ('Katran', katran_data), ('BCC', bcc_data)]:
    attempts, improvements = extract_best_so_far(data)
    ax.plot(attempts, improvements,
            label=name,
            color=colors[name],
            marker=markers[name],
            markevery=1,
            alpha=0.9)

# Add horizontal line at 0%
ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.8, alpha=0.5)

# Add phase boundary annotation
ax.axvline(x=5.5, color='gray', linestyle=':', linewidth=0.8, alpha=0.7)

# Labels and legend
ax.set_xlabel('Exploration Attempt')
ax.set_ylabel('Best Improvement (%)')
ax.set_xlim(-0.5, 10.5)
ax.set_ylim(-2, 14)

# Position legend in center-right to avoid main data
ax.legend(loc='center right', framealpha=0.9, bbox_to_anchor=(1.0, 0.35))

# Tight layout for paper
plt.tight_layout()

# Save
plt.savefig('/home/yunwei37/workspace/bpf-benchmark/docs/ebpf27-bpfoptbench/convergence.pdf',
            dpi=300, bbox_inches='tight')
plt.savefig('/home/yunwei37/workspace/bpf-benchmark/docs/ebpf27-bpfoptbench/convergence.png',
            dpi=300, bbox_inches='tight')

print("Saved: convergence.pdf and convergence.png")
print("\nKey insights from the curves:")
print("- Cilium: Breakthrough at attempt 5 (+12.37%), Phase 2 couldn't improve further")
print("- Tetragon: Breakthrough at attempt 3 (+8.15%), refined to +8.61%")
print("- Katran: Phase 1 was flat/negative, Phase 2 enabled +9.40%")
print("- BCC: Steady incremental gains, final +2.70%")
