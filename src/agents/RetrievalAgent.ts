import { URLEntry, ProcessedContent } from '../types';

/**
 * RetrievalAgent fetches content from URLs using fetch or puppeteer MCP servers.
 */
export class RetrievalAgent {
  async fetch(url: string): Promise<ProcessedContent> {
    // placeholder implementation
    return {
      id: url,
      url,
      title: url,
      type: 'webpage',
      content: '',
      metadata: {},
      lastProcessed: new Date().toISOString(),
    };
  }
}
