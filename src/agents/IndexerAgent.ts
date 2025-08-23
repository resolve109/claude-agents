import { ProcessedContent } from '../types';

/**
 * IndexerAgent stores processed content into SQLite with FTS capabilities.
 */
export class IndexerAgent {
  async index(content: ProcessedContent): Promise<void> {
    // placeholder for SQLite persistence
    console.log(`Indexing content for ${content.url}`);
  }
}
