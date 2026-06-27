# Chapter 13: Instrumentation

## Core Idea
You cannot study what you cannot measure. Instrumentation is the science of choosing, configuring, and calibrating sensors to collect data that can actually answer your research question. In cyber security, most available sensors were built for operational use — not scientific rigor — and using them uncritically produces data with hidden limitations.

## Frameworks Introduced

- **5 Axes of Data Fidelity**: The quality dimensions of any data collection effort:
  1. **Time Fidelity** — accuracy/precision of measurement timestamps; critical for determining event ordering and causality. NTP ≈ millisecond precision; GPS ≈ nanosecond precision.
  2. **Sample Rate** — frequency of data collection; options: full capture, filtered (subset by type), truncated (partial records), downsampled (1-in-N). Choose based on whether the phenomenon of interest appears in what you're keeping.
  3. **Summarization/Compression** — level of aggregation (e.g., packet captures vs. NetFlow); aggregation removes payload content; truncation removes tail data. Know what information your summarization removes before choosing it.
  4. **Proxy** — when direct measurement is impossible (e.g., attacker intent), use indirect observables. Verify the proxy captures the right abstraction level: not too low (electron-level), not too high (aggregate patterns that miss individual events).
  5. **Scale** — number and placement of sensors; must cover all locations where the phenomenon manifests. A worm study needs sensors on infected hosts AND on DNS/C2 channels.
  - When to use: As a checklist when designing the instrumentation plan for any research project.
  - How: Map each research question to a data requirement, then check all 5 axes for each data source to confirm it's adequate.

- **Scientific vs. Operational Instrumentation**: Sensors built for operations optimize for usability, efficiency, and cost — not scientific coverage and fidelity. Research requires explicit calibration and validation of operational sensors before use.
  - When to use: Every time you reuse operational data (e.g., SIEM logs, firewall logs, NetFlow) for research.
  - How: Document what each operational sensor collects, what it omits, and what limitations those omissions impose on your conclusions.

- **Testbed Design**: A controlled experimental environment that mimics operational conditions at reduced scale.
  - When to use: When operational environment variables cannot be controlled for experimentation.
  - How: Define the fidelity requirements first; select testbed components that meet those requirements; validate that testbed behavior matches operational behavior in controlled cases before using it for research.

## Key Concepts
- **Instrumentation** — the tools, sensors, and processes used to collect data; the physical manifestation of the research data collection plan
- **Data Fidelity** — accuracy and completeness of collected data along multiple axes (time, sample rate, summarization, proxy, scale)
- **Time Fidelity** — precision of sensor timestamps; determines causal ordering resolution
- **Sample Rate** — collection frequency; full capture vs. filtered, truncated, or downsampled
- **Full Packet Capture** — captures complete network packets including payload; highest fidelity, highest storage/processing cost
- **NetFlow / IPFIX** — flow-level summaries (source IP/port, destination IP/port, bytes, duration); loses payload content; good for behavioral pattern analysis
- **Summarization** — aggregating raw data into higher-level summaries; reduces storage but loses detail
- **Truncation** — capturing only a portion of each record (e.g., packet headers only); preserves structure, loses payload
- **Downsampling** — collecting 1-in-N records; reduces volume; may miss rare events
- **Proxy Measurement** — indirect observation of an unmeasurable phenomenon (e.g., inferring attacker intent from network behavior)
- **Testbed** — controlled cyber environment for experimentation; replicates operational conditions at reduced scale
- **Coverage** — the degree to which sensors capture all instances of the phenomenon across all relevant locations in the system
- **Extraneous Variable (Sensor-introduced)** — a measurement artifact caused by sensor design choices (e.g., unsynchronized clocks creating false event ordering)

## Mental Models
- Think of instrumentation as "operationalizing your research questions into data." For every question, ask: "What data would prove or disprove this if I had it?" Then work backward to "what sensor produces that data?"
- The most available sensor is rarely the most appropriate sensor for research. Log what your operational tools collect, then explicitly check if that's enough.
- Unsynchronized clocks across sensors is the silent killer of causal analysis — always verify time synchronization before a study that depends on event ordering.
- NetFlow is "who talked to whom and when" — not "what was said." The moment your research question requires content, NetFlow is insufficient.
- Sensor coverage = making sure the phenomenon "can't escape" your measurement net. A worm that spreads via fast-flux DNS is invisible if you only instrument the endpoints.

## Anti-patterns
- **Using operational sensors uncritically**: Operational sensors optimize for performance, not scientific fidelity; their blind spots become your study's confounders.
- **Truncating packet captures without checking for payload-relevant phenomena**: If the attack pattern lives in HTTP headers and you truncated to TCP headers, you've collected the wrong data.
- **Relying on NetFlow for content-based research**: NetFlow strips payload; studying DPI-detectable threats with NetFlow alone will miss the detection signal.
- **Misaligned sensor clock synchronization**: Out-of-sync clocks create false event orderings; NTP is insufficient for nanosecond-scale analysis. Verify time sync precision before the study.
- **Single-location sensor placement**: A phenomenon that manifests at multiple points in the network (e.g., multi-stage attacks) requires sensors at all relevant points, not just one.
- **Oversampling without purpose**: Full packet capture generates enormous data volumes; don't default to "collect everything" without confirming storage and processing capacity matches.

## Reference Tables

| Data Type | What it Captures | What it Loses | Best For |
|---|---|---|---|
| Full Packet Capture (PCAP) | All packet content, headers, payload | Nothing (within interface capacity) | Protocol analysis, payload-based attack detection |
| NetFlow / IPFIX | Flow metadata (IPs, ports, bytes, duration) | Payload, packet timing details | Behavioral analysis, anomaly detection, lateral movement |
| Host Logs (OS, syslog) | System events, process activity | Network behavior, inter-host context | Endpoint behavior, privilege escalation, persistence |
| DNS Logs | Query/response pairs, TTLs | Payload, encrypted C2 | C2 detection, domain generation algorithms |
| Memory Dump | Runtime state, volatile memory | Persistent storage, network | Malware analysis, in-memory attack detection |

| Fidelity Axis | Question to Ask | If Insufficient → |
|---|---|---|
| Time | Can I determine event ordering to the precision needed? | Add GPS time sync; calibrate NTP offsets |
| Sample Rate | Am I missing rare events by downsampling? | Increase rate or use triggers for suspicious traffic |
| Summarization | Does my aggregation remove information I need? | Use higher-fidelity collection (e.g., PCAP instead of NetFlow) |
| Proxy | Does my indirect measure capture the right level of abstraction? | Find a closer proxy or accept the limitation explicitly |
| Scale | Are all locations where the phenomenon appears instrumented? | Add sensors at missing points; use distributed collection |

## Worked Example
**Instrumentation Plan for a Lateral Movement Study:**

Research question: "Does lateral movement through WMI (Windows Management Instrumentation) leave detectable signatures in network flow data?"

1. **Fidelity analysis**:
   - Time fidelity: NetFlow reports flows at 15-second intervals → sufficient to detect connection patterns, but may not capture sub-second burst behavior → add full PCAP on the target subnet
   - Sample rate: Full capture on 1Gbps internal network → feasible; on 10Gbps core → add 10G capture hardware or filter to WMI traffic (port 135, port 445)
   - Summarization: NetFlow loses WMI RPC payload → insufficient for payload-based detection; need PCAP for payload analysis
   - Proxy: Network behavior is a proxy for "attacker used WMI" → valid if WMI produces unique flow signatures; verify against controlled WMI executions
   - Scale: Place sensors on: target host's network interface, domain controller (authentication logs), DNS resolver (for potential name resolution)

2. **Sensor selection**:
   - PCAP on subnet switch span port (payload-level WMI detection)
   - NetFlow on core router (behavioral pattern analysis, connection frequency)
   - Windows Event Logs (Event ID 4688 process creation, 4624 logon) on target and DC
   - DNS query logs on DNS resolver

3. **Time sync verification**: Confirm NTP sync <5ms drift across all sensors before collection

## Key Takeaways
1. Map research questions to data requirements BEFORE selecting sensors — don't start with what's available and work backward to the question.
2. Check all 5 fidelity axes (time, sample rate, summarization, proxy, scale) for every data source; gaps in any axis constrain what conclusions you can draw.
3. Operational sensors were designed for operational use, not scientific rigor — validate them explicitly and document their limitations in your methodology.
4. Time synchronization is a prerequisite for any study involving event ordering or causal analysis.
5. Don't default to full packet capture unless you've confirmed storage capacity; don't default to NetFlow unless you've confirmed you don't need payload data.

## Connects To
- **Ch 9**: Hypothetico-deductive — experimental design must specify instrumentation as part of the experimental design documentation
- **Ch 10**: Quasi-experimental — operational environments require careful instrumentation to compensate for the lack of experimental control
- **Ch 11–12**: Applied Experimentation and Applied Observational — operational bounds testing requires correctly calibrated performance sensors
- **Ch 4–5**: Exploratory/Descriptive — data collection for observational studies follows the same fidelity analysis process
