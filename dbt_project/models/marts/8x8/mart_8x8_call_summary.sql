-- mart_8x8_call_summary.sql
--
-- Daily call summary aggregated by office (country + PBX), direction,
-- and final disposition. This is the primary 8x8 table exported to Power BI.
--
-- Granularity: one row per (call_date, pbx_id, country, direction, last_leg_disposition)

with calls as (
    select * from {{ ref('stg_8x8_call_detail_records') }}
)

select
    -- ── Dimensions ────────────────────────────────────────────────────────────
    date_trunc('day', started_at)           as call_date,
    pbx_id,
    country,
    direction,
    last_leg_disposition,

    -- ── Volume ────────────────────────────────────────────────────────────────
    count(*)                                as total_calls,
    sum(is_missed::integer)                 as missed_calls,
    sum(is_answered::integer)               as answered_calls,
    sum(is_abandoned::integer)              as abandoned_calls,

    -- ── Duration (seconds) ────────────────────────────────────────────────────
    round(avg(call_duration_seconds), 2)    as avg_call_duration_seconds,
    round(sum(call_duration_seconds), 2)    as total_call_duration_seconds,
    round(avg(talk_duration_seconds), 2)    as avg_talk_duration_seconds,
    round(avg(ring_duration_seconds), 2)    as avg_ring_duration_seconds,
    round(avg(wait_duration_seconds), 2)    as avg_wait_duration_seconds,

    -- ── Call complexity ───────────────────────────────────────────────────────
    round(avg(call_leg_count), 2)           as avg_call_legs

from calls
group by 1, 2, 3, 4, 5
