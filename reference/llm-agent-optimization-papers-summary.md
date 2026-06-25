# LLM Agent + Code Optimization Papers Summary

This document summarizes papers on LLM-based code optimization that should be cited in the BPFOptBench paper, with concrete performance numbers and key characteristics.

---

## 1. GPU Kernel Optimization

### KernelBench (Ouyang et al., 2025)
- **Venue**: arXiv 2502.10517
- **Use case**: Evaluating LLMs' ability to generate efficient GPU kernels for PyTorch workloads
- **Benchmark**: 250 PyTorch workloads across 4 levels (single ops, fusion, models, HuggingFace)
- **Performance results**:
  - DeepSeek R1: 12% success at Level 1 (one-shot), 43% with iterative refinement (10 turns)
  - Frontier models match PyTorch baseline in <20% of cases
  - STARK multi-agent: 100% success at Level 1 with up to 3.0x speedup
- **Feedback mechanism**: Execution feedback (correctness + speedup measurement)
- **Key metric**: fast_p (fraction of correct kernels achieving speedup > p over PyTorch eager)
- **Already in reference.bib**: Yes (kernelbench2025)

### STARK (Multi-Agent GPU Kernel Optimization, 2025)
- **Venue**: arXiv 2510.16996
- **Use case**: Multi-agent collaborative GPU kernel optimization
- **Performance results**:
  - 100% success rate on KernelBench Level 1
  - Up to 3.0x speedup over Torch Eager baselines
  - 10x speedup over baseline single-agent approaches
- **Feedback mechanism**: Plan/code/debug agents with strategic tree search memory
- **Key insight**: Multi-agent workflow with grounded instructions anchored to code spans
- **To add to reference.bib**: Yes

### GPU Kernel Scientist (Andrews & Witteveen, 2025)
- **Venue**: arXiv (referenced in your docs)
- **Use case**: LLM-driven iterative optimization for AMD MI300 (limited documentation)
- **Performance results**:
  - ~450us kernel time (LLM-only) vs ~850us PyTorch reference
  - vs ~105us human 1st place (with hardware access)
- **Feedback mechanism**: Autonomous experiment design + hypothesis generation
- **Key insight**: LLM bootstraps from limited documentation via knowledge transfer from CUDA
- **To add to reference.bib**: Yes

---

## 2. Loop/Compiler Optimization

### ComPilot (Merouani et al., 2025)
- **Venue**: PACT 2025, arXiv 2511.00592
- **Use case**: LLM-guided loop optimization via closed-loop compiler interaction
- **Performance results**:
  - **2.66x** geomean speedup (single run) over original code
  - **3.54x** geomean speedup (best-of-5 runs)
  - **2.94x** over Pluto polyhedral optimizer (best-of-5)
  - On smaller inputs (MINI): **16.35x** over Pluto
- **Feedback mechanism**: Closed-loop with Tiramisu compiler (legality check, speedup measurement)
- **Key insight**: General-purpose LLMs can guide optimization without task-specific fine-tuning
- **Already in reference.bib**: Yes (compilot2025)

### AwareCompiler (2025)
- **Venue**: arXiv 2510.11759
- **Use case**: Agentic context-aware compiler optimization
- **Feedback mechanism**: Knowledge-data driven synergistic framework
- **Key insight**: Combines domain knowledge with runtime data for optimization decisions
- **To add to reference.bib**: Yes

---

## 3. Software Engineering Benchmarks

### SWE-bench (Jimenez et al., 2023)
- **Venue**: arXiv 2310.06770, ICLR 2024
- **Use case**: Evaluating LLMs on resolving real-world GitHub issues
- **Benchmark**: Repository + issue description -> patch generation
- **Performance results**:
  - Claude 3.7 Sonnet: **43%** on SWE-bench Multilingual, **63%** on SWE-bench Verified
  - SWE-bench Verified: 500 engineer-confirmed solvable problems
- **Feedback mechanism**: Test-based validation (pass/fail)
- **Key insight**: Real-world software engineering tasks require localization + multi-step reasoning
- **Already in reference.bib**: Yes (swebench2023)

### GSO: Global Software Optimization (Shetty et al., 2025)
- **Venue**: NeurIPS 2025, arXiv 2505.23671
- **Use case**: Challenging software optimization tasks for SWE-Agents
- **Benchmark**: 102 optimization tasks across 10 codebases (NumPy, Pandas, Pillow, Llama-CPP)
- **Performance results**:
  - Leading SWE-Agents achieve **<5% success rate**
  - GPT-4O: **0%** at K=1
  - Gold patches: 4-15x more lines edited than previous benchmarks
- **Feedback mechanism**: Speedup measurement + hack detector (penalizes deceptive optimizations)
- **Key insight**: Low-level languages (C/C++/Cython) cause 70% of failures (drops to 4% success)
- **Already in reference.bib**: Yes (gso2025)

### tau-bench (Yao et al., 2024)
- **Venue**: arXiv 2406.12045
- **Use case**: Tool-Agent-User interaction benchmark
- **Key insight**: Real-world domains require multi-turn tool use
- **Already in reference.bib**: Yes (taubench2024)

---

## 4. Competitive Programming / Algorithm Optimization

### PIE: Performance-Improving Edits (Shypula et al., ICLR 2024)
- **Venue**: ICLR 2024 Spotlight
- **Use case**: Adapting LLMs to perform high-level algorithmic optimizations on C++ programs
- **Dataset**: 77K C++ program pairs with execution time annotations (gem5 simulator)
- **Performance results**:
  - GPT-3.5 + self-play fine-tuning: **6.86x** average speedup (best-of-8)
  - CodeLLama 13B fine-tuned: **5.65x** average speedup
  - Human reference: 3.66x average speedup
  - Best model speedup: **9.64x** (vs 9.56x best human)
  - Optimizes **87.63%** of test set by at least 10%
- **Feedback mechanism**: Execution time measurement on gem5 simulator (deterministic)
- **Key insight**: Algorithmic transformations (34%), data structure mods (21%), I/O optimizations (14%)
- **To add to reference.bib**: Yes

### AlphaCode (Li et al., Science 2022)
- **Venue**: Science, arXiv 2203.07814
- **Use case**: Competition-level code generation for competitive programming
- **Performance results**:
  - Ranked within **top 54%** of participants on Codeforces
  - First AI to achieve competitive-level performance
  - Generates millions of candidates, filters to 10 submissions
- **Feedback mechanism**: Test case validation + clustering for diversity
- **Key insight**: Scale (generate millions) + filter (cluster + validate) paradigm
- **To add to reference.bib**: Yes

### CodeContests (2022)
- **Venue**: arXiv 2203.07814 (same as AlphaCode)
- **Use case**: Benchmark dataset for competitive programming
- **Benchmark**: 10K problems from Codeforces with extensive test cases
- **Key feature**: Rigorous test case quality (reduced false positive rate from 62% to 4%)
- **Already implicitly covered by AlphaCode citation**

---

## 5. eBPF + LLM

### Kgent (Zheng et al., eBPF '24)
- **Venue**: ACM SIGCOMM 2024 Workshop on eBPF
- **Use case**: LLM agent for generating eBPF kernel extensions from natural language
- **Performance results**:
  - **2.67x** improvement over GPT-4 in producing correct eBPF programs
  - High accuracy rate with minimal false positives
- **Feedback mechanism**: Program comprehension + symbolic execution + verifier feedback loops
- **Key insight**: Combines LLM with symbolic execution for eBPF-specific constraints
- **Already in reference.bib**: Yes (zheng2024kgent)

### SimpleBPF (Gao et al., eBPF '25)
- **Venue**: eBPF '25 Workshop
- **Use case**: Offloading tedious task of writing eBPF programs
- **Components**: Concise DSL + LLM generator + semantic checker + LLM optimizer
- **Feedback mechanism**: Semantic checker + BPF verifier + LLM-based optimizer
- **Key insight**: DSL constrains generation space; post-generation optimization
- **Already in reference.bib**: Yes (simplebpf2025)

---

## 6. Papers to Add to reference.bib

### High Priority (directly relevant to agent-based optimization)

```bibtex
@misc{stark2025,
  title = {{STARK}: Strategic Team of Agents for Refining Kernels},
  author = {Anonymous},
  year = {2025},
  howpublished = {arXiv preprint arXiv:2510.16996},
  url = {https://arxiv.org/abs/2510.16996}
}

@misc{pie2024,
  title = {Learning Performance-Improving Code Edits},
  author = {Shypula, Alexander and Madaan, Aman and Zeng, Yimeng and Alon, Uri and Gardner, Jacob and Hashemi, Milad and Neubig, Graham and Ranganathan, Parthasarathy and Bastani, Osbert and Yazdanbakhsh, Amir},
  year = {2024},
  booktitle = {International Conference on Learning Representations (ICLR)},
  url = {https://openreview.net/forum?id=ix7rLVHXyY}
}

@article{alphacode2022,
  title = {Competition-Level Code Generation with {AlphaCode}},
  author = {Li, Yujia and Choi, David and Chung, Junyoung and Kushman, Nate and Schrittwieser, Julian and Leblond, R{\'e}mi and Eccles, Tom and Keeling, James and Gimeno, Felix and Dal Lago, Agustin and others},
  journal = {Science},
  volume = {378},
  number = {6624},
  pages = {1092--1097},
  year = {2022},
  publisher = {American Association for the Advancement of Science},
  doi = {10.1126/science.abq1158}
}

@misc{gpukernelscientist2025,
  title = {{GPU} Kernel Scientist: Iterative {LLM}-Driven Optimization for {AMD} {MI300}},
  author = {Andrews, David and Witteveen, Alwin},
  year = {2025},
  howpublished = {arXiv preprint},
  url = {https://arxiv.org/abs/2505.xxxxx}
}

@misc{awarecompiler2025,
  title = {{AwareCompiler}: Agentic Context-Aware Compiler Optimization via a Synergistic Knowledge-Data Driven Framework},
  author = {Anonymous},
  year = {2025},
  howpublished = {arXiv preprint arXiv:2510.11759},
  url = {https://arxiv.org/abs/2510.11759}
}
```

### Medium Priority (survey/context papers)

```bibtex
@misc{llmagentsesurvey2025,
  title = {A Comprehensive Survey on Benchmarks and Solutions in Software Engineering of {LLM}-Empowered Agentic System},
  author = {Guo, Jialin and others},
  year = {2025},
  howpublished = {arXiv preprint arXiv:2510.09721},
  url = {https://arxiv.org/abs/2510.09721}
}

@misc{agenticcodeopt2026,
  title = {Agentic Code Optimization via Compiler-{LLM} Cooperation},
  author = {Anonymous},
  year = {2026},
  howpublished = {arXiv preprint arXiv:2604.04238},
  url = {https://arxiv.org/abs/2604.04238}
}
```

---

## Summary Table

| Paper | Domain | Best Performance | Feedback Type |
|-------|--------|-----------------|---------------|
| PIE (ICLR '24) | C++ algorithms | 6.86x speedup | Execution time (gem5) |
| KernelBench '25 | GPU kernels | <20% match baseline | Execution + correctness |
| STARK '25 | GPU kernels | 3.0x speedup, 100% L1 | Multi-agent + tree search |
| ComPilot (PACT '25) | Loop optimization | 2.66x (3.54x best-of-5) | Compiler legality + timing |
| GSO (NeurIPS '25) | General software | <5% success | Speedup + hack detection |
| SWE-bench '23 | GitHub issues | 43-63% resolve | Test pass/fail |
| AlphaCode '22 | Competitive prog | Top 54% ranking | Test validation |
| Kgent (eBPF '24) | eBPF generation | 2.67x over GPT-4 | Symbolic exec + verifier |
| SimpleBPF (eBPF '25) | eBPF generation | N/A | DSL + semantic check |

---

## Key Themes for BPFOptBench Positioning

1. **Feedback-guided optimization loop**: All successful systems use closed-loop feedback (ComPilot, KernelBench, PIE). BPFOptBench provides this with verifier logs + runtime counters.

2. **Domain-specific constraints**: eBPF verifier is analogous to compiler legality checks (ComPilot) and correctness oracles (PIE). The verifier log provides rich semantic feedback.

3. **Multi-pass transformation**: Like PIE's algorithmic vs. data structure vs. I/O categories, BPFOptBench decomposes optimizations into orthogonal passes.

4. **Benchmark gap**: GSO shows current agents fail at <5% on software optimization. BPFOptBench fills a gap in kernel/systems software optimization benchmarks.

5. **eBPF-specific value**: Unlike SimpleBPF/Kgent (generation), BPFOptBench focuses on optimization of existing production programs - a distinct and underexplored task.
