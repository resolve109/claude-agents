import { ProcessedContent } from '../types';

/**
 * AnalysisAgent performs semantic analysis using Claude Code.
 */
export class AnalysisAgent {
  async summarize(content: ProcessedContent, query: string): Promise<string> {
    // placeholder summarization
    return `Summary for ${content.url}`;
  }
}
