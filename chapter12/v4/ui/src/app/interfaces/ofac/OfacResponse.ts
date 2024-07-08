
export interface OfacResponse {
  ach_files_id: string;
  ach_batch_id: string;
  sdn_name: string;
  individual_name: string;
  alias: string | null;
  similarity_score: number;
  daitch_mokotoff_match_name: boolean;
  daitch_mokotoff_match_alias: boolean;
}