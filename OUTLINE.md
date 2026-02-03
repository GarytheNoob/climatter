# Project Outline: counting-days

## 1. Overview

- Terminal-based countdown/countup application for specific dates
- Provides both command-line (CLI) and terminal user interface (TUI) modes
- Supports local and remote JSON data sources for events grouped by tags
- Focus on daily terminal usage (e.g., shell startup messages)

## 2. Core Concepts

### 2.1 Events

- Represent a single dated item
- Fields (from JSON):
  - `type`: fixed value `"event"`
  - `name`: human-readable event title (e.g., `"Alice's Birthday"`)
  - `date`: event date in `YYYY-MM-DD` format
- Derived values at runtime:
  - Number of days until the event (for future dates)
  - Number of days since the event (for past dates)
  - Whether the event is today

### 2.2 Tags

- Logical groupings of events
- Fields (from JSON):
  - `type`: fixed value `"tag"`
  - `name`: tag label (e.g., `"Friends' Birthdays"`, `"Holidays"`)
  - `color`: tag display color name (e.g., `"cyan"`, `"green"`)
  - `content`: array of `event` objects
- Used for:
  - Visual grouping in TUI and CLI output
  - Color-coding sections
  - Filtering and searching

### 2.3 Time and Counting Rules

- All calculations use local system time
- Counting happens at runtime (no precomputed values stored in JSON)
- Outputs days difference as whole days (implementation detail left to code)
- Supports both countdown (future) and countup (past) semantics

## 3. Data Sources

### 3.1 Local Source

- JSON file located on local filesystem
- Must conform to expected array-of-tags structure shown in DESIGN.md
- Loaded on demand for each run

### 3.2 Remote Source

- JSON fetched from remote location (e.g., HTTP endpoint)
- Same schema as local JSON
- May require basic error handling for network failures or invalid data

### 3.3 Data Validation and Normalization

- Validate `type` fields for `tag` and `event`
- Ensure `date` values follow `YYYY-MM-DD` and are parseable
- Handle invalid or missing `color`, `name`, or `content` fields gracefully
- Normalize colors to internal representation (for terminal output)

## 4. Backend Responsibilities

- Abstract access to both local and remote JSON sources
- Parse and build in-memory representation of tags and events
- Provide utility functions:
  - Compute days until/since a given date
  - Determine if event is today
  - Filter and search events by name, date, or tag
  - Mark events as important/favorite (for TUI and possibly persisted state)
- Provide results in a form easily consumed by both CLI and TUI layers

## 5. CLI Mode

### 5.1 Invocation Styles

- Run as a one-off script to print results
- Integrate into shell configuration to run automatically at terminal startup
- Accept parameters to control behavior and queries

### 5.2 Core Behaviors

- When run without special options:
  - Load configured sources
  - Identify events relevant to today (e.g., happening today or near today)
  - Display those events in a concise format
- When run with query parameters:
  - List all events
  - Filter by tag name
  - Search by event name or partial match
  - Show upcoming events within a specified window

### 5.3 Example CLI Use Cases

- Show today's birthdays and holidays
- List all events under a tag (e.g., `Friends' Birthdays`)
- Query next N upcoming events across all tags

### 5.4 Shell Startup Integration

- Designed to be called from shell configuration (e.g., `.bashrc`, `.zshrc`)
- Prints countdowns/countups when a new terminal session starts

### 5.5 Optional Caching Mechanism

- Purpose:
  - Avoid printing the same content on every terminal startup within a period
- Characteristics:
  - Cache lifetime typically one day (configurable at implementation time)
  - Cache key likely tied to current date and configuration
  - Stores pre-rendered output or computed data for reuse
- Behavior:
  - On startup, check cache
  - If valid cache exists, reuse cached output
  - If not, compute fresh output and update cache

## 6. TUI Mode

### 6.1 General Behavior

- Full-screen terminal user interface launched by a command
- Presents tag and event information interactively
- Uses keyboard input for navigation and actions

### 6.2 Layout and Display

- Shows all tags and their events
- Color-codes tags according to their `color` field
- For each event, displays:
  - Event name
  - Event date
  - Number of days until or since the event date
- May separate future and past events visually (implementation detail)

### 6.3 Navigation

- Keyboard-based navigation between:
  - Tags list
  - Events within a selected tag
- Likely supports:
  - Up/down movement
  - Page or section navigation
  - Switching focus between tag pane and event pane

### 6.4 Searching and Filtering

- Search interface for quickly finding specific events
- Possible capabilities (within scope of DESIGN.md):
  - Filter by tag name
  - Filter by event name substring
  - Combined filtering (tag + text search)

### 6.5 Event Importance and Favorites

- Ability to mark events as important or favorite from within the TUI
- Visual indication of important/favorite events (e.g., highlight or icon)
- Should integrate with filtering/sorting (e.g., show favorites first)

### 6.6 Event Management

- CRUD operations from TUI:
  - Add new events
  - Edit existing events (name and date at minimum)
  - Delete events
- Changes may:
  - Update in-memory model immediately
  - Optionally persist to underlying data source (implementation detail)

## 7. Time Handling

- Use local system timezone for all computations
- Recompute days differences at runtime whenever needed
- No reliance on precomputed or persisted countdown values

## 8. Error Handling and Edge Cases

- Handle missing or malformed JSON data
- Handle unreachable remote sources
- Protect against invalid dates or out-of-range values
- Gracefully degrade when colors or tags are missing

## 9. Extensibility Considerations

- Potential to add:
  - Additional source types (e.g., database, calendar integrations)
  - More advanced recurrence rules for events
  - Custom formatting and localization of date/days output
- Should keep backend abstractions independent of UI (CLI/TUI)
