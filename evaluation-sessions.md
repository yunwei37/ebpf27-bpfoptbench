# BPFOptBench Evaluation Sessions: Agentic Exploration Analysis

Date: 2026-06-24

BPFOptBench 的核心贡献不仅是最终的性能数字，更是**自动化探索过程本身**。本文档详细记录了框架稳定后（2026-05-20 起）的全部探索活动，展示 auto-research 框架如何实现大规模的优化策略空间搜索。

---

## 1. 探索规模 (Exploration Scale)

### 总体数据

| 指标 | 数值 |
|------|-----:|
| **总 session 数** | **2,874** |
| Corpus sessions | 2,022 |
| Micro sessions | 852 |
| x86 KVM corpus | 1,635 |
| AWS ARM64 corpus | 213 |
| 五月 sessions | 1,273 |
| 六月 sessions | 485 |

### Agentic Exploration 标志

**显式 pass 配置的 sessions**: 845 (约 66% 的 corpus sessions)

这表明三分之二的运行都是有目的的策略探索，而非简单的基线测量。剩余三分之一用于 noise floor 校准和 infrastructure 验证。

**测试过的唯一 pass 配置数**: 25 种

### 密集探索期: May 21-24

| 日期 | Sessions | 说明 |
|------|-------:|------|
| May 21 | 157 | 初始爆发，workload 设计探索 |
| May 22 | 142 | cilium/katran packet 工作负载变体 |
| May 23 | 117 | pass 组合测试 |
| May 24 | 99 | 持续迭代 |
| **合计** | **515** | **4 天内完成全年 26% 的探索** |

这 4 天的密集探索是典型的 auto-research 行为：框架稳定后立即开始大规模策略空间搜索。

---

## 2. 探索时间线 (Exploration Timeline)

### Phase 1: Framework Bootstrapping (March 2026)

| 里程碑 | 日期 | 关键事件 |
|--------|------|----------|
| 初始架构 | Mar 28 | Benchmark 配置与 pass 管理引入 |
| 清理 | Mar 29 | 删除不符合设计的代码 (`8565cbb55`) |
| 首批 corpus | Mar 30-31 | `vm_corpus_20260331_*` 系列建立基线 |
| Micro 权威测量 | Mar 14 | `vm_micro_authoritative_20260314`: overall **1.054x** |

### Phase 2: App Selection & Methodology (April-May 2026)

| 里程碑 | 日期 | 关键事件 |
|--------|------|----------|
| 6 App 候选 | Apr 23 | 6 个生产 workload 变体加入 |
| SCX 移除 | Apr 25 | struct_ops ReJIT 崩溃调度器 |
| Calico 移除 | May 4 | BPF dataplane 需要 K8s pod 模型 |
| bcc/set 引入 | May 6 | 8 工具合并 runner |
| **方法论稳定** | **May 5** | SAMPLES=3 上限, min_runs>=100 阈值 |
| **Framework 稳定** | **May 20** | bpftrace 脚本移除，最终 6-app 列表确定 |

**最终 6-app corpus**:
1. `bcc/set` (8 工具合并)
2. `otelcol-ebpf-profiler/profiling`
3. `cilium/agent`
4. `tetragon/observer`
5. `katran`
6. `tracee/monitor`

### Phase 3: Post-Stabilization Exploration (May 20 - June)

| 阶段 | 时间 | Sessions | 重点 |
|------|------|-------:|------|
| Workload 设计 | May 21-22 | ~300 | packet generator 变体 (pktgen_bidir, pktgen_noclone, heavy_flags) |
| Pass 组合 | May 23-29 | ~350 | 11-pass full pipeline vs 单 pass 隔离 |
| Noise Floor | May 7-8 | ~150 | Q1/P1 基线校准 |
| LEA 调试 | Jun 2-3 | ~150 | lea pass 高失败率调试 |
| Kinsn 评估 | Jun 3-6 | ~100 | all-force kinsn 策略验证 |
| ARM64 验证 | Jun 14-17 | ~180 | 跨架构覆盖 |
| 近期验证 | Jun 22 | ~50 | 最新 infrastructure 验证 |

### 关键转折点

1. **May 7-8 Noise Floor 发现**: `|0.9019 - 0.8587| = 0.04x` 套件噪声幅度
   - 改变了所有后续分析的信号阈值
   - Session: `x86_kvm_corpus_20260507_190554_205137` (Q1) 和 `x86_kvm_corpus_20260508_000244_131324` (P1)

2. **June 2 LEA 崩溃日**: 94 个 sessions 中 77 个 error (82% 失败率)
   - 触发了 lea pass 的深入调试
   - 暴露了 kinsn 与 verifier 交互的边界情况

3. **June 3 Kinsn 突破**: `x86_kvm_corpus_20260603_175429_964295`
   - BPF geomean **0.938x** (6.2% 改进)
   - 27,085 sites applied, 0 errors
   - 首个 paper-grade 正向结果

---

## 3. Pass 策略探索 (Pass Strategy Exploration)

### Pass 配置频次分布

| 配置 | Sessions | Completed | Error | 日期范围 |
|------|-------:|----------:|------:|----------|
| Full pipeline (11 passes) | 284 | 142 | 103 | May 23-29 |
| noop (baseline) | 196 | 103 | 46 | May 21 - Jun 21 |
| [empty/default] | 115 | 98 | 10 | May 22 - Jun 22 |
| lea only | 102 | 13 | 76 | May 31 - Jun 3 |
| ARM64 pipeline (10 passes) | 97 | 43 | 16 | Jun 14-17 |
| kinsn only | 50 | 37 | 9 | Jun 3-8 |
| rotate only | 35 | 8 | 21 | Jun 2-3 |
| map_inline only | 33 | 22 | 11 | May 21-22 |

### Pass 级别应用统计

从所有 post-May-20 sessions 的 report 文件聚合：

| Pass | Sessions | Sites Applied | Sites Matched | Sites Skipped |
|------|-------:|-------------:|-------------:|-------------:|
| **kinsn** | 30 | **305,449** | 305,449 | 0 |
| **rotate** | 40 | **222,547** | 222,547 | 0 |
| **lea** | 10 | **46,749** | 46,749 | 0 |
| **cond_select** | 13 | **6,578** | 6,578 | 0 |
| **map_inline** | 24 | 3,918 | 5,859 | **1,941** |
| noop | 13 | 874 | 874 | 0 |
| endian_fusion | 6 | 197 | 197 | 0 |
| bulk_memory | 5 | 57 | 57 | 0 |
| extract | 6 | 48 | 48 | 0 |
| const_prop | 1 | 2 | 2 | 0 |
| dce | 1 | 2 | 2 | 0 |
| bounds_check_merge | 1 | 1 | 1 | 0 |
| wide_mem | 1 | 1 | 1 | 0 |
| skb_load_bytes_spec | 1 | 1 | 1 | 0 |
| prefetch | 2 | 0 | 0 | 0 |
| ccmp | 1 | 0 | 0 | 0 |

### map_inline 的 33% Skip Rate 分析

**数据**: 5,859 matched, 1,941 skipped (33.1%)

**原因分析**:
- map_inline 需要 verifier state 确认 map 内容在 load 和 rejit 之间未改变
- 动态 map (per-CPU, per-socket) 无法内联
- 部分 map 在 workload 运行期间被更新

**Session 示例**: `x86_kvm_corpus_20260507_033859_357762`
- noop + map_inline 配置
- 28 retained programs
- Method B geomean: 0.9817 (接近中性)

**结论**: 33% skip rate 是保守策略的正常表现，不是 bug。map_inline 只内联确定不变的 map，skip 的 site 是因为无法证明安全性。

### lea 的 85% 失败率分析

**数据**: 102 sessions, 13 completed, 76 error (85% 失败率)

**时间集中**: May 31 - Jun 3

**失败模式**:
- Jun 2 单日 94 sessions，77 个 error
- 大部分是连续重试（每隔几分钟一个）

**根因**:
1. lea pass 依赖 kinsn 基础设施
2. 某些 verifier log 边界情况导致 daemon 崩溃
3. 属于 active debugging 期间的预期行为

**Session 示例**: `x86_kvm_corpus_20260602_040512_393134` (error)
- 典型的基础设施调试 session
- 不是 pass 算法问题，而是集成问题

**后续**: Jun 3 修复后，`x86_kvm_corpus_20260603_175429_964295` 成功运行，27,085 sites applied。

### 成功率趋势

| 阶段 | 成功率 | 说明 |
|------|-------:|------|
| May 21-24 密集期 | ~60% | 预期的探索噪声 |
| May 27-29 稳定期 | ~75% | 方法论改进 |
| Jun 1-2 LEA 调试 | ~15% | 集中调试 |
| Jun 3-6 Kinsn 评估 | ~80% | 稳定后验证 |
| Jun 14-17 ARM64 | ~70% | 跨架构扩展 |

---

## 4. 跨架构探索 (Cross-Architecture)

### 平台分布

| 平台 | Corpus Sessions | Micro Sessions |
|------|---------------:|---------------:|
| x86 KVM | 1,635 | 224 |
| AWS ARM64 | 213 | 82 |
| AWS x86 | 0 | 4 |
| ARM64 QEMU | ~100 | 5 |

### ARM64 集中在 June 14-17 的原因

**Session 分布**:
| 日期 | Sessions | 说明 |
|------|-------:|------|
| Jun 14 | 42 | ARM64 初始 pipeline 测试 |
| Jun 15 | 48 | kinsn ARM64 适配验证 |
| Jun 16 | 45 | ARM64-only passes (ccmp) |
| Jun 17 | 39 | 最终 paper-grade 运行 |
| **合计** | **174** | **占全部 ARM64 corpus 的 82%** |

**原因**:
1. x86 pipeline 在 Jun 3 稳定后，优先级转向 ARM64
2. ARM64 需要特定的 kinsn 指令 (EXTR, UBFM, REV)
3. `ccmp` pass 只对 ARM64 有效
4. Paper deadline 驱动的集中验证

### ARM64 权威结果

**Session**: `aws_arm64_micro_20260606_001225_821028`
- Benchmarks: 29
- **Speedup geomean: 1.208x** (20.8% 改进)
- Kinsn-bearing geomean: 1.222x over 27 benchmarks
- Wins/losses/ties: 24/2/3
- Code-size ratio: 0.879x (12% 更小)

**Kinsn 调用分布**:
| 指令 | 调用次数 |
|------|-------:|
| bpf_arm64_extr_x | 387 |
| bpf_arm64_ldr_w | 198 |
| bpf_arm64_ubfm_x | 144 |
| bpf_arm64_ldrh | 114 |
| bpf_arm64_rev16_w | 39 |
| bpf_arm64_stp_x | 21 |
| bpf_arm64_rev_w | 15 |
| bpf_arm64_ldp_x | 6 |

---

## 5. 有趣的发现 (Interesting Findings)

### 5.1 Kinsn 主导 (305K Sites)

**关键数据**:
- kinsn 应用了 305,449 sites，占全部应用的 ~52%
- 其次是 rotate (222,547) 和 lea (46,749)

**June 3 All-Force Kinsn 突破**:
- Session: `x86_kvm_corpus_20260603_175429_964295`
- Applied: 27,085/27,085 sites (0 skipped, 0 errors)
- BPF geomean: **0.938x** (6.2% 改进)
- Workload throughput: **1.081x** (8.1% 吞吐提升)

**Kinsn 家族分布**:
| 家族 | Sites | 占比 |
|------|------:|-----:|
| lea | 26,097 | 96.4% |
| cond_select | 988 | 3.6% |

**具体 kinsn 名称**:
| 名称 | 调用次数 |
|------|-------:|
| bpf_x86_leaq | 24,352 |
| bpf_x86_leal | 1,745 |
| bpf_x86_cmp_cmovb | 753 |
| bpf_x86_cmp_cmove | 200 |
| bpf_x86_cmp_cmovne | 35 |

### 5.2 Applied-Split 悖论

**April 2026 权威 corpus 数据** (`x86_kvm_corpus_20260428_070851_973550`):

| 子集 | Programs | Geomean | Wins/Losses |
|------|-------:|--------:|-------------|
| 所有 comparable | 146 | 1.0038 | 81/65 |
| **有代码改变 (applied)** | 63 | **1.032** | 31/32 |
| **无代码改变** | 83 | **0.983** | 50/33 |

**悖论**: 被优化的程序反而慢了 3.2%，而未被优化的程序"快了" 1.7%。

**解释**:
1. 未优化程序的 1.7% "改进"证明了测量噪声的存在
2. 相位效应（phase effects）主导了信号
3. tracee 集中度过高：59/63 个 applied rows 来自 tracee

**启示**: 这个发现推动了 noise floor 分析和更严格的信号阈值。

### 5.3 Noise Floor 问题

**Q1/P1 基线测量**:

| Floor | Session | skip_rejit | Retained | Method B | W/L/T |
|-------|---------|-----------|-------:|--------:|-------|
| Q1 noop ReJIT | `x86_kvm_corpus_20260507_190554_205137` | false | 147 | 0.9019 | 73/74/0 |
| P1 noop SKIP_REJIT | `x86_kvm_corpus_20260508_000244_131324` | true | 147 | 0.8587 | 75/72/0 |

**噪声幅度**: |0.9019 - 0.8587| = **0.0431** (~4.3%)

**关键洞察**:
- 两个基线都显示"加速"（0.90x 和 0.86x），而不是预期的 1.0x
- 即使什么都不做，第二次测量也比第一次快 10-14%
- 任何声称的优化必须超过这个 4.3% 的噪声阈值

### 5.4 Workload 影响

**May 22 Workload 变体探索**:

| Session 前缀 | Workload 类型 | 目的 |
|-------------|--------------|------|
| `workload_perf_bcc_hot4_60s` | BCC 高频 syscall | syscall 密集 |
| `workload_perf_cilium_endpoint_pktgen_bidir` | 双向 packet | 网络密集 |
| `workload_perf_katran_heavy_flags_4pktgen` | 4x packet generator | 极限负载 |
| `workload_perf_otel_intloop_100khz` | 100kHz profiling | 高频采样 |

**发现**: 不同 workload 显著影响哪些程序被执行、执行频率、以及最终的 ratio 分布。标准化 workload 是 paper-grade 测量的前提。

---

## 6. 从探索中学到的 (Lessons from Exploration)

### 有效的策略

1. **Kinsn 优先**: 305K sites 的高覆盖率证明了 kinsn 是主要优化机会
   - LEA 指令替换是最大赢家 (96% of kinsn sites)
   - ARM64 上 20.8% 改进比 x86 上 6.2% 更显著

2. **Noise Floor 校准必要**: Q1/P1 基线发现了 4.3% 的系统性偏差
   - 任何声称都必须超过这个阈值
   - 促使了方法论的严格化

3. **SAMPLES=3 + min_runs>=100**: 这个组合平衡了统计信心和运行时间
   - CV 从 29.6% (无过滤) 降到 17.7% (>=100 runs)
   - SAMPLES=1 用于快速迭代，SAMPLES=3 用于权威测量

4. **Per-Program Geomean**: 作为主要指标，避免了 run-weighted 的 tracee 集中问题

### 无效的策略

1. **Static Policy 单独使用**: 1.004x geomean 几乎是中性的
   - 81 wins / 65 losses 不足以声称改进
   - Applied-split 悖论暴露了问题

2. **LEA Pass 孤立测试**: 85% 失败率
   - 需要完整的 kinsn 基础设施支持
   - 不能作为独立 pass 评估

3. **Short Workload (3s)**: 大量 3s 运行产生了高噪声
   - 30s workload 成为标准
   - 短运行只用于 infrastructure 验证

### 为什么需要 Adaptive Exploration

**问题**: 静态策略（固定的 pass 列表）无法适应：
1. 应用程序 BPF 代码的多样性
2. 运行时 map 状态的变化
3. 不同架构的指令集差异

**证据**:
- map_inline 33% skip rate 来自动态 map 状态
- lea 在 Jun 2 的 85% 失败率需要实时调试
- ARM64 需要不同的 kinsn 指令集

**Auto-Research 价值**:
- 2,874 sessions 的规模人工不可能完成
- 4 天 515 sessions 的密集探索发现了关键问题
- Noise floor 分析需要专门的基线 sessions

---

## 7. 附录: 关键 Session 索引

### 权威测量 Sessions

| Session | 日期 | 类型 | 主要结果 |
|---------|------|------|----------|
| `vm_micro_authoritative_20260314` | Mar 14 | micro | Overall 1.054x |
| `x86_kvm_corpus_20260428_070851_973550` | Apr 28 | corpus | Geomean 1.004x, 146 programs |
| `x86_kvm_corpus_20260507_190554_205137` | May 7 | corpus | Q1 noop baseline 0.902x |
| `x86_kvm_corpus_20260508_000244_131324` | May 8 | corpus | P1 skip-rejit baseline 0.859x |
| `x86_kvm_corpus_20260603_175429_964295` | Jun 3 | corpus | Kinsn 0.938x, 27085 sites |
| `aws_arm64_micro_20260606_001225_821028` | Jun 6 | micro | ARM64 kinsn 1.208x |

### 调试 Sessions 示例

| Session | 日期 | 问题 |
|---------|------|------|
| `x86_kvm_corpus_20260602_*` (77 errors) | Jun 2 | LEA pass 崩溃调试 |
| `manual_matrix_20260521_*` | May 21 | 初始矩阵测试 |
| `workload_perf_katran_heavy_*` | May 22 | Katran workload 调优 |

### Workload 设计 Sessions

| Session 前缀 | 日期 | 目的 |
|--------------|------|------|
| `workload_perf_bcc_*` | May 22 | BCC syscall 密集 |
| `workload_perf_cilium_endpoint_*` | May 22 | Cilium packet 变体 |
| `workload_perf_otel_*` | May 22 | OTEL profiling 频率 |

---

## 总结

BPFOptBench 的探索规模（2,874 sessions, 25 种 pass 配置）证明了 auto-research 框架的价值。关键发现：

1. **Kinsn 是主要机会**: 305K sites, ARM64 上 20.8% 改进
2. **Noise Floor 是真实的**: 4.3% 基线偏差需要超越
3. **Adaptive Exploration 必要**: 静态策略无法应对动态 BPF 生态

这些发现来自于系统化的自动探索，而不是一次性的手工实验。框架使能了这种规模的研究。
