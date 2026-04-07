-- int_8x8_cdr_enriched.sql
--
-- Intermediate model: enriches 8x8 CDR with site information.
--
-- Site name is derived directly from the `branches` array on each CDR row
-- (populated by dlt from the call_detail_records__branches child table).
-- The first element of the array is the site name for the call.

with cdr as (
    select * from {{ ref('stg_8x8_call_detail_records') }}
),

enriched as (
    select
        -- ── All CDR fields ────────────────────────────────────────────────────
        cdr.call_id,
        cdr.pbx_id,
        cdr.country,
        cdr.sip_call_id,
        cdr.dnis,
        cdr.started_at_local::date as "date", 
        cdr.aa_destination,
        cdr.caller,
        cdr.caller_name,
        cdr.caller_id,
        cdr.callee,
        cdr.callee_name,
        cdr.direction,
        cdr.started_at,
        cdr.started_at_local,
        cdr.connected_at,
        cdr.disconnected_at,
        cdr.answered_at,
        cdr.missed,
        cdr.abandoned,
        cdr.answered,
        cdr.last_leg_disposition,
        cdr.is_missed,
        cdr.is_answered,
        cdr.is_abandoned,
        case 
	        when cdr.answered != '-' and cdr.answered not null then 'Answered'
	        when cdr.missed != '-' and cdr.missed not null then 'Missed'
        end as type,
        cdr.call_leg_count,
        cdr.call_duration_seconds,
        cdr.talk_duration_seconds,
        cdr.ring_duration_seconds,
        cdr.wait_duration_seconds,
        cdr.callee_hold_duration_seconds,
        cdr.abandoned_duration_seconds,
        cdr.talk_time_formatted,
        cdr.callee_hold_duration_formatted,
        cdr.wait_time_formatted,
        cdr.callee_disconnect_on_hold,
        cdr.caller_disconnect_on_hold,
        cdr.departments,
        cdr.branches,

        -- ── Site ──────────────────────────────────────────────────────────────
        -- branches is a VARCHAR[] from the dlt child table; first element = site name
        cdr.branches[1]     as site_name,
        Left(regexp_extract(cdr.branches[1], '^(.+?)\s-'),-2) as short_site_name

    from cdr
)

select * from enriched
