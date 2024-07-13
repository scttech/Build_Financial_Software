from psycopg.rows import dict_row, class_row

from chapter11.v4.AchParser.ach_processor.database.db_utils import get_db_connection
from chapter12.v4.AchParser.ofac.results.ofac_scan_results import OfacScanResults


class OfacSql:
    def get_scan_results(self) -> list[OfacScanResults]:
        with get_db_connection(row_factory=class_row(OfacScanResults)) as conn:
            result = conn.execute(
                """
WITH ach_ppd_collected_names AS (
    SELECT DISTINCT aped.individual_name,
                    REPLACE(aped.individual_name, ' ', '') as cleaned_individual_name,
                    art1.ach_files_id,
                    art5.ach_records_type_5_id
    FROM ach_files
    INNER JOIN ach_records_type_1 AS art1 USING (ach_files_id)
    INNER JOIN ach_records_type_5 AS art5 USING (ach_records_type_1_id)
    INNER JOIN ach_records_type_6 AS art6 USING (ach_records_type_5_id)
    INNER JOIN ach_ppd_entry_details AS aped USING (ach_records_type_6_id)
    GROUP BY art1.ach_files_id, art5.ach_records_type_5_id, individual_name, cleaned_individual_name
), ach_iat_collected_names AS (
    SELECT DISTINCT aia10d.receiving_name AS individual_name,
                    REPLACE(aia10d.receiving_name, ' ', '') as cleaned_individual_name,
                    art1.ach_files_id,
                    art5.ach_records_type_5_id
    FROM ach_files
    INNER JOIN ach_records_type_1 AS art1 USING (ach_files_id)
    INNER JOIN ach_records_type_5 AS art5 USING (ach_records_type_1_id)
    INNER JOIN ach_records_type_6 AS art6 USING (ach_records_type_5_id)
    INNER JOIN ach_records_type_7 AS art7 USING (ach_records_type_6_id)
    INNER JOIN ach_iat_addenda_10_details AS aia10d USING (ach_records_type_7_id)
    GROUP BY art1.ach_files_id, art5.ach_records_type_5_id, individual_name, cleaned_individual_name
), 
sdn_names AS (
    SELECT
        CONCAT_WS(' ', first_name, middle_name, last_name) AS sdn_name,
        REPLACE(CONCAT(first_name, middle_name, last_name), ' ', '') as cleaned_sdn_name,
        alias,
        REPLACE(alias, ' ', '') as cleaned_sdn_alias
    FROM sdn_list
), computed_similarity_ppd AS (
    SELECT
        ach_files_id,
        ach_records_type_5_id AS ach_batch_id,
        sdn.sdn_name,
        apcn.individual_name,
        alias,
        (1 - (levenshtein(cleaned_individual_name, sdn.cleaned_sdn_name)::float / GREATEST(length(cleaned_individual_name), length(sdn.cleaned_sdn_name)))) * 100 AS similarity_score,
        CASE
           WHEN daitch_mokotoff(cleaned_individual_name) && daitch_mokotoff(sdn.cleaned_sdn_name) THEN TRUE
           ELSE FALSE
        END AS daitch_mokotoff_match_name,
        CASE
           WHEN daitch_mokotoff(cleaned_individual_name) && daitch_mokotoff(sdn.cleaned_sdn_alias) THEN TRUE
           ELSE FALSE
        END AS daitch_mokotoff_match_alias
    FROM ach_ppd_collected_names AS apcn
    CROSS JOIN sdn_names sdn
), computed_similarity_iat AS (
    SELECT
        ach_files_id,
        ach_records_type_5_id AS ach_batch_id,
        sdn.sdn_name,
        aicn.individual_name,
        alias,
        (1 - (levenshtein(cleaned_individual_name, sdn.cleaned_sdn_name)::float / GREATEST(length(cleaned_individual_name), length(sdn.cleaned_sdn_name)))) * 100 AS similarity_score,
        CASE
           WHEN daitch_mokotoff(cleaned_individual_name) && daitch_mokotoff(sdn.cleaned_sdn_name) THEN TRUE
           ELSE FALSE
        END AS daitch_mokotoff_match_name,
        CASE
           WHEN daitch_mokotoff(cleaned_individual_name) && daitch_mokotoff(sdn.cleaned_sdn_alias) THEN TRUE
           ELSE FALSE
        END AS daitch_mokotoff_match_alias
    FROM ach_iat_collected_names aicn
    CROSS JOIN sdn_names sdn    
), computed_similarity AS (
    SELECT * FROM computed_similarity_ppd
    UNION ALL
    SELECT * FROM computed_similarity_iat
)
SELECT ROW_NUMBER() OVER (ORDER BY ach_files_id, ach_batch_id) AS id, *
FROM computed_similarity
WHERE similarity_score >= 80
   OR daitch_mokotoff_match_name = TRUE
    OR daitch_mokotoff_match_alias = TRUE
ORDER BY similarity_score DESC
                """,
                [],
            ).fetchall()

        return result
