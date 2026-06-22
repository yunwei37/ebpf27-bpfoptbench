# BPFOptBench Paper Draft

This repository is the paper workspace for:

> BPFOptBench: Benchmarking Agentic Optimization of Existing eBPF Programs

The current draft frames the work as a benchmark/tooling paper, not as a claim that the current optimizer already wins across the corpus. The first track should evaluate agents that tune existing eBPF programs through bytecode/ReJIT/kinsn-backed actions under real verifier, JIT, application, workload, and performance feedback.

Key files:

- `main.tex`: ACM paper entry point.
- `sections/`: active paper draft.
- `research-plan.md`: claim ledger and experiment plan.
- `reference.bib`: current bibliography, inherited from the initial template and partially reused.

Current scope:

- Primary: agent policy over existing optimization actions, especially suite-wide, per-app, and per-program pass selection.
- Supported first-track backends: bytecode-only, live ReJIT, optional kinsn.
- Future adapters: source-level rewrites, LLVM BPF backend changes, pre-load object rewrites beyond the existing path.
- Benchmark assets still needed: frozen task manifests, hidden evaluator, protected workloads, private/rotating holdout tasks, fresh-VM replay, and expert-audited reference solutions.

Important claim discipline:

- Historical data supports the benchmark motivation and difficulty claim.
- Agent success claims require new controlled runs.
- Verifier acceptance is not enough; the oracle must include app lifecycle, workload correctness, and performance beyond noise.
- The existing `bpf-benchmark` runner is an execution substrate; BPFOptBench must add task datasets and evaluator isolation to be a real agent benchmark.
