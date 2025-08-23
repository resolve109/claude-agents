import { RetrievalAgent } from './RetrievalAgent';
import { IndexerAgent } from './IndexerAgent';
import { AnalysisAgent } from './AnalysisAgent';
import { MonitorAgent } from './MonitorAgent';
import { ExporterAgent } from './ExporterAgent';
import { URLCollection, URLEntry } from '../types';

/**
 * OrchestratorAgent coordinates the workflow across sub-agents
 * and enforces policy compliance.
 */
export class OrchestratorAgent {
  constructor(
    private retrieval: RetrievalAgent,
    private indexer: IndexerAgent,
    private analysis: AnalysisAgent,
    private monitor: MonitorAgent,
    private exporter: ExporterAgent
  ) {}

  async addUrls(collection: URLCollection, urls: URLEntry[]): Promise<void> {
    // stub for URL management
  }

  async fetchAndIndex(url: string): Promise<void> {
    const content = await this.retrieval.fetch(url);
    await this.indexer.index(content);
  }
}
