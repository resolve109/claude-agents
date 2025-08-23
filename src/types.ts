export interface URLCollection {
  name: string;
  description: string;
  urls: URLEntry[];
  lastUpdated: Date;
  tags: string[];
}

export interface URLEntry {
  id: string;
  url: string;
  type: 'pdf' | 'webpage' | 'github' | 'documentation';
  title: string;
  description?: string;
  category?: string;
  lastFetched?: Date;
  contentHash?: string;
}

export interface ProcessedContent {
  id: string;
  url: string;
  title: string;
  type: string;
  collection?: string;
  content: string;
  metadata: Record<string, unknown>;
  lastProcessed: string;
}
