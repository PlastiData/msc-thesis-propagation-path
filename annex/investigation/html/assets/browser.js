(function () {
  "use strict";

  const table = document.getElementById("incidents-table");
  const tbody = table && table.querySelector("tbody");
  const searchInput = document.getElementById("search");
  const faultFilter = document.getElementById("filter-fault");
  const serviceFilter = document.getElementById("filter-service");
  const sloFilter = document.getElementById("filter-slo");
  const missingFilter = document.getElementById("filter-missing");
  const sortSelect = document.getElementById("sort-by");
  const countEl = document.getElementById("result-count");

  if (!tbody || !window.INCIDENTS_INDEX) return;

  let rows = window.INCIDENTS_INDEX.slice();

  function populateFilters() {
    const faults = new Set();
    const services = new Set();
    rows.forEach(function (r) {
      faults.add(r.fault_type);
      (r.root_cause_services || []).forEach(function (s) { services.add(s); });
    });
    Array.from(faults).sort().forEach(function (f) {
      const opt = document.createElement("option");
      opt.value = f;
      opt.textContent = f;
      faultFilter.appendChild(opt);
    });
    Array.from(services).sort().forEach(function (s) {
      const opt = document.createElement("option");
      opt.value = s;
      opt.textContent = s;
      serviceFilter.appendChild(opt);
    });
  }

  function matches(row) {
    const q = (searchInput.value || "").toLowerCase();
    if (q && row.incident_id.toLowerCase().indexOf(q) === -1) return false;
    if (faultFilter.value && row.fault_type !== faultFilter.value) return false;
    if (serviceFilter.value && (row.root_cause_services || []).indexOf(serviceFilter.value) === -1) return false;
    if (sloFilter.value === "yes" && !row.slo_violated) return false;
    if (sloFilter.value === "no" && row.slo_violated) return false;
    if (missingFilter.value === "yes" && (!row.missing_files || row.missing_files.length === 0)) return false;
    if (missingFilter.value === "no" && row.missing_files && row.missing_files.length > 0) return false;
    return true;
  }

  function sortRows(list) {
    const key = sortSelect.value;
    return list.slice().sort(function (a, b) {
      if (key === "start_time") return (a.start_time || "").localeCompare(b.start_time || "");
      if (key === "fault_type") return a.fault_type.localeCompare(b.fault_type);
      if (key === "abnormal_trace_rows") return (b.abnormal_trace_rows || 0) - (a.abnormal_trace_rows || 0);
      return a.incident_id.localeCompare(b.incident_id);
    });
  }

  function render() {
    const filtered = sortRows(rows.filter(matches));
    tbody.innerHTML = "";
    filtered.forEach(function (r) {
      const tr = document.createElement("tr");
      const missing = (r.missing_files && r.missing_files.length) ? "MISSING FILE" : "";
      tr.innerHTML =
        '<td class="mono"><a href="' + r.html_path + '">' + r.incident_id + "</a></td>" +
        "<td>" + r.fault_type + "</td>" +
        "<td>" + (r.root_cause_services || []).join(", ") + "</td>" +
        "<td>" + (r.slo_violated ? '<span class="badge badge-slo">SLO</span>' : "") +
        (missing ? ' <span class="badge badge-missing">' + missing + "</span>" : "") + "</td>" +
        "<td>" + (r.abnormal_trace_rows || 0).toLocaleString() + "</td>" +
        "<td>" + (r.start_time || "") + "</td>";
      tbody.appendChild(tr);
    });
    if (countEl) countEl.textContent = filtered.length + " / " + rows.length + " incidents";
  }

  populateFilters();
  ["input", "change"].forEach(function (ev) {
    searchInput.addEventListener(ev, render);
    faultFilter.addEventListener(ev, render);
    serviceFilter.addEventListener(ev, render);
    sloFilter.addEventListener(ev, render);
    missingFilter.addEventListener(ev, render);
    sortSelect.addEventListener(ev, render);
  });
  render();
})();
