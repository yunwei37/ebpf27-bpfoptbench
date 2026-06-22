# Research Plan: BPFOptBench

Last updated: 2026-06-22
Stage: experiment design

## Thesis

BPFOptBench evaluates whether agents can tune existing eBPF programs under real verifier, JIT, and workload feedback by exposing eBPF optimization as a closed-loop decision problem over multiple transformation layers.

## Paper Type

- Type: benchmark/tooling plus measurement study.
- Target: eBPF workshop first.
- Implementation status: bytecode/ReJIT/kinsn infrastructure exists in the parent project; source and LLVM adapters are future work.
- Main risk: historical data proves the task is hard, but does not yet prove that an agent improves the corpus.
- Scope discipline: BPFOptBench should be an optimization-focused benchmark, not a broad BPF-AgentBench unless we also build a large frozen task dataset and hidden grader.

## Optimization Space

| Layer | What the agent changes | First-paper role |
|---|---|---|
| Source | C/Rust eBPF source, app-side generator logic, map layout, explicit checks | future adapter |
| LLVM backend | BPF target cost model, IR/MIR passes, peepholes, branch analysis | future adapter |
| Pre-load bytecode | BPF object or bytecode before kernel load | supported where adapter exists |
| Live bytecode/ReJIT | pass list, pass order, per-app/per-program policy, per-site gating | primary |
| Kernel/JIT/kinsn | native idioms exposed through kinsn or JIT capability choices | optional backend |

## Claim Ledger

| ID | Claim | Evidence needed | Status |
|---|---|---|---|
| C1 | BPFOptBench defines a backend-agnostic task interface for eBPF optimization agents. | task schema, feedback schema, oracle definition, traces | planned |
| C2 | eBPF optimization is noisy and policy-sensitive, so static pass policies are insufficient. | existing noise floors, pass-signal audit, policy comparison | partially supported |
| C3 | The oracle must compose verifier, app, workload, and performance outcomes. | failure taxonomy from controlled runs | planned |
| C4 | Agents can be compared fairly under equal budgets. | scoreboard over no-op, static, random, human, LLM variants | unsupported until run |
| C5 | Structured feedback improves decisions over raw logs. | prompt/feedback ablation | unsupported until run |
| C6 | The benchmark is not tied to kinsn. | at least one bytecode-only task track | planned |

## Main Experiment Blocks

1. Historical difficulty study: summarize noop floors, pass instability, applied-count mismatch, and policy-tuning results.
2. Benchmark schema validation: create frozen task manifests and replayable traces.
3. Oracle taxonomy: classify failures as verifier rejection, app failure, workload failure, no-signal, regression, or noise chasing.
4. Agent scoreboard: compare no-op, noop-ReJIT, static policy, random/grid, human tuned, raw one-shot LLM, structured one-shot LLM, and closed-loop LLM.
5. Feedback ablation: raw logs versus structured summaries versus closed-loop feedback.
6. Backend ablation: bytecode-only versus kinsn-enabled tracks.
7. Integrity audit: measure attempts to change workloads, reduce run counts, filter failures, bypass app loaders, or modify protected evaluator files.

## Metrics

- Validity rate: accepted by verifier and benchmark policy.
- Workload success rate: app lifecycle and workload checks pass.
- Performance success rate: workload-correct attempts that beat the threshold/noise gate.
- `bpfopt_success_p`: accepted, workload-correct, and faster than baseline by threshold `p`.
- Geomean ratio: post/baseline per-program runtime ratio after the documented run-count filter.
- Regret: gap to the best-known valid action.
- Cost: attempts, wall-clock time, tokens, dollars, and benchmark runs.
- Consistency: repeated-run success and pass-at-k-style stability.
- Integrity failures: protected-path edits, workload mutation, run-budget changes, result fabrication, or fallback behavior.

## Near-Term Run Order

1. Freeze task and trace schema, including protected paths, workload hashes, public checks, hidden checks, and evaluator ownership.
2. Build 15--25 vertical-slice tasks: a small mix of repo/harness tasks, kernel-in-the-loop tasks, and performance-optimization tasks.
3. Recompute current six-app noop/noop-ReJIT floor if historical runs are too stale.
4. Run a small A1 pass-selection smoke test on one or two apps.
5. Run historical-only agent tasks to validate prompts and action parsing.
6. Run live A1/A2 tasks with fixed budgets and fresh-VM replay.
7. Expand to A3 per-program tasks only if the A1/A2 scoreboard has signal.
8. Move toward 30--50 audited tasks for a workshop paper; reserve 80--150 audited tasks plus private holdout for a stronger standalone benchmark claim.

## Claim Discipline

Do not claim that agents optimize eBPF until controlled agent runs beat static and random baselines. The safe current claim is narrower: existing data shows that the optimization problem is noisy, layer-crossing, and not solved by static pass policies, motivating BPFOptBench as a benchmark.

Do not claim that the existing parent repository is already an agent benchmark. It is the execution substrate. The benchmark contribution requires frozen tasks, evaluator isolation, hidden checks, contamination policy, and anti-gaming tests.
