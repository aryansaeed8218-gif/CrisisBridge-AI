# PRD — CrisisBridge AI

## 1. Product Overview

**Product name:** CrisisBridge AI  
**Current application type:** Streamlit web application  
**Primary purpose:** Provide an emergency-response command-center interface that accepts an unstructured emergency dispatch message and uses Google Gemini to produce a structured tactical breakdown.

The current UI presents the product as an **“Autonomous Multi-Agent Humanitarian Orchestration”** platform and visually represents a five-stage agent pipeline:

1. Intake Agent
2. Analysis Agent
3. Resource-Matching
4. Coordinator Agent
5. Follow-up Agent

However, the current implementation does **not** contain five independently implemented agent components. The runtime LLM operation is a single Gemini model invocation with one prompt. The five pipeline stages are currently a UI/status representation rather than separately executed agents.

---

## 2. Source of Truth and Scope

This PRD is derived strictly from the supplied:

- `app.py` — 331 lines containing the current application implementation.
- `requirements.txt` — two declared Python dependencies.

The PRD describes the **current implemented product**, not an assumed future architecture.

### Dependency baseline

`requirements.txt` currently declares:

- `streamlit>=1.32.0`
- `pandas>=2.0.0`

The current `app.py` directly imports Streamlit, Google Generative AI, and Google API Core. Google AI dependencies are therefore used by the application but are not explicitly declared in the supplied `requirements.txt`.

---

## 3. Problem Statement

Emergency dispatch information may arrive as unstructured text containing multiple operational facts at once, such as:

- affected population
- location
- urgency/severity
- medical requirements
- environmental hazards
- resource requirements

The application is intended to turn such an incoming dispatch stream into a concise, structured tactical response view for an emergency-response operator.

---

## 4. Target User

The implemented interface is designed for an emergency-response / humanitarian operations user who needs to:

- enter or receive an emergency dispatch message,
- trigger AI analysis,
- view an operational summary,
- inspect extracted location/hazard/medical information,
- see an apparent agent-pipeline status.

The code does not implement authentication, user roles, operator profiles, or organization-specific permissions.

---

## 5. Primary User Journey

### Step 1 — Open application

The Streamlit application opens as a wide-layout dark command-center interface titled:

**“CrisisBridge AI | Emergency Response Command Center”**

### Step 2 — Configure Gemini API access

The application first checks Streamlit secrets for `GEMINI_API_KEY`.

If the key is not present in secrets, the sidebar provides a password-style input for the operator to enter the Gemini API key.

If no API key is available and the operator attempts execution, the application displays:

**“Please provide your Gemini API key.”**

### Step 3 — Review/edit incoming dispatch

The main screen provides a text area labeled:

**“Incoming Emergency Dispatch Stream”**

It is pre-populated with a flood emergency scenario involving approximately 45 families, three elderly people needing medical assistance and insulin, rapidly rising waist-high water, and contaminated drinking water.

The input can be edited before execution.

### Step 4 — Run AI analysis

The operator clicks:

**“🚀 Run Multi-Agent”**

The application then:

1. Sets `run_pipeline` to `True`.
2. Shows a processing spinner.
3. Instantiates a Gemini generative model.
4. Sends the dispatch text in a single structured prompt.
5. Stores the returned response text in Streamlit session state.
6. Reruns the application to render the execution dashboard.

### Step 5 — View execution dashboard

After execution, the UI displays:

- Severity Level
- Estimated Victims
- Assigned Units
- Response SLA
- Gemini-generated synthesis
- Location coordinates
- Critical hazards
- Medical requirements
- Resource audit log

---

## 6. Functional Requirements

### FR-01 — Emergency dispatch input

The system shall provide a text input area for unstructured emergency dispatch information.

**Current implementation:**

- Streamlit `st.text_area`
- Label: `Incoming Emergency Dispatch Stream`
- Height: 95 pixels
- Editable by the user
- Includes help text explaining that input may represent radio transcripts, SOS forms, or panic-button feeds.

### FR-02 — Gemini API configuration

The system shall support a Gemini API key through:

1. Streamlit secrets using `GEMINI_API_KEY`, or
2. A sidebar password input when the secret is unavailable.

### FR-03 — Gemini model invocation

On execution, the system shall instantiate:

`gemini-3.8-flash`

and invoke `generate_content()` using a prompt containing the entered dispatch message.

### FR-04 — Structured AI analysis request

The current prompt requests a concise tactical breakdown containing:

1. Severity Level
2. Estimated Victims
3. Assigned Units needed
4. Action Plan steps
5. Extracted Coordinates & Hazards

The current implementation stores the response as raw text and renders it with Streamlit.

### FR-05 — Execution state

The system shall maintain session state for:

- `run_pipeline`
- `ai_response`

Initial values are:

- `run_pipeline = False`
- `ai_response = ""`

### FR-06 — Pipeline visualization

The sidebar shall display five pipeline stages:

| Stage | Current displayed purpose |
|---|---|
| Intake Agent | Parsing unstructured text & dispatch logs |
| Analysis Agent | Extracting entities, severity & constraints |
| Resource-Matching | Mapping needs to available units |
| Coordinator Agent | Compiling tactical action plan |
| Follow-up Agent | SLA tracking & audit logs |

Before execution, stages appear as pending.

After `run_pipeline` becomes true, all five are displayed as completed.

**Important implementation constraint:** the current code does not execute each stage independently.

### FR-07 — System status

Before execution, the sidebar displays:

**Standby Mode**

After execution, it displays:

**All Agents Operational**

This status is driven by the boolean `run_pipeline` state.

### FR-08 — Execution metrics

After execution, the dashboard displays four metrics:

- Severity Level: `Level 1`
- Estimated Victims: `~45 Families`
- Assigned Units: `2 Rescue Boats` with `+ 1 Paramedic Team`
- Response SLA: `< 15 Mins` with `● On Track`

These values are currently hard-coded in the UI and are not populated from the Gemini response.

### FR-09 — Gemini synthesis display

The coordinator section shall display the stored Gemini response under:

**“Live Gemini Multi-Agent Synthesis”**

If no response text is available, it displays a processing message.

### FR-10 — Telemetry and extracted information panel

The right-hand dashboard panel shall display:

**Location Coordinates**

`Sector 4, Downtown (34.0500° N, 118.2400° W)`

**Critical Hazards**

`Flash Flooding (Waist-High), Contaminated Water Source`

**Medical Requirements**

`3x Senior Citizens – Insulin & Warmth Support Required`

**Resource Audit Log**

`[18:52:04] Unit Alpha-1 assigned & acknowledged dispatch.`

These values are currently hard-coded and are not extracted dynamically from the Gemini response.

### FR-11 — Error handling

If Gemini execution raises an exception, the system shall store:

`API Error: <exception>`

as the AI response.

The current code does not provide separate structured error categories or retry logic.

---

## 7. User Interface Requirements

### 7.1 Overall visual design

The interface uses a dark command-center visual language.

Key characteristics include:

- dark navy application background,
- white/light typography,
- blue action buttons,
- cyan metric emphasis,
- green completed-agent indicators,
- sidebar-based pipeline status,
- wide desktop-oriented layout.

### 7.2 Page configuration

The Streamlit page is configured with:

- page title: `CrisisBridge AI | Emergency Response Command Center`
- page icon: `🚨`
- layout: `wide`
- initial sidebar state: `expanded`

### 7.3 Main sections

The interface contains:

1. Sidebar branding and agent pipeline
2. Emergency dispatch input
3. Run Multi-Agent action
4. Execution metrics
5. Coordinator Agent Action Plan
6. Extracted Entities & Telemetry
7. Pre-execution informational state

### 7.4 Typography

The CSS imports:

- Inter
- JetBrains Mono

The latter is used for code-font styling.

---

## 8. AI / LLM Requirements

### 8.1 Provider

Google Generative AI / Gemini.

The code imports:

- `google.generativeai`
- `google.api_core.client_options.ClientOptions`

### 8.2 Endpoint configuration

The code configures the Gemini client with:

`generativelanguage.googleapis.com`

### 8.3 Current AI architecture

The current runtime path is:

**Dispatch text → Prompt construction → Gemini model → Raw response text → Streamlit dashboard**

There is no implemented orchestration layer that passes structured output from one independently executed agent to another.

### 8.4 Prompt contract

The model is instructed to behave as CrisisBridge AI and return a concise tactical breakdown covering:

- severity,
- victims,
- assigned units,
- action plan,
- coordinates/hazards.

The dispatch text is interpolated directly into the prompt.

### 8.5 Output handling

The application uses:

`response.text`

and stores it as a string.

There is no JSON schema, typed response model, parser, validation layer, or structured database record in the supplied implementation.

---

## 9. Data Requirements

### Input data

Primary input is free-form emergency dispatch text.

The current application does not define a formal schema for:

- incident ID,
- timestamp,
- geographic coordinates,
- casualty count,
- resource inventory,
- responder identity,
- SLA metadata.

### Output data

The AI response is stored as a plain text string.

Dashboard telemetry shown alongside it is partly hard-coded.

### Persistence

No external database, file store, cache, or persistent incident store is implemented.

Streamlit session state is used for the current application session.

---

## 10. Multi-Agent Requirements — Current State

The product presentation defines five conceptual agents:

### 10.1 Intake Agent

Displayed responsibility:

**Parsing unstructured text & dispatch logs**

No separate implementation exists in the supplied `app.py`.

### 10.2 Analysis Agent

Displayed responsibility:

**Extracting entities, severity & constraints**

No separate implementation exists in the supplied `app.py`.

### 10.3 Resource-Matching Agent

Displayed responsibility:

**Mapping needs to available units**

No resource database, matching algorithm, or separate agent implementation exists in the supplied `app.py`.

### 10.4 Coordinator Agent

Displayed responsibility:

**Compiling tactical action plan**

The UI labels the Gemini response as the coordinator synthesis, but the underlying code uses the same single Gemini invocation rather than a separately implemented coordinator agent.

### 10.5 Follow-up Agent

Displayed responsibility:

**SLA tracking & audit logs**

The current application displays a static audit-log message and static SLA metric. No background follow-up process, scheduler, event listener, or persistent SLA tracker is implemented.

---

## 11. Security Requirements — Current Implementation

The application accepts a Gemini API key through Streamlit secrets or a password-style sidebar input.

The code does not implement:

- authentication,
- authorization,
- role-based access control,
- audit authentication,
- encryption configuration,
- secret rotation,
- user management,
- incident-level access control.

The PRD therefore does not claim these capabilities.

---

## 12. Reliability and Error Handling

Current behavior includes a `try/except` around Gemini model execution.

On exception, the application stores an API error message in `ai_response`.

The current implementation does not include:

- retries,
- exponential backoff,
- timeout configuration,
- circuit breakers,
- model fallback,
- structured error reporting,
- partial-agent recovery.

---

## 13. Performance Requirements — Source-Supported

The application uses a Streamlit spinner while the Gemini request is running.

No explicit latency, throughput, concurrency, or availability targets are defined in the supplied source files.

The UI displays a `< 15 Mins` response SLA, but this is a dashboard value for the scenario and is not implemented as an application-level performance guarantee.

---

## 14. Dependencies

Declared in `requirements.txt`:

```text
streamlit>=1.32.0
pandas>=2.0.0
```

Direct imports visible in `app.py` additionally include:

```text
time
google.api_core.client_options
google.generativeai
streamlit
```

`time` is imported but not used in the supplied implementation.

`pandas` is declared in `requirements.txt` but is not imported or used in the supplied `app.py`.

---

## 15. Configuration Requirements

The application expects a Gemini API key named:

`GEMINI_API_KEY`

It may be supplied through Streamlit secrets.

If absent, the application exposes an input field in the sidebar.

No other environment variables or application configuration files are referenced by the supplied source.

---

## 16. Example / Default Scenario

The default dispatch scenario represents a flood emergency with:

- approximately 45 affected families,
- Sector 4, Downtown,
- rapidly rising waist-high water,
- three elderly individuals requiring medical assistance,
- insulin requirements,
- contaminated drinking water.

The dashboard subsequently displays fixed example telemetry corresponding to this scenario.

---

## 17. Non-Functional Requirements Evidenced by the Current Code

### NFR-01 — Responsive desktop layout

The application uses Streamlit's wide layout and column-based dashboard design.

### NFR-02 — Operational visual clarity

The UI emphasizes status, severity, metrics, hazards, and action-plan content.

### NFR-03 — Immediate operator feedback

The run action provides a spinner while Gemini processing occurs.

### NFR-04 — Session-level state

Execution state and the current AI response persist in Streamlit session state across the application rerun.

No broader persistence requirement is implemented.

---

## 18. Current Limitations / Gaps

The following are directly observable limitations of the supplied implementation:

1. **Five agents are represented visually but are not independently implemented.**
2. **Only one Gemini model call performs the AI analysis.**
3. **Dashboard metrics are hard-coded.**
4. **Location coordinates are hard-coded.**
5. **Hazard information is hard-coded.**
6. **Medical requirements are hard-coded.**
7. **The resource audit log is hard-coded.**
8. **The displayed SLA is hard-coded and is not an actual tracking mechanism.**
9. **There is no resource inventory or resource-matching backend.**
10. **There is no persistent incident database.**
11. **There is no structured AI output schema.**
12. **There is no authentication or authorization layer.**
13. **There is no retry/fallback mechanism for Gemini failures.**
14. **Google AI dependencies are not explicitly listed in the supplied `requirements.txt`.**
15. **`pandas` is declared but unused by the supplied `app.py`.**
16. **`time` is imported but unused.**

These are implementation observations, not proposed defects beyond what can be established from the supplied files.

---

## 19. Acceptance Criteria for the Current Product

A build matching the supplied source should satisfy the following:

### AC-01
Opening the application renders the CrisisBridge AI emergency command-center interface in a wide layout with an expanded sidebar.

### AC-02
The sidebar contains the five named pipeline stages.

### AC-03
The main area contains an editable emergency dispatch text area.

### AC-04
A user with a valid Gemini API key can trigger the Gemini analysis flow.

### AC-05
The Gemini response is displayed in the coordinator synthesis area.

### AC-06
After execution, the four dashboard metrics are displayed with the currently coded values.

### AC-07
After execution, the telemetry panel displays the currently coded location, hazards, medical requirements, and audit log.

### AC-08
When no Gemini API key is available, the application prompts the user to provide one.

### AC-09
Gemini execution exceptions are surfaced in the stored AI response as an API error.

---

## 20. Future Product Direction (Not Currently Implemented)

The source files do not define a future roadmap. If the product is subsequently evolved into a true multi-agent emergency-response platform, the following areas would need explicit product and technical specifications rather than being assumed to exist today:

- independently executable agent contracts,
- structured inter-agent messages,
- validated incident schemas,
- live resource inventory,
- deterministic resource matching,
- real SLA timers,
- persistent audit/event logs,
- structured Gemini outputs,
- human approval gates,
- authentication and authorization,
- incident history,
- observability and monitoring,
- retry and fallback behavior,
- explicit safety controls for emergency recommendations.

These are **future considerations only** and are not part of the currently implemented feature set.

---

## 21. Product Definition Summary

CrisisBridge AI, as currently implemented, is a **Streamlit-based emergency dispatch analysis dashboard** that presents a five-stage multi-agent concept while using a single Gemini generative-model call to analyze an operator-provided dispatch message.

Its current functional core is:

**Emergency dispatch text → Gemini tactical analysis → session-stored response → command-center dashboard**

The surrounding pipeline indicators, metrics, telemetry, SLA, and audit information provide the current command-center presentation, with several of those values implemented as static UI content rather than dynamically computed application data.
