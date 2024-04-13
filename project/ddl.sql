-- reset the database
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;

-- create composite data types
DO $$ BEGIN
CREATE TYPE card AS (
    time                interval,
    type                varchar(20),
    reason              varchar(20),
    period              integer
);
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
CREATE TYPE position AS (
    name                varchar(25),
    "from"              interval,
    "to"                interval,
    from_period         integer,
    to_period           integer,
    start_reason        varchar(35),
    end_reason          varchar(35)
);
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
-- a lineup data type for events 35 and 36
CREATE TYPE lineup AS (
    player_id               integer, -- REFERENCES players
    position                varchar(25),
    jersey_number           int
);
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;


-- create tables

CREATE TABLE IF NOT EXISTS referees (
    referee_id          integer PRIMARY KEY,
    name                varchar(50),
    country             varchar(35)
);


CREATE TABLE IF NOT EXISTS stadiums (
    stadium_id          integer PRIMARY KEY,
    name                varchar(50),
    country             varchar(35)
);


CREATE TABLE IF NOT EXISTS managers (
    manager_id          integer PRIMARY KEY,
    name                varchar(50),
    nickname            varchar(50),
    dob                 date,
    country             varchar(35)
);


CREATE TABLE IF NOT EXISTS teams (
    team_id             integer PRIMARY KEY,
    name                varchar(50),
    gender              varchar(6),
    country             varchar(35)
);


CREATE TABLE IF NOT EXISTS competitions (
    competition_id      int PRIMARY KEY,
    country             varchar(35),
    name                varchar(50),
    gender              varchar(6),
    youth               boolean,
    international       boolean
);


CREATE TABLE IF NOT EXISTS matches (
    match_id                    integer PRIMARY KEY,
    match_date                        date,
    kick_off                     time, -- game start time
    competition_id              integer REFERENCES competitions (competition_id) ON DELETE CASCADE,
    season                      char(9), -- yyyy/yyyy
    home_team_id                integer REFERENCES teams (team_id) ON DELETE CASCADE,
    away_team_id                integer REFERENCES teams (team_id) ON DELETE CASCADE,
    home_score                  integer,
    away_score                  integer,
    match_week                  integer,
    competition_stage_name      varchar(40),
    stadium_id                  integer REFERENCES stadiums (stadium_id) ON DELETE CASCADE,
    referee_id                  integer REFERENCES referees (referee_id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS managers_by_team_and_match (
    match_id        integer REFERENCES matches (match_id) ON DELETE CASCADE,
    team_id         integer REFERENCES teams (team_id) ON DELETE CASCADE,
    manager_id      integer REFERENCES managers (manager_id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS players (
    player_id           integer PRIMARY KEY,
    name                varchar(50),
    nickname            varchar(50),
    country             varchar(35)
);



CREATE TABLE IF NOT EXISTS lineups (
    match_id            integer REFERENCES matches (match_id) ON DELETE CASCADE,
    team_id             integer REFERENCES teams (team_id) ON DELETE CASCADE,
    player_id           integer REFERENCES players (player_id) ON DELETE CASCADE,
    cards               card[],
    positions           "position"[],
    jersey_number       integer
);


-- one table per event type, which lists match/player/team info, plus event specific info

-- 50/50
CREATE TABLE IF NOT EXISTS event_33 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches (match_id) ON DELETE CASCADE,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams (team_id) ON DELETE CASCADE,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams (team_id) ON DELETE CASCADE,
    player_id               integer REFERENCES players (player_id) ON DELETE CASCADE,
    position                varchar(25),
    location                point,
    under_pressure          boolean,
    out                     boolean,
    outcome                 varchar(20),
    counterpress            boolean
);


-- Bad Behaviour
CREATE TABLE IF NOT EXISTS event_24 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches (match_id) ON DELETE CASCADE,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams (team_id) ON DELETE CASCADE,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams (team_id) ON DELETE CASCADE,
    player_id               integer REFERENCES players (player_id) ON DELETE CASCADE,
    position                varchar(25),
    off_camera              boolean,
    card                    varchar(20)
);


-- Ball Receipt
CREATE TABLE IF NOT EXISTS event_42 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches (match_id) ON DELETE CASCADE,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams (team_id) ON DELETE CASCADE,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams (team_id) ON DELETE CASCADE,
    player_id               integer REFERENCES players (player_id) ON DELETE CASCADE,
    position                varchar(25),
    location                point,
    under_pressure          boolean,
    outcome                 varchar(20)
);


-- Ball Recovery
CREATE TABLE IF NOT EXISTS event_2 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches (match_id) ON DELETE CASCADE,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams (team_id) ON DELETE CASCADE,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams (team_id) ON DELETE CASCADE,
    player_id               integer REFERENCES players (player_id) ON DELETE CASCADE,
    position                varchar(25),
    location                point,
    under_pressure          boolean,
    off_camera              boolean,
    out                     boolean,
    offensive               boolean,
    recovery_failure        boolean
);


-- Block
CREATE TABLE IF NOT EXISTS event_6 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches (match_id) ON DELETE CASCADE,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams (team_id) ON DELETE CASCADE,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams (team_id) ON DELETE CASCADE,
    player_id               integer REFERENCES players (player_id) ON DELETE CASCADE,
    position                varchar(25),
    location                point,
    under_pressure          boolean,
    off_camera              boolean,
    out                     boolean,
    counterpress            boolean,
    deflection              boolean,
    offensive               boolean,
    save_block              boolean
);


-- Carry
CREATE TABLE IF NOT EXISTS event_43 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches (match_id) ON DELETE CASCADE,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams (team_id) ON DELETE CASCADE,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams (team_id) ON DELETE CASCADE,
    player_id               integer REFERENCES players (player_id) ON DELETE CASCADE,
    position                varchar(25),
    location                point,
    duration                integer, -- event duration in seconds
    under_pressure          boolean,
    end_location            point
);


-- Clearance
CREATE TABLE IF NOT EXISTS event_9 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches (match_id) ON DELETE CASCADE,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams (team_id) ON DELETE CASCADE,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams (team_id) ON DELETE CASCADE,
    player_id               integer REFERENCES players (player_id) ON DELETE CASCADE,
    position                varchar(25),
    location                point,
    under_pressure          boolean,
    off_camera              boolean,
    out                     boolean,
    aerial_won              boolean,
    body_part               varchar(20)
);


-- Dispossessed
CREATE TABLE IF NOT EXISTS event_3 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches (match_id) ON DELETE CASCADE,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams (team_id) ON DELETE CASCADE,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams (team_id) ON DELETE CASCADE,
    player_id               integer REFERENCES players (player_id) ON DELETE CASCADE,
    position                varchar(25),
    location                point,
    under_pressure          boolean,
    off_camera              boolean
);


-- Dribble
CREATE TABLE IF NOT EXISTS event_14 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches (match_id) ON DELETE CASCADE,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams (team_id) ON DELETE CASCADE,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams (team_id) ON DELETE CASCADE,
    player_id               integer REFERENCES players (player_id) ON DELETE CASCADE,
    position                varchar(25),
    location                point,
    under_pressure          boolean,
    off_camera              boolean,
    out                     boolean,
    outcome                 varchar(20),
    nutmeg                  boolean,
    overrun                 boolean,
    no_touch                boolean
);


-- Dribbled Past
CREATE TABLE IF NOT EXISTS event_39 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches (match_id) ON DELETE CASCADE,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams (team_id) ON DELETE CASCADE,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams (team_id) ON DELETE CASCADE,
    player_id               integer REFERENCES players (player_id) ON DELETE CASCADE,
    position                varchar(25),
    location                point,
    off_camera              boolean,
    counterpress            boolean
);


-- Duel
CREATE TABLE IF NOT EXISTS event_4 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches (match_id) ON DELETE CASCADE,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams (team_id) ON DELETE CASCADE,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams (team_id) ON DELETE CASCADE,
    player_id               integer REFERENCES players (player_id) ON DELETE CASCADE,
    position                varchar(25),
    location                point,
    under_pressure          boolean,
    off_camera              boolean,
    counterpress            boolean,
    type                    varchar(20),
    outcome                 varchar(20)
);


-- Error
CREATE TABLE IF NOT EXISTS event_37 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches (match_id) ON DELETE CASCADE,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams (team_id) ON DELETE CASCADE,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams (team_id) ON DELETE CASCADE,
    player_id               integer REFERENCES players (player_id) ON DELETE CASCADE,
    position                varchar(25),
    location                point,
    under_pressure          boolean,
    off_camera              boolean
);


-- Foul Committed
CREATE TABLE IF NOT EXISTS event_22 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches (match_id) ON DELETE CASCADE,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams (team_id) ON DELETE CASCADE,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams (team_id) ON DELETE CASCADE,
    player_id               integer REFERENCES players (player_id) ON DELETE CASCADE,
    position                varchar(25),
    location                point,
    under_pressure          boolean,
    off_camera              boolean,
    advantage               boolean,
    counterpress            boolean,
    offensive               boolean,
    penalty                 boolean,
    card                    varchar(20),
    type                    varchar(20)
);


-- Foul Won
CREATE TABLE IF NOT EXISTS event_21 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches (match_id) ON DELETE CASCADE,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams (team_id) ON DELETE CASCADE,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams (team_id) ON DELETE CASCADE,
    player_id               integer REFERENCES players (player_id) ON DELETE CASCADE,
    position                varchar(25),
    location                point,
    under_pressure          boolean,
    off_camera              boolean,
    advantage               boolean,
    defensive               boolean,
    penalty                 boolean
);


-- Goal Keeper
CREATE TABLE IF NOT EXISTS event_23 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches (match_id) ON DELETE CASCADE,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams (team_id) ON DELETE CASCADE,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams (team_id) ON DELETE CASCADE,
    player_id               integer REFERENCES players (player_id) ON DELETE CASCADE,
    position                varchar(25),
    location                point,
    under_pressure          boolean,
    off_camera              boolean,
    out                     boolean,
    goalkeeper_position     varchar(20),
    technique               varchar(20),
    body_part               varchar(20),
    type                    varchar(20),
    outcome                 varchar(20)
);


-- Half End
CREATE TABLE IF NOT EXISTS event_34 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches (match_id) ON DELETE CASCADE,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams (team_id) ON DELETE CASCADE,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams (team_id) ON DELETE CASCADE,
    under_pressure          boolean
);


-- Half Start
CREATE TABLE IF NOT EXISTS event_18 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches (match_id) ON DELETE CASCADE,
    index                   integer,
    period                  integer, -- constraints: 1-5
    possession              integer,
    possession_team_id      integer REFERENCES teams (team_id) ON DELETE CASCADE,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams (team_id) ON DELETE CASCADE,
    late_video_start        boolean
);


-- Injury Stoppage
CREATE TABLE IF NOT EXISTS event_40 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches (match_id) ON DELETE CASCADE,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams (team_id) ON DELETE CASCADE,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams (team_id) ON DELETE CASCADE,
    player_id               integer REFERENCES players (player_id) ON DELETE CASCADE,
    position                varchar(25),
    under_pressure          boolean,
    off_camera              boolean,
    in_chain                boolean
);


-- Interception
CREATE TABLE IF NOT EXISTS event_10 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches (match_id) ON DELETE CASCADE,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams (team_id) ON DELETE CASCADE,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams (team_id) ON DELETE CASCADE,
    player_id               integer REFERENCES players (player_id) ON DELETE CASCADE,
    position                varchar(25),
    location                point,
    under_pressure          boolean,
    off_camera              boolean,
    outcome                 varchar(20)
);


-- Miscontrol
CREATE TABLE IF NOT EXISTS event_38 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches (match_id) ON DELETE CASCADE,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams (team_id) ON DELETE CASCADE,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams (team_id) ON DELETE CASCADE,
    player_id               integer REFERENCES players (player_id) ON DELETE CASCADE,
    position                varchar(25),
    location                point,
    under_pressure          boolean,
    off_camera              boolean,
    out                     boolean,
    aerial_won              boolean
);


-- Offside
CREATE TABLE IF NOT EXISTS event_8 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches (match_id) ON DELETE CASCADE,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams (team_id) ON DELETE CASCADE,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams (team_id) ON DELETE CASCADE,
    player_id               integer REFERENCES players (player_id) ON DELETE CASCADE,
    position                varchar(25),
    location                point
);


-- Own Goal Against
CREATE TABLE IF NOT EXISTS event_20 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches (match_id) ON DELETE CASCADE,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams (team_id) ON DELETE CASCADE,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams (team_id) ON DELETE CASCADE,
    player_id               integer REFERENCES players (player_id) ON DELETE CASCADE,
    position                varchar(25),
    location                point
);


-- Own Goal For
CREATE TABLE IF NOT EXISTS event_25 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches (match_id) ON DELETE CASCADE,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams (team_id) ON DELETE CASCADE,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams (team_id) ON DELETE CASCADE,
    player_id               integer REFERENCES players (player_id) ON DELETE CASCADE,
    position                varchar(25),
    location                point
);


-- Pass
CREATE TABLE IF NOT EXISTS event_30 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches (match_id) ON DELETE CASCADE,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams (team_id) ON DELETE CASCADE,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams (team_id) ON DELETE CASCADE,
    player_id               integer REFERENCES players (player_id) ON DELETE CASCADE,
    position                varchar(25),
    location                point,
    duration                integer, -- event duration in seconds
    under_pressure          boolean,
    off_camera              boolean,
    out                     boolean,
    recipient               integer REFERENCES players (player_id) ON DELETE CASCADE,
    length                  float,
    angle                   float,
    height                  varchar(20),
    end_location            point,
    assisted_shot_id        uuid, -- references event_16
    backheel                boolean,
    deflected               boolean,
    miscommunication        boolean,
    "cross"                 boolean,
    cut_back                boolean,
    switch                  boolean,
    shot_assist             boolean,
    goal_assist             boolean,
    body_part               varchar(20),
    type                    varchar(20),
    outcome                 varchar(20),
    technique               varchar(20)
);


-- Player Off
CREATE TABLE IF NOT EXISTS event_27 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches (match_id) ON DELETE CASCADE,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams (team_id) ON DELETE CASCADE,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams (team_id) ON DELETE CASCADE,
    player_id               integer REFERENCES players (player_id) ON DELETE CASCADE,
    position                varchar(25),
    off_camera              boolean
);


-- Player On
CREATE TABLE IF NOT EXISTS event_26 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches (match_id) ON DELETE CASCADE,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams (team_id) ON DELETE CASCADE,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams (team_id) ON DELETE CASCADE,
    player_id               integer REFERENCES players (player_id) ON DELETE CASCADE,
    position                varchar(25),
    off_camera              boolean
);


-- Pressure
CREATE TABLE IF NOT EXISTS event_17 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches (match_id) ON DELETE CASCADE,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams (team_id) ON DELETE CASCADE,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams (team_id) ON DELETE CASCADE,
    player_id               integer REFERENCES players (player_id) ON DELETE CASCADE,
    position                varchar(25),
    location                point,
    duration                integer, -- event duration in seconds
    under_pressure          boolean,
    off_camera              boolean,
    counterpress            boolean
);


-- Referee Ball Drop
CREATE TABLE IF NOT EXISTS event_41 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches (match_id) ON DELETE CASCADE,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams (team_id) ON DELETE CASCADE,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams (team_id) ON DELETE CASCADE,
    location                point,
    off_camera              boolean
);


-- Shield
CREATE TABLE IF NOT EXISTS event_28 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches (match_id) ON DELETE CASCADE,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams (team_id) ON DELETE CASCADE,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams (team_id) ON DELETE CASCADE,
    player_id               integer REFERENCES players (player_id) ON DELETE CASCADE,
    position                varchar(25),
    location                point,
    under_pressure          boolean
);


-- Shot
CREATE TABLE IF NOT EXISTS event_16 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches (match_id) ON DELETE CASCADE,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams (team_id) ON DELETE CASCADE,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams (team_id) ON DELETE CASCADE,
    player_id               integer REFERENCES players (player_id) ON DELETE CASCADE,
    position                varchar(25),
    location                point,
    duration                integer, -- event duration in seconds
    under_pressure          boolean,
    off_camera              boolean,
    out                     boolean,
    key_pass_id             uuid REFERENCES event_30 (event_id) ON DELETE CASCADE,
    end_location            point,
    aerial_won              boolean,
    follows_dribble         boolean,
    first_time              boolean,
    open_goal               boolean,
    statsbomb_xg            float,
    deflected               boolean,
    technique               varchar(20),
    body_part               varchar(20),
    type                    varchar(20),
    outcome                 varchar(20)
);

-- add foreign key constrain to event_30
--ALTER TABLE event_30 DROP CONSTRAINT IF EXISTS fk_assisted_shot;
ALTER TABLE event_30
    ADD CONSTRAINT fk_assisted_shot FOREIGN KEY (assisted_shot_id)
        REFERENCES event_16 (event_id) ON DELETE CASCADE;


-- Starting XI
CREATE TABLE IF NOT EXISTS event_35 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches (match_id) ON DELETE CASCADE,
    index                   integer,
    team_id                 integer REFERENCES teams (team_id) ON DELETE CASCADE,
    duration                integer, -- event duration in seconds
    formation               integer,
    lineup                  lineup[]
);


-- Substitution
CREATE TABLE IF NOT EXISTS event_19 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches (match_id) ON DELETE CASCADE,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams (team_id) ON DELETE CASCADE,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams (team_id) ON DELETE CASCADE,
    player_id               integer REFERENCES players (player_id) ON DELETE CASCADE,
    position                varchar(25),
    off_camera              boolean,
    replacement             integer REFERENCES players (player_id) ON DELETE CASCADE,
    outcome                 varchar(20)
);


-- Tactical Shift
CREATE TABLE IF NOT EXISTS event_36 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches (match_id) ON DELETE CASCADE,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams (team_id) ON DELETE CASCADE,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams (team_id) ON DELETE CASCADE,
    duration                integer, -- event duration in seconds
    formation               integer,
    lineup                  lineup[]
);

CREATE TABLE IF NOT EXISTS events_by_type (
    event_id                uuid PRIMARY KEY,
    table_name              char(8)
);

CREATE TABLE IF NOT EXISTS related_events (
    event_id_1              uuid REFERENCES events_by_type (event_id) ON DELETE CASCADE,
    event_id_2              uuid REFERENCES events_by_type (event_id) ON DELETE CASCADE
);

