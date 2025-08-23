import { OrchestratorAgent } from './agents/OrchestratorAgent';
import { RetrievalAgent } from './agents/RetrievalAgent';
import { IndexerAgent } from './agents/IndexerAgent';
import { AnalysisAgent } from './agents/AnalysisAgent';
import { MonitorAgent } from './agents/MonitorAgent';
import { ExporterAgent } from './agents/ExporterAgent';

const retrieval = new RetrievalAgent();
const indexer = new IndexerAgent();
const analysis = new AnalysisAgent();
const monitor = new MonitorAgent();
const exporter = new ExporterAgent();

const orchestrator = new OrchestratorAgent(
  retrieval,
  indexer,
  analysis,
  monitor,
  exporter
);

async function main() {
  // placeholder entrypoint
  console.log('Orchestrator initialized');
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
