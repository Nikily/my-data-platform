-- int_8x8_cdr_enriched.sql
--
-- Intermediate model: enriches 8x8 CDR with user and site information.
--
-- Join logic:
--   Incoming calls  → callee  = user extension number (the agent who received)
--   Outgoing calls  → caller  = user extension number (the agent who dialled)
--
-- Result: one row per call leg with the internal agent's profile and site
-- attached. External caller/callee data (where no extension match exists)
-- is preserved from CDR; agent columns will be NULL for those rows.

with cdr as (
    select * from {{ ref('stg_8x8_call_detail_records') }}
),

users as (
    select * from {{ ref('stg_8x8_users') }}
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

        -- ── Agent (internal party) identity ───────────────────────────────────
        u.user_id                               as agent_user_id,
        u.user_name                             as agent_user_name,
        u.first_name                            as agent_first_name,
        u.last_name                             as agent_last_name,
        u.primary_email                         as agent_email,
        u.department                            as agent_department,
        u.job_title                             as agent_job_title,
        u.extension_number                      as agent_extension,
        u.primary_phone_number                  as agent_phone_number,

        -- ── Agent site information ────────────────────────────────────────────
        u.site_id                               as agent_site_id,
        u.site_name                             as agent_site_name,
        u.site_pbx_name                         as agent_site_pbx_name

    from cdr
    left join users u on (
        (cdr.direction = 'Incoming' and cdr.callee = u.extension_number)
        or (cdr.direction = 'Outgoing' and cdr.caller = u.extension_number)
    )
)

select * from enriched
