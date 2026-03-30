-- stg_8x8_call_detail_records.sql
--
-- Staging model for 8x8 Work Call Detail Records.
-- Schema derived from actual API responses (March 2026).
--
-- Source: raw_eight_x_eight.call_detail_records (written by dlt)
--         All PBXs share one table; pbx_id + country identify the office.
--
-- Key type notes (verified against live data):
--   call_leg_count  — API returns a STRING ("1","2","3") → cast to INTEGER
--   answered_time   — epoch ms TIMESTAMP when answered, 0 when not → NULL when 0
--   connect_time_utc / connect_time — 0 / "0" when call never connected → NULL
--   ring_duration   — milliseconds
--   call_time       — milliseconds
--   talk_time_ms    — milliseconds
--   wait_time_ms    — milliseconds
--   departments / branches — LIST type (may be NULL)

with source as (
    select * from {{ source('raw_eight_x_eight', 'call_detail_records') }}
),

pbx_map as (
    select pbx_id, country from {{ ref('pbx_country_mapping') }}
),

-- dlt flattens nested arrays into child tables; re-aggregate them here
departments_agg as (
    select _dlt_root_id, list(value) as departments
    from {{ source('raw_eight_x_eight', 'call_detail_records__departments') }}
    group by _dlt_root_id
),

branches_agg as (
    select _dlt_root_id, list(value) as branches
    from {{ source('raw_eight_x_eight', 'call_detail_records__branches') }}
    group by _dlt_root_id
),

staged as (
    select
        -- ── Identifiers ───────────────────────────────────────────────────────
        s.call_id,
        s.pbx_id,
        p.country,
        s.sip_call_id,
        s.dnis,
        s.aa_destination,

        -- ── Parties ───────────────────────────────────────────────────────────
        s.caller,
        s.caller_name,
        s.caller_id,
        s.callee,
        s.callee_name,
        s.direction,

        -- ── Timestamps ────────────────────────────────────────────────────────
        -- epoch_ms() converts BIGINT milliseconds → TIMESTAMP (DuckDB built-in)
        epoch_ms(s.start_time_utc)                                  as started_at,

        -- connect_time_utc is 0 when the call never connected
        case
            when s.connect_time_utc = 0 then null
            else epoch_ms(s.connect_time_utc)
        end                                                         as connected_at,

        epoch_ms(s.disconnected_time_utc)                           as disconnected_at,

        -- answered_time is an epoch ms timestamp when the call was answered,
        -- and 0 when it was not answered
        case
            when s.answered_time = 0 then null
            else epoch_ms(s.answered_time)
        end                                                         as answered_at,

        -- ── Outcome flags ─────────────────────────────────────────────────────
        s.missed,
        s.abandoned,
        s.answered,
        s.last_leg_disposition,

        -- Boolean convenience columns for easier filtering in Power BI / marts
        s.missed    = 'Missed'   as is_missed,
        s.answered  = 'Answered' as is_answered,
        s.abandoned = 'Abandoned' as is_abandoned,

        -- call_leg_count arrives as a string from the API ("1", "2", "3")
        s.call_leg_count::integer                                   as call_leg_count,

        -- ── Durations in seconds (source is milliseconds) ──────────────────
        round(s.call_time          / 1000.0, 3)                    as call_duration_seconds,
        round(s.talk_time_ms       / 1000.0, 3)                    as talk_duration_seconds,
        round(s.ring_duration      / 1000.0, 3)                    as ring_duration_seconds,
        round(s.wait_time_ms       / 1000.0, 3)                    as wait_duration_seconds,
        round(s.callee_hold_duration_ms / 1000.0, 3)               as callee_hold_duration_seconds,
        round(s.abandoned_time     / 1000.0, 3)                    as abandoned_duration_seconds,

        -- Formatted HH:MM:SS strings as returned by the API
        s.talk_time                                                 as talk_time_formatted,
        s.callee_hold_duration                                      as callee_hold_duration_formatted,
        s.wait_time                                                 as wait_time_formatted,

        -- ── Hold / transfer flags ──────────────────────────────────────────
        s.callee_disconnect_on_hold,
        s.caller_disconnect_on_hold,

        -- ── Classification ────────────────────────────────────────────────
        dept.departments,
        br.branches,

        -- ── dlt metadata ──────────────────────────────────────────────────
        s._dlt_load_id,
        s._dlt_id

    from source s
    left join pbx_map p    on s.pbx_id  = p.pbx_id
    left join departments_agg dept on s._dlt_id = dept._dlt_root_id
    left join branches_agg    br   on s._dlt_id = br._dlt_root_id
)

select * from staged
