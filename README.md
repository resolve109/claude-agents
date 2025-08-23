# Claude Agents

This project scaffolds a local URL retrieval service using Model Context Protocol (MCP) agents.

It includes skeleton implementations for:

- **OrchestratorAgent** – coordinates sub-agents and enforces policies.
- **RetrievalAgent** – fetches content using Fetch or Puppeteer MCP servers.
- **IndexerAgent** – stores processed content in SQLite with FTS.
- **AnalysisAgent** – performs summarization via Claude Code.
- **MonitorAgent** – watches collections for updates.
- **ExporterAgent** – outputs content in multiple formats.

To build the TypeScript source:

```bash
npm run build
```

Run a type check without emitting JavaScript:

```bash
npm test
```
