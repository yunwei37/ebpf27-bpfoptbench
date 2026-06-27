#!/usr/bin/env python3
"""Generate multi-layer optimization results figure."""

import matplotlib.pyplot as plt
import numpy as np

# App colors
app_colors = {
    'Cilium': '#4e79a7',
    'Katran': '#f28e2b',
    'Tetragon': '#59a14f',
    'OTEL': '#e15759',
    'Tracee': '#76b7b2',
    'BCC': '#edc949',
}

# Best few apps per layer (Phase 3 peaks)
source_data = [('Cilium', 15), ('Katran', 12), ('Tetragon', 12), ('BCC', 12)]
llvm_data = [('OTEL', 34), ('Katran', 12)]
kernel_data = [('Tetragon', 17), ('Cilium', 15), ('Tracee', 7), ('BCC', 4)]

fig, ax = plt.subplots(figsize=(6, 2.33))

width = 0.28
used_apps = set()

# Source layer (position 0)
x_base = 0
for i, (app, val) in enumerate(source_data):
    label = app if app not in used_apps else ''
    ax.bar(x_base + i * width, val, width * 0.9, color=app_colors[app], label=label)
    ax.text(x_base + i * width, val + 1.5, f'{val}%', ha='center', fontsize=10, fontweight='bold')
    used_apps.add(app)

# LLVM layer (position 1.2)
x_base = 1.2
for i, (app, val) in enumerate(llvm_data):
    label = app if app not in used_apps else ''
    ax.bar(x_base + i * width, val, width * 0.9, color=app_colors[app], label=label)
    ax.text(x_base + i * width, val + 1.5, f'{val}%', ha='center', fontsize=10, fontweight='bold')
    used_apps.add(app)

# Kernel JIT layer (position 2.4)
x_base = 2.4
for i, (app, val) in enumerate(kernel_data):
    label = app if app not in used_apps else ''
    ax.bar(x_base + i * width, val, width * 0.9, color=app_colors[app], label=label)
    ax.text(x_base + i * width, val + 1.5, f'{val}%', ha='center', fontsize=10, fontweight='bold')
    used_apps.add(app)

ax.set_ylabel('Improvement (%)', fontsize=14)
ax.set_xticks([0.28, 1.34, 2.68])
ax.set_xticklabels(['Source', 'LLVM', 'Kernel'], fontsize=14)
ax.tick_params(axis='y', labelsize=13)
ax.set_ylim(0, 48)
ax.legend(loc='upper right', fontsize=12, ncol=2)

plt.tight_layout()
plt.savefig('layers.pdf', bbox_inches='tight', dpi=300)
plt.savefig('layers.png', bbox_inches='tight', dpi=150)
print('Saved layers.pdf and layers.png')
