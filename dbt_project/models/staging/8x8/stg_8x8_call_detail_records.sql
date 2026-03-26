-- stg_8x8_call_detail_records.sql
--
-- Staging model for 8x8 Work Call Detail Records.
--
-- Source: raw_eight_x_eight.call_detail_records (written by dlt)
--
-- What this model does:
--   1. Renames columns from dlt's snake_case normalisation to clear,
--      self-documenting names.
--   2. Converts UTC epoch milliseconds to proper TIMESTAMP values.
--   3. Derives human-readable duration columns (seconds).
--   4. Excludes dlt internal metadata columns (_dlt_load_id, _dlt_id).
--
-- Column name note:
--   dlt normalises camelCase API fields to snake_case:
--     callId          → call_id
--     startTimeUTC    → start_time_utc
--     talkTimeMS      → talk_time_ms
--   The source columns referenced below use these normalised names.

with source as (
    select * from {{ source('raw_eight_x_eight', 'call_detail_records') }}
),

staged as (
    select
        -- ── Identifiers ──────────────────────────────────────────────────────
        call_id,
        pbx_id,
        sip_call_id,
        dnis,

        -- ── Parties ──────────────────────────────────────────────────────────
        caller,
        caller_name,
        caller_id,
        callee,
        callee_name,
        direction,

        -- ── Timestamps (converted from epoch ms to TIMESTAMP) ─────────────
        -- epoch_ms() is a DuckDB built-in: converts BIGINT milliseconds → TIMESTAMP
        epoch_ms(start_time_utc)         as started_at,
        epoch_ms(connect_time_utc)       as connected_at,
        epoch_ms(disconnected_time_utc)  as disconnected_at,

        -- Raw local-time strings from the API (include UTC offset, e.g. -0500)
        start_time                       as start_time_local,
        connect_time                     as connect_time_local,
        disconnected_time                as disconnected_time_local,

        -- ── Outcome ──────────────────────────────────────────────────────────
        missed,
        abandoned,
        answered,
        last_leg_disposition,
        call_leg_count,

        -- ── Durations (converted from milliseconds to seconds) ────────────
        round(call_time     / 1000.0, 3) as call_duration_seconds,
        round(talk_time_ms  / 1000.0, 3) as talk_duration_seconds,
        round(ring_duration / 1000.0, 3) as ring_duration_seconds,
        round(wait_time_ms  / 1000.0, 3) as wait_duration_seconds,
        round(callee_hold_duration_ms / 1000.0, 3) as callee_hold_duration_seconds,
        round(abandoned_time / 1000.0, 3) as abandoned_duration_seconds,
        round(answered_time  / 1000.0, 3) as answered_duration_seconds,

        -- Formatted HH:MM:SS strings as provided by the API
        talk_time                        as talk_time_formatted,
        callee_hold_duration             as callee_hold_duration_formatted,
        wait_time                        as wait_time_formatted,

        -- ── Classification ───────────────────────────────────────────────────
        departments,
        branches,

        -- ── dlt load metadata ────────────────────────────────────────────────
        _dlt_load_id,
        _dlt_id

    from source
)

select * from staged
