const API_BASE = "/api";

const runForm = document.getElementById("run-form");
const endpointsInput = document.getElementById("endpoints-input");
const modeSelect = document.getElementById("mode-select");
const clearFormBtn = document.getElementById("clear-form");
const statusPill = document.getElementById("run-status-pill");
const progressCard = document.getElementById("progress-card");
const resultsCard = document.getElementById("results-card");
const runIdDisplay = document.getElementById("run-id-display");
const copyRunIdBtn = document.getElementById("copy-run-id");
const logOutput = document.getElementById("log-output");
const logStatus = document.getElementById("log-status");
const metricTotal = document.getElementById("metric-total");
const metricGo = document.getElementById("metric-go");
const metricNoGo = document.getElementById("metric-nogo");
const metricIndeterminate = document.getElementById("metric-indeterminate");
const artifactContainer = document.getElementById("artifact-links");
const artifactList = artifactContainer.querySelector("ul");
const decisionFilter = document.getElementById("decision-filter");
const resultsTableBody = document.querySelector("#results-table tbody");
const rowTemplate = document.getElementById("assessment-row-template");
const resultDetail = document.getElementById("result-detail");
const detailTitle = document.getElementById("detail-title");
const detailList = document.getElementById("detail-list");
const detailAnalysis = document.getElementById("detail-analysis");
const detailReportContainer = document.getElementById("full-report-container");
const detailReport = document.getElementById("detail-report");

const state = {
  runId: null,
  logOffset: 0,
  logTimer: null,
  summaryTimer: null,
  decisionFilter: "",
  fullReportMarkdown: null,
};

runForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const endpoints = sanitizeEndpoints(endpointsInput.value);
  if (!endpoints) {
    alert("Please paste at least one HigherGov search ID.");
    return;
  }

  toggleForm(false);
  resetRunState();
  setStatus("Starting…", "running");
  logOutput.textContent = "";
  logStatus.textContent = "Waiting for pipeline…";
  progressCard.classList.remove("hidden");
  resultsCard.classList.add("hidden");
  resultDetail.hidden = true;

  try {
    const response = await fetch(`${API_BASE}/runs`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ endpoints, mode: modeSelect.value }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error?.detail || "Failed to start pipeline");
    }

    const payload = await response.json();
    state.runId = payload.run_id;
    runIdDisplay.textContent = payload.run_id;
    setStatus("Running", "running");
    startPolling();
  } catch (err) {
    console.error(err);
    alert(err.message || "Unable to start the pipeline run.");
    toggleForm(true);
    setStatus("Idle", "idle");
  }
});

clearFormBtn.addEventListener("click", () => {
  endpointsInput.value = "";
});

copyRunIdBtn.addEventListener("click", async () => {
  if (!state.runId) return;
  try {
    await navigator.clipboard.writeText(state.runId);
    copyRunIdBtn.textContent = "Copied";
    setTimeout(() => (copyRunIdBtn.textContent = "Copy"), 1500);
  } catch (err) {
    console.warn("Clipboard unavailable", err);
  }
});

decisionFilter.addEventListener("change", () => {
  state.decisionFilter = decisionFilter.value;
  if (state.runId) {
    fetchSummary(true);
  }
});

function sanitizeEndpoints(raw) {
  return raw
    .split("\n")
    .map((line) => line.trim())
    .filter((line) => line && !line.startsWith("#"))
    .join("\n");
}

function toggleForm(enabled) {
  [endpointsInput, modeSelect, clearFormBtn].forEach((el) => {
    el.disabled = !enabled;
  });
  runForm.querySelector("button[type=submit]").disabled = !enabled;
}

function resetRunState() {
  if (state.logTimer) {
    clearTimeout(state.logTimer);
    state.logTimer = null;
  }
  if (state.summaryTimer) {
    clearTimeout(state.summaryTimer);
    state.summaryTimer = null;
  }
  state.runId = null;
  state.logOffset = 0;
  state.fullReportMarkdown = null;
  resultsTableBody.innerHTML = "";
  artifactList.innerHTML = "";
  artifactContainer.hidden = true;
  detailList.innerHTML = "";
  detailAnalysis.textContent = "";
  detailReportContainer.hidden = true;
}

function setStatus(text, statusClass) {
  statusPill.textContent = text;
  statusPill.className = "status-pill";
  if (statusClass === "running") {
    statusPill.classList.add("running-pill");
  } else if (statusClass === "completed") {
    statusPill.classList.add("completed-pill");
  } else if (statusClass === "failed") {
    statusPill.classList.add("failed-pill");
  }
}

function startPolling() {
  state.logOffset = 0;
  fetchLogs();
  fetchSummary(true);
}

async function fetchLogs() {
  if (!state.runId) return;
  try {
    const response = await fetch(
      `${API_BASE}/runs/${encodeURIComponent(state.runId)}/logs?offset=${state.logOffset}`
    );
    if (!response.ok) {
      throw new Error("Failed to fetch logs");
    }
    const chunk = await response.json();
    if (chunk.text) {
      logOutput.textContent += chunk.text;
      logOutput.scrollTop = logOutput.scrollHeight;
    }
    state.logOffset = chunk.offset;
    logStatus.textContent = chunk.complete ? "Log captured" : "Streaming…";

    if (!chunk.complete) {
      state.logTimer = setTimeout(fetchLogs, 1500);
    }
  } catch (err) {
    console.error(err);
    logStatus.textContent = "Log stream interrupted";
  }
}

async function fetchSummary(force = false) {
  if (!state.runId) return;
  try {
    const params = new URLSearchParams();
    if (state.decisionFilter) params.set("decision", state.decisionFilter);
    if (force) params.set("offset", "0");
    params.set("limit", "200");

    const response = await fetch(
      `${API_BASE}/runs/${encodeURIComponent(state.runId)}/summary?${params.toString()}`
    );
    if (!response.ok) {
      if (response.status === 404) {
        // summary not ready yet
        state.summaryTimer = setTimeout(() => fetchSummary(false), 3000);
        return;
      }
      throw new Error("Failed to fetch summary");
    }
    const data = await response.json();
    updateSummary(data);

    if (data.status === "running") {
      state.summaryTimer = setTimeout(() => fetchSummary(false), 4000);
    } else {
      toggleForm(true);
    }
  } catch (err) {
    console.error(err);
    state.summaryTimer = setTimeout(() => fetchSummary(false), 5000);
  }
}

function updateSummary(data) {
  const { metadata = {}, summary = {}, files = [] } = data;
  metricTotal.textContent = metadata.total ?? 0;
  metricGo.textContent = summary.go ?? 0;
  metricNoGo.textContent = summary.no_go ?? 0;
  metricIndeterminate.textContent = summary.indeterminate ?? 0;

  if (files.length) {
    artifactContainer.hidden = false;
    artifactList.innerHTML = "";
    files.forEach((file) => {
      const li = document.createElement("li");
      const link = document.createElement("a");
      link.href = `/artifacts/${file.relative_path.replace(/\\\\/g, "/")}`;
      link.target = "_blank";
      link.rel = "noopener";
      link.textContent = `${file.label}`;
      li.appendChild(link);
      artifactList.appendChild(li);
    });
  }

  renderAssessments(data.assessments || []);
  state.fullReportMarkdown = data.full_report_markdown;

  if (data.status === "completed") {
    setStatus("Completed", "completed");
  } else if (data.status === "failed") {
    setStatus("Failed", "failed");
  } else {
    setStatus("Running", "running");
  }

  progressCard.classList.remove("hidden");
  resultsCard.classList.remove("hidden");
}

function renderAssessments(list) {
  resultsTableBody.innerHTML = "";
  if (!list.length) {
    const row = resultsTableBody.insertRow();
    const cell = row.insertCell();
    cell.colSpan = 5;
    cell.className = "empty-row";
    cell.textContent = "No assessments available yet.";
    return;
  }

  list.forEach((item) => {
    const clone = rowTemplate.content.firstElementChild.cloneNode(true);
    const decisionCell = clone.querySelector(".decision-cell");
    decisionCell.textContent = item.final_decision || "";
    decisionCell.classList.add(decisionClass(decisionCell.textContent));

    clone.querySelector(".title-cell").textContent = item.announcement_title || item.sos_pipeline_title || "—";
    clone.querySelector(".agency-cell").textContent = item.agency || "—";
    clone.querySelector(".reason-cell").textContent = item.knock_pattern || item.analysis_notes || "—";
    clone.querySelector(".knockout-cell").textContent = item.knockout_category || "—";

    clone.addEventListener("click", () => showDetail(item));
    resultsTableBody.appendChild(clone);
  });
}

function decisionClass(decision) {
  const upper = (decision || "").toUpperCase();
  if (upper === "GO") return "go";
  if (upper === "NO-GO") return "no-go";
  if (upper === "INDETERMINATE") return "indeterminate";
  return "";
}

function showDetail(item) {
  resultDetail.hidden = false;
  detailTitle.textContent = item.announcement_title || item.sos_pipeline_title || "Opportunity";
  detailList.innerHTML = "";

  const fields = [
    ["Decision", item.final_decision],
    ["Knockout Category", item.knockout_category],
    ["Knock Pattern", item.knock_pattern],
    ["Agency", item.agency],
    ["Announcement #", item.announcement_number],
    ["Due Date", item.due_date],
    ["HigherGov URL", item.highergov_url],
    ["SAM URL", item.sam_url],
    ["Pipeline Stage", item.pipeline_stage],
    ["Assessment Type", item.assessment_type],
    ["Processing Method", item.processing_method],
    ["Batch Decision", item.batch_decision],
    ["Agent Decision", item.agent_decision],
    ["Place of Performance", item.place_of_performance],
    ["Set Aside", item.set_aside],
    ["NAICS", item.naics],
    ["PSC", item.psc],
  ];

  fields.forEach(([label, value]) => {
    if (!value) return;
    const dt = document.createElement("dt");
    dt.textContent = label;
    const dd = document.createElement("dd");
    if (label.toLowerCase().includes("url")) {
      const link = document.createElement("a");
      link.href = value;
      link.target = "_blank";
      link.rel = "noopener";
      link.textContent = value;
      dd.appendChild(link);
    } else {
      dd.textContent = value;
    }
    detailList.append(dt, dd);
  });

  detailAnalysis.textContent = item.analysis_notes || "(No analysis notes provided.)";

  if (state.fullReportMarkdown) {
    detailReport.textContent = state.fullReportMarkdown;
    detailReportContainer.hidden = false;
  } else {
    detailReportContainer.hidden = true;
  }
}

// Initial state
setStatus("Idle", "idle");
progressCard.classList.add("hidden");
resultsCard.classList.add("hidden");

