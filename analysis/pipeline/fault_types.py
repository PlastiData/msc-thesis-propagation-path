"""Fault type integer → name and OpenRCA 2.0 injection taxonomy.

Int keys match `FAULT_TYPES` index in
`src/rcabench_platform/v2/datasets/rcabench.py` (injection.json `fault_type`).
Taxonomy fields follow OpenRCA 2.0 Tables 5–6 (Chaos Mesh category, target
layer, Table-6 fault_kind collapse). This is the injected-fault benchmark
label, not a detected error type and not Table 7 rule firing.
"""

from __future__ import annotations

import warnings
from typing import Any

# Legacy browser slugs (investigation UI). Prefer chaos_type from taxonomy.
FAULT_TYPE_NAMES: dict[int, str] = {
    0: "pod_kill",
    1: "pod_failure",
    2: "container_kill",
    3: "memory_stress",
    4: "cpu_stress",
    5: "request_abort",
    6: "response_abort",
    7: "request_delay",
    8: "response_delay",
    9: "response_replace_body",
    10: "response_patch_body",
    11: "request_replace_path",
    12: "request_replace_method",
    13: "response_replace_code",
    14: "dns_error",
    15: "dns_random",
    16: "time_skew",
    17: "network_delay",
    18: "network_loss",
    19: "network_duplicate",
    20: "network_corrupt",
    21: "network_bandwidth",
    22: "network_partition",
    23: "jvm_latency",
    24: "jvm_return",
    25: "jvm_exception",
    26: "jvm_gc",
    27: "jvm_cpu_stress",
    28: "jvm_memory_stress",
    29: "jvm_mysql_latency",
    30: "jvm_mysql_exception",
}

# OpenRCA 2.0 Tables 5–6. Rules live in data, not an if-chain.
# channel: vertical | horizontal | vertical+horizontal
_INJECTION_TAXONOMY: dict[int, dict[str, str]] = {
    0: {
        "category": "PodChaos",
        "chaos_type": "PodKill",
        "target_layer": "infrastructure",
        "expected_propagation_channel": "vertical",
        "fault_kind": "pod_failure",
        "obs_channel_expected": "trace emission gap, brief, recovers in window",
    },
    1: {
        "category": "PodChaos",
        "chaos_type": "PodFailure",
        "target_layer": "infrastructure",
        "expected_propagation_channel": "vertical",
        "fault_kind": "pod_unavailable",
        "obs_channel_expected": "trace emission gap, sustained to window end",
    },
    2: {
        "category": "PodChaos",
        "chaos_type": "ContainerKill",
        "target_layer": "infrastructure",
        "expected_propagation_channel": "vertical",
        "fault_kind": "pod_failure",
        "obs_channel_expected": "trace emission gap, brief, recovers in window",
    },
    3: {
        "category": "StressChaos",
        "chaos_type": "MemoryStress",
        "target_layer": "infrastructure",
        "expected_propagation_channel": "vertical",
        "fault_kind": "mem_stress",
        "obs_channel_expected": "container.memory.* saturated",
    },
    4: {
        "category": "StressChaos",
        "chaos_type": "CPUStress",
        "target_layer": "infrastructure",
        "expected_propagation_channel": "vertical",
        "fault_kind": "cpu_stress",
        "obs_channel_expected": "container.cpu.* saturated",
    },
    5: {
        "category": "HTTPChaos",
        "chaos_type": "HTTPRequestAbort",
        "target_layer": "application",
        "expected_propagation_channel": "horizontal",
        "fault_kind": "http_aborted",
        "obs_channel_expected": "HTTP span status, request-failure rate",
    },
    6: {
        "category": "HTTPChaos",
        "chaos_type": "HTTPResponseAbort",
        "target_layer": "application",
        "expected_propagation_channel": "horizontal",
        "fault_kind": "http_aborted",
        "obs_channel_expected": "HTTP span status, request-failure rate",
    },
    7: {
        "category": "HTTPChaos",
        "chaos_type": "HTTPRequestDelay",
        "target_layer": "application",
        "expected_propagation_channel": "horizontal",
        "fault_kind": "http_slow",
        "obs_channel_expected": "HTTP span duration distribution",
    },
    8: {
        "category": "HTTPChaos",
        "chaos_type": "HTTPResponseDelay",
        "target_layer": "application",
        "expected_propagation_channel": "horizontal",
        "fault_kind": "http_slow",
        "obs_channel_expected": "HTTP span duration distribution",
    },
    9: {
        "category": "HTTPChaos",
        "chaos_type": "HTTPResponseReplaceBody",
        "target_layer": "application",
        "expected_propagation_channel": "horizontal",
        "fault_kind": "http_payload_modified",
        "obs_channel_expected": "response body differs from baseline",
    },
    10: {
        "category": "HTTPChaos",
        "chaos_type": "HTTPResponsePatchBody",
        "target_layer": "application",
        "expected_propagation_channel": "horizontal",
        "fault_kind": "http_payload_modified",
        "obs_channel_expected": "response body differs from baseline",
    },
    11: {
        "category": "HTTPChaos",
        "chaos_type": "HTTPRequestReplacePath",
        "target_layer": "application",
        "expected_propagation_channel": "horizontal",
        "fault_kind": "http_payload_modified",
        "obs_channel_expected": "request path differs from baseline",
    },
    12: {
        "category": "HTTPChaos",
        "chaos_type": "HTTPRequestReplaceMethod",
        "target_layer": "application",
        "expected_propagation_channel": "horizontal",
        "fault_kind": "http_payload_modified",
        "obs_channel_expected": "request method differs from baseline",
    },
    13: {
        "category": "HTTPChaos",
        "chaos_type": "HTTPResponseReplaceCode",
        "target_layer": "application",
        "expected_propagation_channel": "horizontal",
        "fault_kind": "http_response_status_modified",
        "obs_channel_expected": "HTTP span status-code distribution",
    },
    14: {
        "category": "DNSChaos",
        "chaos_type": "DNSError",
        "target_layer": "infrastructure",
        "expected_propagation_channel": "vertical",
        "fault_kind": "dns_resolution_failed",
        "obs_channel_expected": "DNS error log entries on the affected service",
    },
    15: {
        "category": "DNSChaos",
        "chaos_type": "DNSRandom",
        "target_layer": "infrastructure",
        "expected_propagation_channel": "vertical",
        "fault_kind": "dns_resolution_wrong",
        "obs_channel_expected": "resolution succeeds but returns wrong target",
    },
    16: {
        "category": "TimeChaos",
        "chaos_type": "TimeSkew",
        "target_layer": "infrastructure",
        "expected_propagation_channel": "vertical",
        "fault_kind": "clock_skew",
        "obs_channel_expected": "cross-service timestamp drift in correlated logs",
    },
    17: {
        "category": "NetworkChaos",
        "chaos_type": "NetworkDelay",
        "target_layer": "infrastructure",
        "expected_propagation_channel": "vertical+horizontal",
        "fault_kind": "network_delay",
        "obs_channel_expected": "container.network.*, trace latency tail",
    },
    18: {
        "category": "NetworkChaos",
        "chaos_type": "NetworkLoss",
        "target_layer": "infrastructure",
        "expected_propagation_channel": "vertical+horizontal",
        "fault_kind": "network_loss",
        "obs_channel_expected": "container.network.*, trace retry pattern",
    },
    19: {
        "category": "NetworkChaos",
        "chaos_type": "NetworkDuplicate",
        "target_layer": "infrastructure",
        "expected_propagation_channel": "vertical+horizontal",
        "fault_kind": "network_duplicate",
        "obs_channel_expected": "container.network.*, duplicate-ack pattern",
    },
    20: {
        "category": "NetworkChaos",
        "chaos_type": "NetworkCorrupt",
        "target_layer": "infrastructure",
        "expected_propagation_channel": "vertical+horizontal",
        "fault_kind": "network_corrupt",
        "obs_channel_expected": "container.network.*, TCP retransmit signal",
    },
    21: {
        "category": "NetworkChaos",
        "chaos_type": "NetworkBandwidth",
        "target_layer": "infrastructure",
        "expected_propagation_channel": "vertical+horizontal",
        "fault_kind": "network_bandwidth_limit",
        "obs_channel_expected": "container.network.*, throughput drop",
    },
    22: {
        "category": "NetworkChaos",
        "chaos_type": "NetworkPartition",
        "target_layer": "infrastructure",
        "expected_propagation_channel": "vertical+horizontal",
        "fault_kind": "network_partition",
        "obs_channel_expected": "container.network.*, timeout share approaches one",
    },
    23: {
        "category": "JVMChaos",
        "chaos_type": "JVMLatency",
        "target_layer": "application",
        "expected_propagation_channel": "horizontal",
        "fault_kind": "jvm_method_latency",
        "obs_channel_expected": "elevated span duration on a method",
    },
    24: {
        "category": "JVMChaos",
        "chaos_type": "JVMReturn",
        "target_layer": "application",
        "expected_propagation_channel": "horizontal",
        "fault_kind": "jvm_method_mutated",
        "obs_channel_expected": "method returns a value differing from baseline",
    },
    25: {
        "category": "JVMChaos",
        "chaos_type": "JVMException",
        "target_layer": "application",
        "expected_propagation_channel": "horizontal",
        "fault_kind": "jvm_method_exception",
        "obs_channel_expected": "log exception class on a specific method",
    },
    26: {
        "category": "JVMChaos",
        "chaos_type": "JVMGarbageCollector",
        "target_layer": "application",
        "expected_propagation_channel": "vertical",
        "fault_kind": "jvm_gc_pressure",
        "obs_channel_expected": "jvm.gc.duration histogram spikes",
    },
    27: {
        "category": "JVMChaos",
        "chaos_type": "JVMCPUStress",
        "target_layer": "application",
        "expected_propagation_channel": "vertical",
        "fault_kind": "jvm_thread_cpu_stress",
        "obs_channel_expected": "jvm.cpu.* elevated, container CPU normal",
    },
    28: {
        "category": "JVMChaos",
        "chaos_type": "JVMMemoryStress",
        "target_layer": "application",
        "expected_propagation_channel": "vertical",
        "fault_kind": "jvm_heap_stress",
        "obs_channel_expected": "jvm.memory.used climbs to limit",
    },
    29: {
        "category": "JVMChaos",
        "chaos_type": "JVMMySQLLatency",
        "target_layer": "application",
        "expected_propagation_channel": "horizontal",
        "fault_kind": "jvm_jdbc_latency",
        "obs_channel_expected": "elevated span duration on a JDBC call",
    },
    30: {
        "category": "JVMChaos",
        "chaos_type": "JVMMySQLException",
        "target_layer": "application",
        "expected_propagation_channel": "horizontal",
        "fault_kind": "jvm_jdbc_exception",
        "obs_channel_expected": "exception on a JDBC client call",
    },
}

TAXONOMY_FIELDS = (
    "category",
    "chaos_type",
    "target_layer",
    "expected_propagation_channel",
    "fault_kind",
    "obs_channel_expected",
)


def fault_name(ft: int) -> str:
    if ft in FAULT_TYPE_NAMES:
        return FAULT_TYPE_NAMES[ft]
    warnings.warn(f"Unknown fault_type {ft}")
    return f"unknown_{ft}"


def all_fault_slugs() -> list[str]:
    return sorted(set(FAULT_TYPE_NAMES.values()))


def all_taxonomy_fault_types() -> list[int]:
    return sorted(_INJECTION_TAXONOMY)


def injection_taxonomy(fault_type: Any) -> dict[str, Any]:
    """Map injection.json fault_type int → OpenRCA Tables 5–6 fields.

    Returns a dict always. Unmapped ints get mapped=False and unknown_* labels.
    """
    if fault_type is None:
        return _unknown_taxonomy(None, reason="fault_type_missing")
    try:
        ft = int(fault_type)
    except (TypeError, ValueError):
        return _unknown_taxonomy(fault_type, reason="fault_type_not_int")
    row = _INJECTION_TAXONOMY.get(ft)
    if not row:
        return _unknown_taxonomy(ft, reason="fault_type_unmapped")
    out = {"fault_type": ft, "mapped": True, **row}
    return out


def _unknown_taxonomy(fault_type: Any, *, reason: str) -> dict[str, Any]:
    return {
        "fault_type": fault_type,
        "mapped": False,
        "category": "unknown",
        "chaos_type": f"unknown_{fault_type}",
        "target_layer": "unknown",
        "expected_propagation_channel": "unknown",
        "fault_kind": f"unknown_{fault_type}",
        "obs_channel_expected": reason,
    }


FAULT_TYPE_DESCRIPTIONS: dict[str, str] = {
    "pod_kill": "Kubernetes pod is forcefully terminated.",
    "pod_failure": "Pod enters a failed state and stops serving traffic.",
    "container_kill": "A container inside a pod is terminated (process killed).",
    "memory_stress": "Memory stress is applied to exhaust RAM.",
    "cpu_stress": "CPU stress is applied to exhaust compute resources.",
    "request_abort": "Outgoing HTTP request is aborted before completion.",
    "response_abort": "HTTP response is aborted mid-stream.",
    "request_delay": "Artificial delay injected into outgoing HTTP requests.",
    "response_delay": "Artificial delay injected into HTTP responses.",
    "response_replace_body": "HTTP response body is replaced with faulty content.",
    "response_patch_body": "HTTP response body is partially patched.",
    "request_replace_path": "HTTP request path is replaced.",
    "request_replace_method": "HTTP request method is replaced.",
    "response_replace_code": "HTTP response status code is replaced.",
    "dns_error": "DNS resolution fails for the target hostname.",
    "dns_random": "DNS resolution returns an incorrect target.",
    "time_skew": "System clock is manipulated.",
    "network_delay": "Network packets are delayed.",
    "network_loss": "Network packets are dropped.",
    "network_duplicate": "Network packets are duplicated.",
    "network_corrupt": "Network packets are corrupted.",
    "network_bandwidth": "Available network bandwidth is constrained.",
    "network_partition": "Network partition isolates the target from peers.",
    "jvm_latency": "JVM method latency is artificially increased.",
    "jvm_return": "JVM method return value is altered.",
    "jvm_exception": "An exception is injected into a JVM method.",
    "jvm_gc": "JVM garbage collector pressure is induced.",
    "jvm_cpu_stress": "JVM-level CPU stress is applied.",
    "jvm_memory_stress": "JVM heap or stack memory stress is applied.",
    "jvm_mysql_latency": "JDBC/MySQL client call latency is increased.",
    "jvm_mysql_exception": "An exception is injected on a JDBC/MySQL client call.",
    # Legacy slugs kept so old HTML artifacts still resolve.
    "dns": "DNS resolution is disrupted.",
    "time": "System clock is manipulated.",
    "network_latency": "Network latency is increased.",
    "return": "Function return value is altered.",
    "exception": "An exception is injected into the target code path.",
    "mysql_fault": "MySQL database fault is injected.",
}


def fault_description(slug: str) -> str:
    if slug in FAULT_TYPE_DESCRIPTIONS:
        return FAULT_TYPE_DESCRIPTIONS[slug]
    if slug.startswith("unknown_"):
        return "Unknown fault type (see dataset documentation)."
    return "Fault type description not available."


def fault_display_name(slug: str) -> str:
    return slug.replace("_", " ").title()
