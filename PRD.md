# CrisisBridge AI — Product Requirements Document (PRD)

> **Document status:** As-built / code-derived PRD  
> **Source of truth:** `app.py` + `requirements.txt` supplied for this project  
> **Scope:** This document describes only what is supported by the supplied source files. It does not assume undocumented AI models, APIs, databases, authentication, or external integrations.

## 1. Product Overview

CrisisBridge AI is a Streamlit-based web interface presented as an **Emergency Response Command & Control** dashboard.

The interface is branded around **Autonomous Multi-Agent Humanitarian Orchestration** and visually represents a five-stage emergency-response pipeline.

The current supplied implementation accepts emergency dispatch text and, after the user presses **Run Multi-Agent**, renders a predefined emergency-response dashboard.

**Important implementation fact:** the current code does not actually parse the entered dispatch text or call an LLM/API. The displayed metrics, action plan, extracted entities, and audit information are hard-coded in `app.py`.

## 2. Product Goal

The implemented product is designed to:

- Provide a dark command-center interface for an emergency scenario.
- Display a five-stage agent pipeline.
- Accept an incoming emergency dispatch text.
- Allow the user to trigger the displayed multi-agent workflow.
- Display emergency severity, estimated victims, assigned resources, response SLA, tactical actions, extracted entities, hazards, medical requirements, and an audit-log entry.

## 3. Product / Application Identity

- **Product name:** CrisisBridge AI
- **Interface title:** CrisisBridge AI | Emergency Response Command Center
- **Application framework:** Streamlit
- **Page icon:** 🚨
- **Layout:** Wide
- **Sidebar:** Expanded initially

## 4. User Flow

1. User opens the Streamlit application.
2. Sidebar displays CrisisBridge AI branding and the five pipeline stages in standby/pending state.
3. Main area displays the **Incoming Emergency Dispatch Stream** text area.
4. The text area contains a default emergency scenario and can be edited by the user.
5. User clicks **🚀 Run Multi-Agent**.
6. The application sets `st.session_state["run_pipeline"] = True`.
7. The application reruns using `st.rerun()`.
8. A spinner displays **🔄 Orchestrating multi-agent pipeline...**.
9. The code waits for 0.5 seconds.
10. The dashboard displays the predefined emergency-response information.
11. The sidebar changes the five stages to **Completed** and system status to **All Agents Operational**.

## 5. Agent Pipeline

The sidebar defines the following five stages:

| # | Agent / Stage | Displayed Purpose |
|---|---|---|
| 1 | Intake Agent | Parsing unstructured text & dispatch logs |
| 2 | Analysis Agent | Extracting entities, severity & constraints |
| 3 | Resource-Matching | Mapping needs to available units |
| 4 | Coordinator Agent | Compiling tactical action plan |
| 5 | Follow-up Agent | SLA tracking & audit logs |

### Pipeline State

Before execution:

- Pipeline stages are shown as pending.
- System status is **Standby Mode**.

After execution:

- All five stages are shown as completed.
- System status is **All Agents Operational**.

**Implementation limitation:** there is no separate execution logic for these five agents in the supplied code. The completed state is driven by the single `run_pipeline` session-state value.

## 6. Emergency Dispatch Input

### Input

- **Label:** Incoming Emergency Dispatch Stream
- **Component:** Streamlit text area
- **Height:** 95
- **Help text:** Input raw text feeds from radio transcripts, SOS forms, or panic buttons.

### Default Emergency Scenario

The supplied application contains this default scenario:

> URGENT: Flooding has trapped approximately 45 families in Sector 4, Downtown. Water levels are rising rapidly (currently waist-high). We have 3 elderly individuals requiring immediate medical assistance and insulin supplies. Drinking water is contaminated.

### Important Implementation Limitation

The text is stored in the `sos_input` variable, but the supplied code does not subsequently process that variable.

Therefore, changing the text does **not** dynamically change the dashboard output in the current implementation.

## 7. Execution Trigger

The primary action is:

**🚀 Run Multi-Agent**

When clicked:

- `run_pipeline` is set to `True`.
- `st.rerun()` is called.
- The post-execution dashboard is rendered.

No LLM/API call is made by this action in the supplied source code.

## 8. Execution Dashboard

After execution, four metrics are displayed.

| Metric | Displayed Value | Delta / Status |
|---|---|---|
| Severity Level | Level 1 | Critical Priority |
| Estimated Victims | ~45 Families | Urgent Evacuation |
| Assigned Units | 2 Rescue Boats | + 1 Paramedic Team |
| Response SLA | < 15 Mins | ● On Track |

These values are hard-coded in `app.py`.

## 9. Coordinator Agent Action Plan

The dashboard displays an **Incident Summary & Operational Constraints** section stating:

- Rapid snowmelt / flash flooding has marooned approximately 45 families in Sector 4, Downtown.
- Standard utility and ground transport vehicles are blocked because of waist-high moving water.
- Immediate medical triage is required for 3 vulnerable patients with acute insulin dependency.

### Tactical Execution Steps

1. **Dispatch Marine Units:** Route 2 inflatable rescue watercraft to coordinates `Lat: 34.05, Long: -118.24`.
2. **Medical Payload Mobilization:** Equip paramedic boat with cold-storage emergency insulin kits.
3. **Hospital Alert:** Pre-alert Central Triage Ward 3 for incoming hypothermic / diabetic admissions.
4. **Public Safety Broadcast:** Issue localized SMS evacuation beacon warning against drinking contaminated flood water.

These action-plan contents are hard-coded display content in the supplied application.

## 10. Extracted Entities & Telemetry

The dashboard displays:

### Location Coordinates

**Sector 4, Downtown (34.0500° N, 118.2400° W)**

### Critical Hazards

- Flash Flooding (Waist-High)
- Contaminated Water Source

### Medical Requirements

- 3x Senior Citizens
- Insulin & Warmth Support Required

### Resource Audit Log

`[18:52:04] Unit Alpha-1 assigned & acknowledged dispatch.`

These values are displayed statically by the current code; they are not dynamically extracted from the user-entered dispatch text.

## 11. Session State

The application initializes:

`st.session_state["run_pipeline"] = False`

When the user runs the workflow:

`st.session_state["run_pipeline"] = True`

The supplied application does not implement:

- Database persistence
- Historical incident storage
- Persistent audit logs
- Structured incident records
- External state storage

## 12. UI / Visual Requirements Implemented

The supplied `app.py` includes a custom dark command-center visual design.

### Main Visual Theme

- Dark application background
- Dark sidebar
- High-contrast white/light text
- Cyan metric values
- Blue primary action button
- Pending and completed pipeline states

### Typography

- Inter font
- JetBrains Mono defined for code-style text
- Google Fonts imported through CSS

### Main UI Components

- Sidebar
- Pipeline status cards
- Emergency dispatch text area
- Run Multi-Agent button
- Four metrics
- Coordinator action-plan container
- Extracted entities and telemetry container
- Status/info/error/warning/success UI blocks

## 13. Dependencies

The supplied `requirements.txt` contains:

```text
streamlit>=1.32.0
pandas>=2.0.0
```

### Dependency Usage

- `streamlit` is imported and used by `app.py`.
- `pandas` is declared in `requirements.txt`, but no pandas import or pandas functionality appears in the supplied `app.py`.

The supplied `app.py` also imports Python's built-in `time` module.

## 14. LLM / API Integration Status

Based strictly on the supplied files:

- No OpenAI API integration is present.
- No Gemini API integration is present.
- No Groq API integration is present.
- No Claude API integration is present.
- No LLM SDK dependency is declared in `requirements.txt`.
- No API key configuration is present.
- No external AI model call is present.

Therefore, the current version should be treated as a **Streamlit emergency-response UI/prototype with hard-coded orchestration output**, not as a live LLM-powered multi-agent system.

## 15. External Integrations

The supplied files do not implement integrations with:

- Emergency dispatch systems
- SMS providers
- Hospital systems
- Mapping/GPS services
- Resource-management systems
- Databases
- LLM providers
- Authentication providers

The action-plan text mentions SMS and hospital alerts, but the supplied code only displays those instructions; it does not send them.

## 16. Acceptance Criteria — Current Implementation

The current implementation satisfies the following observable behavior:

- The application opens with the configured CrisisBridge AI title.
- The emergency icon is displayed.
- The layout is wide.
- The sidebar is expanded initially.
- The five named pipeline stages are displayed.
- The emergency dispatch text area is displayed with the supplied default scenario.
- The Run Multi-Agent button is available.
- Clicking Run Multi-Agent changes the session state and reruns the application.
- Four dashboard metrics are displayed after execution.
- The Coordinator Agent action plan is displayed.
- Extracted entities and telemetry are displayed.
- The pipeline stages change to Completed.
- System status changes to All Agents Operational.

## 17. Current Implementation Gaps

| Area | Current Status |
|---|---|
| Actual multi-agent execution | Not implemented; visually represented |
| LLM integration | Not implemented |
| Natural-language parsing | Not implemented |
| Dynamic entity extraction | Not implemented |
| Dynamic severity analysis | Not implemented |
| Dynamic victim estimation | Not implemented |
| Dynamic resource matching | Not implemented |
| Dynamic action-plan generation | Not implemented |
| Live SLA tracking | Not implemented |
| Persistent audit logging | Not implemented |
| Real SMS sending | Not implemented |
| Real hospital alerting | Not implemented |
| Database / persistence | Not implemented |
| Authentication / authorization | Not implemented |
| External dispatch integration | Not implemented |
| Automated tests | Not present in supplied files |

## 18. Source Traceability

This PRD is derived from the two supplied project files:

### `app.py`

Defines:

- Streamlit application configuration
- Custom CSS and visual design
- CrisisBridge AI branding
- Five-stage agent pipeline
- Session-state execution trigger
- Emergency dispatch input
- Dashboard metrics
- Coordinator action plan
- Extracted entities and telemetry
- Static audit-log display

### `requirements.txt`

Defines:

- `streamlit>=1.32.0`
- `pandas>=2.0.0`

## 19. Executive Summary

The supplied **CrisisBridge AI** project is a Streamlit-based emergency-response command-center prototype.

Its current implementation provides a polished emergency-response UI and a visually represented five-stage multi-agent pipeline. The application accepts emergency dispatch text and transitions from standby mode to a response dashboard when the user clicks **Run Multi-Agent**.

However, based strictly on the supplied source files, the current version does **not** contain an LLM API, actual agent orchestration, dynamic NLP processing, resource matching, live SLA tracking, persistent audit logging, or external emergency-response integrations.

The displayed emergency-response results are currently predefined in the application code.
