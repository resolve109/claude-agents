import { ProcessedContent } from '../types';

/**
 * ExporterAgent produces exports in various formats.
 */
export class ExporterAgent {
  async export(content: ProcessedContent, format: 'json' | 'markdown'): Promise<string> {
    // placeholder export logic
    return JSON.stringify(content);
  }
}
