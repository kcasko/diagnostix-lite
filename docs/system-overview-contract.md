# System Overview Contract

## Purpose

Answer one question: **What is this machine doing right now?**

This page is the entry point. It must always load. It must never error. It is the spine of DiagnOStiX.

---

## Requirements

### Load Behavior

- Loads on launch
- Loads on refresh
- Loads when diagnostics fail
- Loads when dependencies are missing
- Loads in degraded mode if necessary

### Error Handling

- No page-level failures
- Missing data shows as "unavailable" or "—"
- Admin-required data shows access state, not placeholder values
- Unsupported features show platform incompatibility clearly

### Performance

- Sub-second initial render
- Data refresh without full page reload
- Minimal CPU overhead during idle display

---

## Data Contract

### CPU State

**Required:**
- Physical core count
- Logical core count
- Current utilization (%)
- Current frequency (MHz or GHz)

**Optional (if available):**
- Per-core utilization
- Thermal state
- Throttling indicators

**Display rules:**
- Show current state, not average
- Use exact values, not ranges
- Label units explicitly

### Memory State

**Required:**
- Total RAM (GB)
- Used RAM (GB)
- Available RAM (GB)
- Utilization (%)

**Optional (if available):**
- Swap total
- Swap used
- Memory type/speed

**Display rules:**
- Use binary units (GiB) or decimal (GB) consistently
- Show both absolute and percentage
- No color coding based on thresholds

### Disk State

**Required (per disk):**
- Mount point or drive letter
- Total capacity
- Used capacity
- Free capacity
- Utilization (%)
- Filesystem type

**Optional (if available):**
- Disk model
- Partition table type
- SMART status summary

**Display rules:**
- List all mounted volumes
- Exclude virtual/temporary mounts by default
- Show readonly state if applicable
- Use consistent unit scaling per disk

### Network State

**Required (per interface):**
- Interface name
- Status (up/down)
- IP address(es)
- MAC address

**Optional (if available):**
- Link speed
- Bytes sent/received
- Packet errors
- Default gateway
- DNS servers

**Display rules:**
- Show all interfaces, including loopback
- Distinguish physical from virtual
- Show IPv4 and IPv6 separately if both present

### OS and Uptime

**Required:**
- OS name
- OS version
- Kernel/build version
- Architecture
- Hostname
- Current uptime

**Optional (if available):**
- Boot time (timestamp)
- Last update time
- Virtualization detection

**Display rules:**
- Use OS-reported names, not marketing names
- Show uptime in human-readable format (days, hours, minutes)
- Include timezone or UTC offset for timestamps

---

## UI Contract

### Layout

- Single scrollable page
- Sections in fixed order: CPU, Memory, Disk, Network, OS
- No tabs or hidden content
- No expandable/collapsible sections in v1

### Visual Language

- Monospace font for numeric data
- Sans-serif for labels
- Dark background, high-contrast text
- Neon accent color for borders/dividers only
- No status colors (red/yellow/green)

### Text Rules

- Labels: short noun phrases ("Total RAM", not "Total amount of RAM installed")
- Values: number + unit with single space
- State indicators: present tense verb ("running", "down", "throttled")
- No percentages without absolute values shown alongside
- No "healthy", "good", "optimal" labels

### Refresh Behavior

- Auto-refresh interval: 5 seconds (configurable)
- Manual refresh button visible
- Last update timestamp shown
- No spinners or loading animations over data
- Stale data clearly marked if refresh fails

---

## Degradation Rules

### When Python dependencies are missing:
- Show OS, hostname, uptime via shell fallback
- Mark other sections "unavailable - install psutil"

### When running without admin/root:
- Show all non-privileged data
- Mark admin-required fields "requires elevation"

### When running on unsupported OS:
- Attempt to show generic cross-platform data
- Mark OS-specific features "unsupported on [OS]"

### When hardware access is restricted:
- Show software-visible state only
- Do not guess or extrapolate

---

## Non-Requirements

**Not included in System Overview:**

- Historical data or trends
- Comparisons to previous states
- Process lists
- Service status
- Log entries
- Recommendations
- Scores or ratings
- Predictions
- Alarms or alerts

**These belong in dedicated diagnostic pages.**

---

## Success Criteria

A user looking at this page for 10 seconds should be able to answer:
- Is the CPU busy?
- Is memory full?
- Is disk space low?
- Is the network connected?
- What OS is this?
- How long has it been running?

If any of these cannot be answered, the contract is broken.

---

## Implementation Notes

This contract is platform-agnostic. Implementation must:
- Detect platform capabilities at runtime
- Never assume tool availability
- Fail gracefully per section, never globally
- Use psutil as primary data source
- Fall back to subprocess + platform module when psutil insufficient
- Log unavailable data sources for debug, not to user

**This contract is locked. Changes require explicit approval.**
