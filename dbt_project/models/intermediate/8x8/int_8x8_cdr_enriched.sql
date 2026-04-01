-- int_8x8_cdr_enriched.sql
--
-- Intermediate model: enriches 8x8 CDR with site information.
--
-- Join logic: cdr.pbx_id = site.pbx_id
-- Each CDR row gets the site name for the PBX it belongs to.
--
-- Note: if a PBX has multiple active sites, a row will appear for each.
-- In practice each PBX maps to one site; verify in stg_8x8_pbx_sites if
-- you see unexpected duplicates.

with cdr as (
    select * from {{ ref('stg_8x8_call_detail_records') }}
),

sites as (
    select * from {{ ref('stg_8x8_pbx_sites') }}
),

enriched as (
    select
        -- ── All CDR fields ────────────────────────────────────────────────────
        cdr.call_id,
        cdr.pbx_id,
        cdr.country,
        cdr.sip_call_id,
        cdr.dnis,
        cdr.aa_destination,
        cdr.caller,
        cdr.caller_name,
        cdr.caller_id,
        cdr.callee,
        cdr.callee_name,
        cdr.direction,
        cdr.started_at,
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

        -- ── Site information ──────────────────────────────────────────────────
        s.site_id,
        s.site_name

    from cdr
    left join sites s on cdr.pbx_id = s.pbx_id
)

select * from enriched
