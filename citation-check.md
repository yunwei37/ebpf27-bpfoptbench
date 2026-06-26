# Citation Verification Report

Generated: 2026-06-26

## Summary

Verified 19 citations from reference.bib. Found 5 issues requiring attention.

## Issues Found

### 1. actplane2026 (arXiv:2606.25189) - AUTHOR MISMATCH

**Status:** NEEDS FIX

| Field | Bib Entry | Actual (arXiv) |
|-------|-----------|----------------|
| Title | ActPlane: Programmable OS-Level Policy Enforcement for Agent Harnesses | ActPlane: Programmable OS-Level Policy Enforcement for Agent Harnesses |
| Authors | Yusheng Zheng, Yiwei Chen, Zhengjie Ji, Dan Williams, Andrew Quinn | Yusheng Zheng, Tianyuan Wu, Quanzhi Fu, Tong Yu, Wenan Mao, Wei Wang, Dan Williams, Andi Quinn |
| Year | 2026 | 2026 |

**Issues:**
- Author list completely different (only Yusheng Zheng, Dan Williams overlap)
- "Andrew Quinn" should be "Andi Quinn"

### 2. compilot2025 (arXiv:2511.00592) - TITLE MISMATCH

**Status:** NEEDS FIX

| Field | Bib Entry | Actual (arXiv) |
|-------|-----------|----------------|
| Title | ComPilot: Agentic Auto-Scheduling via LLM-Guided Loop Optimization | Agentic Auto-Scheduling: An Experimental Study of LLM-Guided Loop Optimization |
| Authors | Massinissa Merouani, Islem Kara Bernou, Riyadh Baghdadi | Massinissa Merouani, Islem Kara Bernou, Riyadh Baghdadi |
| Year | 2025 | 2025 |

**Issues:**
- Title does not contain "ComPilot" - this appears to be a fabricated/assumed name
- Actual title is "Agentic Auto-Scheduling: An Experimental Study of LLM-Guided Loop Optimization"

### 3. awarecompiler2025 (arXiv:2510.11759) - AUTHORS NEED UPDATE

**Status:** NEEDS FIX

| Field | Bib Entry | Actual (arXiv) |
|-------|-----------|----------------|
| Title | AwareCompiler: Agentic Context-Aware Compiler Optimization via a Synergistic Knowledge-Data Driven Framework | AwareCompiler: Agentic Context-Aware Compiler Optimization via a Synergistic Knowledge-Data Driven Framework |
| Authors | Anonymous | Hongyu Lin, Haolin Pan, Haoran Luo, Yuchen Li, Kaichun Yao, Libo Zhang, Mingjie Xing, Yanjun Wu |
| Year | 2025 | 2025 |

**Issues:**
- Authors listed as "Anonymous" but paper now has real author names

### 4. llmagentsesurvey2025 (arXiv:2510.09721) - AUTHOR NAME TYPO

**Status:** NEEDS FIX

| Field | Bib Entry | Actual (arXiv) |
|-------|-----------|----------------|
| Title | A Comprehensive Survey on Benchmarks and Solutions in Software Engineering of LLM-Empowered Agentic System | A Comprehensive Survey on Benchmarks and Solutions in Software Engineering of LLM-Empowered Agentic System |
| Authors | Guo, Jialin and others | Jiale Guo, Suizhi Huang, Mei Li, Dong Huang, Xingsheng Chen, Regina Zhang, Zhijiang Guo, Han Yu, Siu-Ming Yiu, Pietro Lio, Kwok-Yan Lam |
| Year | 2025 | 2025 |

**Issues:**
- First author name is "Jiale Guo", not "Jialin Guo"

### 5. claudecode2025 - URL REDIRECT (Minor)

**Status:** WORKS BUT URL CHANGED

| Field | Bib Entry | Current |
|-------|-----------|---------|
| URL | https://docs.anthropic.com/en/docs/claude-code | Redirects to https://code.claude.com/docs |
| Title | Claude Code: An Agentic Coding Tool | Claude Code (confirmed) |
| Author | Anthropic | Anthropic (confirmed) |
| Year | 2025 | 2025 |

**Note:** The old URL works via redirect (HTTP 301), but consider updating to the canonical URL.

## Verified OK

### arXiv Papers

| Citation | arXiv ID | Title | Authors | Year | Status |
|----------|----------|-------|---------|------|--------|
| kops2026 | 2606.24213 | Kops: Safely Extending the eBPF Compilation Pipeline with Native Operations | Yusheng Zheng et al. | 2026 | OK |
| gso2025 | 2505.23671 | GSO: Challenging Software Optimization Tasks for Evaluating SWE-Agents | Manish Shetty et al. | 2025 | OK |
| kernelbench2025 | 2502.10517 | KernelBench: Can LLMs Write Efficient GPU Kernels? | Anne Ouyang et al. | 2025 | OK |
| swebench2023 | 2310.06770 | SWE-bench: Can Language Models Resolve Real-World GitHub Issues? | Carlos E. Jimenez et al. | 2023 | OK |

### DOI Papers (via Crossref API)

| Citation | DOI | Title | Authors | Year | Status |
|----------|-----|-------|---------|------|--------|
| mao2024merlin | 10.1145/3620666.3651387 | Merlin: Multi-tier Optimization of eBPF Code for Performance and Compactness | Jinsong Mao, Hailun Ding, Juan Zhai, Shiqing Ma | 2024 | OK |
| xu2021synthesizing | 10.1145/3452296.3472929 | Synthesizing safe and efficient kernel extensions for packet processing | Qiongwen Xu, Michael D. Wong, Tanvi Wagle, Srinivas Narayana, Anirudh Sivaraman | 2021 | OK |

### OpenReview Papers

| Citation | ID | Title | Venue | Year | Status |
|----------|----|-------|-------|------|--------|
| pie2024 | ix7rLVHXyY | Learning Performance-Improving Code Edits | ICLR 2024 | 2024 | OK |

### Tool/Project Websites

| Citation | URL | Description | Status |
|----------|-----|-------------|--------|
| pktgen | kernel.org/doc/html/latest/networking/pktgen.html | Linux Packet Generator documentation | OK |
| stressng | github.com/ColinIanKing/stress-ng | stress-ng by Colin Ian King | OK |
| cilium | cilium.io | eBPF-based Networking, Security, and Observability | OK |
| tetragon | tetragon.io | eBPF-based Security Observability and Runtime Enforcement | OK |
| falco | falco.org | Cloud Native Runtime Security | OK |
| bcc | github.com/iovisor/bcc | BPF Compiler Collection - IO Visor Project | OK |

## Unable to Verify

| Citation | URL | Reason |
|----------|-----|--------|
| openaicodex2025 | openai.com/index/introducing-codex/ | Cloudflare bot protection (HTTP 403) |

**Note:** The OpenAI Codex URL returns HTTP 403 due to Cloudflare protection. Manual browser verification recommended.

## Recommended Fixes

### Fix 1: actplane2026

```bibtex
@misc{actplane2026,
  title = {{ActPlane}: Programmable {OS}-Level Policy Enforcement for Agent Harnesses},
  author = {Zheng, Yusheng and Wu, Tianyuan and Fu, Quanzhi and Yu, Tong and Mao, Wenan and Wang, Wei and Williams, Dan and Quinn, Andi},
  year = {2026},
  howpublished = {arXiv preprint arXiv:2606.25189},
  url = {https://arxiv.org/abs/2606.25189}
}
```

### Fix 2: compilot2025

```bibtex
@misc{compilot2025,
  title = {Agentic Auto-Scheduling: An Experimental Study of {LLM}-Guided Loop Optimization},
  author = {Merouani, Massinissa and Bernou, Islem Kara and Baghdadi, Riyadh},
  year = {2025},
  howpublished = {arXiv preprint arXiv:2511.00592},
  url = {https://arxiv.org/abs/2511.00592}
}
```

**Note:** If you need to cite this as "ComPilot", verify with the authors whether this is an alternate name for the system.

### Fix 3: awarecompiler2025

```bibtex
@misc{awarecompiler2025,
  title = {{AwareCompiler}: Agentic Context-Aware Compiler Optimization via a Synergistic Knowledge-Data Driven Framework},
  author = {Lin, Hongyu and Pan, Haolin and Luo, Haoran and Li, Yuchen and Yao, Kaichun and Zhang, Libo and Xing, Mingjie and Wu, Yanjun},
  year = {2025},
  howpublished = {arXiv preprint arXiv:2510.11759},
  url = {https://arxiv.org/abs/2510.11759}
}
```

### Fix 4: llmagentsesurvey2025

```bibtex
@misc{llmagentsesurvey2025,
  title = {A Comprehensive Survey on Benchmarks and Solutions in Software Engineering of {LLM}-Empowered Agentic System},
  author = {Guo, Jiale and Huang, Suizhi and Li, Mei and Huang, Dong and Chen, Xingsheng and Zhang, Regina and Guo, Zhijiang and Yu, Han and Yiu, Siu-Ming and Lio, Pietro and Lam, Kwok-Yan},
  year = {2025},
  howpublished = {arXiv preprint arXiv:2510.09721},
  url = {https://arxiv.org/abs/2510.09721}
}
```

### Fix 5: claudecode2025 (Optional)

```bibtex
@misc{claudecode2025,
  title = {Claude Code: An Agentic Coding Tool},
  author = {{Anthropic}},
  year = {2025},
  howpublished = {\url{https://code.claude.com/docs}},
  note = {Accessed: 2026-06-26}
}
```
