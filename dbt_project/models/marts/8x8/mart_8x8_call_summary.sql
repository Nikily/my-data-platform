-- mart_8x8_call_summary.sql
--
-- Daily call summary aggregated by PBX, direction, and disposition.
-- This is the primary 8x8 table exported to Power BI via Parquet.
--
-- Exported by: pipeline/assets/export/parquet_export.py
-- Add 'mart_8x8_call_summary' to MART_TABLES in that file to enable export.

with calls as (
    select * from {{ ref('stg_8x8_call_detail_records') }}
),

summary as (
    select
        date_trunc('day', started_at)               as call_date,
        pbx_id,
        direction,
        last_leg_disposition,

        count(*)                                    as total_calls,
        sum(case when missed   = 'Missed'    then 1 else 0 end) as missed_calls,
        sum(case when answered = 'Answered'  then 1 else 0 end) as answered_calls,

        round(avg(call_duration_seconds), 2)        as avg_call_duration_seconds,
        round(sum(call_duration_seconds), 2)        as total_call_duration_seconds,
        round(avg(ring_duration_seconds), 2)        as avg_ring_duration_seconds,
        round(avg(talk_duration_seconds), 2)        as avg_talk_duration_seconds,
        round(avg(wait_duration_seconds), 2)        as avg_wait_duration_seconds

    from calls
    group by 1, 2, 3, 4
)

select * from summary
