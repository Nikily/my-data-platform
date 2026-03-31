-- stg_8x8_users.sql
--
-- Staging model for 8x8 users from the Admin Provisioning API.
-- Produces one row per user-extension combination so it can be joined
-- directly against call detail records on extension number.
--
-- Source tables (written by dlt, full replace each run):
--   raw_eight_x_eight.users                            — one row per user
--   raw_eight_x_eight.users__service_info__extensions  — one row per extension

with users as (
    select * from {{ source('raw_eight_x_eight', 'users') }}
),

extensions as (
    select * from {{ source('raw_eight_x_eight', 'users__service_info__extensions') }}
),

staged as (
    select
        -- ── Identity ──────────────────────────────────────────────────────────
        u.basic_info__user_id                   as user_id,
        u.basic_info__user_name                 as user_name,
        u.basic_info__first_name                as first_name,
        u.basic_info__last_name                 as last_name,
        u.basic_info__status                    as status,
        u.basic_info__primary_email             as primary_email,
        u.basic_info__locale                    as locale,
        u.basic_info__timezone                  as timezone,

        -- ── Site ──────────────────────────────────────────────────────────────
        u.basic_info__site__id                  as site_id,
        u.basic_info__site__name                as site_name,
        u.basic_info__site__pbx_name            as site_pbx_name,

        -- ── Directory ─────────────────────────────────────────────────────────
        u.directory_info__department            as department,
        u.directory_info__job_title             as job_title,

        -- ── Extension (join key against CDR callee / caller) ──────────────────
        e.extension_number,
        e.fq_extension_number,
        e.primary_phone_number,

        -- ── dlt metadata ──────────────────────────────────────────────────────
        u._dlt_id,
        u._dlt_load_id

    from users u
    left join extensions e on u._dlt_id = e._dlt_root_id
)

select * from staged
