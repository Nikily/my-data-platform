-- stg_8x8_call_detail_records.sql
--
-- Staging model for 8x8 Work Call Detail Records.
--
-- Source: raw_eight_x_eight.call_detail_records (written by dlt)
--         All PBXs (Spain, HK, UK, US) land in this single table.
--         The pbx_id column identifies which PBX each record came from.
--
-- What this model does:
--   1. Renames columns from dlt's snake_case normalisation to clear,
--      self-documenting names.
--   2. Converts UTC epoch milliseconds to proper TIMESTAMP values.
--   3. Derives human-readable duration columns (seconds).
--   4. Joins the pbx_country_mapping seed to add a country column.
--
-- Column name note:
--   dlt normalises camelCase API fields to snake_case:
--     callId          → call_id
--     startTimeUTC    → start_time_utc
--     talkTimeMS      → talk_time_ms

with source as (
    select * from {{ source('raw_eight_x_eight', 'call_detail_records') }}
),

pbx_map as (
    select pbx_id, country from {{ ref('pbx_country_mapping') }}
),

staged as (
    select
        -- ── Identifiers ──────────────────────────────────────────────────────
        s.call_id,
        s.pbx_id,
        s.sip_call_id,
        s.dnis,

        -- ── Geography (from pbx_country_mapping seed) ─────────────────────
        p.country,

        -- ── Parties ──────────────────────────────────────────────────────────
        s.caller,
        s.caller_name,
        s.caller_id,
        s.callee,
        s.callee_name,
        s.direction,

        -- ── Timestamps (converted from epoch ms to TIMESTAMP) ─────────────
        -- epoch_ms() is a DuckDB built-in: converts BIGINT milliseconds → TIMESTAMP
        epoch_ms(s.start_time_utc)         as started_at,
        epoch_ms(s.connect_time_utc)       as connected_at,
        epoch_ms(s.disconnected_time_utc)  as disconnected_at,

        -- Raw local-time strings from the API (include UTC offset, e.g. -0500)
        s.start_time                       as start_time_local,
        s.connect_time                     as connect_time_local,
        s.disconnected_time                as disconnected_time_local,

        -- ── Outcome ──────────────────────────────────────────────────────────
        s.missed,
        s.abandoned,
        s.answered,
        s.last_leg_disposition,
        s.call_leg_count,

        -- ── Durations (converted from milliseconds to seconds) ────────────
        round(s.call_time     / 1000.0, 3) as call_duration_seconds,
        round(s.talk_time_ms  / 1000.0, 3) as talk_duration_seconds,
        round(s.ring_duration / 1000.0, 3) as ring_duration_seconds,
        round(s.wait_time_ms  / 1000.0, 3) as wait_duration_seconds,
        round(s.callee_hold_duration_ms / 1000.0, 3) as callee_hold_duration_seconds,
        round(s.abandoned_time  / 1000.0, 3) as abandoned_duration_seconds,
        round(s.answered_time   / 1000.0, 3) as answered_duration_seconds,

        -- Formatted HH:MM:SS strings as provided by the API
        s.talk_time                        as talk_time_formatted,
        s.callee_hold_duration             as callee_hold_duration_formatted,
        s.wait_time                        as wait_time_formatted,

        -- ── Classification ───────────────────────────────────────────────────
        s.departments,
        s.branches,

        -- ── dlt load metadata ────────────────────────────────────────────────
        s._dlt_load_id,
        s._dlt_id

    from source s
    left join pbx_map p on s.pbx_id = p.pbx_id
)

select * from staged
