DROP TABLE IF EXISTS referees; -- done
CREATE TABLE referees (
    referee_id          integer PRIMARY KEY,
    name                varchar(50),
    country             varchar(35)
);


DROP TABLE IF EXISTS stadiums; -- done
CREATE TABLE stadiums (
    stadium_id          integer PRIMARY KEY,
    name                varchar(50),
    country             varchar(35)
);


DROP TABLE IF EXISTS managers; -- done
CREATE TABLE managers (
    manager_id          integer PRIMARY KEY,
    name                varchar(50),
    nickname            varchar(50),
    dob                 date,
    country             varchar(35)
);


DROP TABLE IF EXISTS teams; -- done
CREATE TABLE teams (
    team_id             integer PRIMARY KEY,
    name                varchar(50),
    gender              varchar(6),
    "group"               varchar(20), -- not sure about character length
    country             varchar(35)
);


DROP TABLE IF EXISTS competitions; -- done
CREATE TABLE competitions (
    competition_id      int PRIMARY KEY,
    country             varchar(35),
    name              varchar(50),
    gender              varchar(6),
    youth               boolean,
    international       boolean
);


DROP TABLE IF EXISTS matches; -- done
CREATE TABLE matches (
    match_id                    integer PRIMARY KEY,
    match_date                        date,
    kick_off                     time, -- game start time
    competition_id              integer REFERENCES competitions,
    season                      char(9), -- yyyy/yyyy
    home_team_id                integer REFERENCES teams,
    away_team_id                integer REFERENCES teams,
    home_score                  integer,
    away_score                  integer,
    match_week                  integer,
    competition_stage_name      varchar(40),
    stadium_id                  integer REFERENCES stadiums,
    referee_id                  integer REFERENCES referees
);


DROP TABLE IF EXISTS managers_by_team_and_match; -- done
CREATE TABLE managers_by_team_and_match (
    match_id        integer REFERENCES matches,
    team_id         integer REFERENCES teams,
    manager_id      integer REFERENCES managers
);


DROP TABLE IF EXISTS players; -- done
CREATE TABLE players (
    player_id           integer PRIMARY KEY,
    name                varchar(50),
    nickname            varchar(50),
    country             varchar(35)
);


CREATE TYPE card AS (
    time                timestamp,
    type                varchar(20),
    reason              varchar(20),
    period              integer
);

CREATE TYPE position AS (
    name                varchar(25),
    "from"                timestamp,
    "to"                  timestamp,
    from_period         integer,
    to_period           integer,
    start_reason        varchar(35),
    end_reason          varchar(35)
);


DROP TABLE IF EXISTS lineups;
CREATE TABLE lineups (
    match_id            integer REFERENCES matches,
    team_id             integer REFERENCES teams,
    player_id           integer REFERENCES players,
    cards               card[],
    positions           "position"[],
    jersey_number       integer
);


-- one table per event type, which lists match/player/team info, plus event specific info

-- 50/50
DROP TABLE IF EXISTS event_33;
CREATE TABLE event_33 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams,
    player_id               integer REFERENCES players,
    position                varchar(25),
    location                point,
    under_pressure          boolean,
    out                     boolean,
    outcome                 varchar(20),
    counterpress            boolean
);


-- Bad Behaviour
DROP TABLE IF EXISTS event_24;
CREATE TABLE event_24 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams,
    player_id               integer REFERENCES players,
    position                varchar(25),
    off_camera              boolean,
    card                    varchar(20)
);


-- Ball Receipt
DROP TABLE IF EXISTS event_42;
CREATE TABLE event_42 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams,
    player_id               integer REFERENCES players,
    position                varchar(25),
    location                point,
    under_pressure          boolean,
    outcome                 varchar(20)
);


-- Ball Recovery
DROP TABLE IF EXISTS event_2;
CREATE TABLE event_2 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams,
    player_id               integer REFERENCES players,
    position                varchar(25),
    location                point,
    under_pressure          boolean,
    off_camera              boolean,
    out                     boolean,
    offensive               boolean,
    recovery_failure        boolean
);


-- Block
DROP TABLE IF EXISTS event_6;
CREATE TABLE event_6 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams,
    player_id               integer REFERENCES players,
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
DROP TABLE IF EXISTS event_43;
CREATE TABLE event_43 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams,
    player_id               integer REFERENCES players,
    position                varchar(25),
    location                point,
    duration                integer, -- event duration in seconds
    under_pressure          boolean,
    end_location            point
);


-- Clearance
DROP TABLE IF EXISTS event_9;
CREATE TABLE event_9 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams,
    player_id               integer REFERENCES players,
    position                varchar(25),
    location                point,
    under_pressure          boolean,
    off_camera              boolean,
    out                     boolean,
    aerial_won              boolean,
    body_part               varchar(20)
);


-- Dispossessed
DROP TABLE IF EXISTS event_3;
CREATE TABLE event_3 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams,
    player_id               integer REFERENCES players,
    position                varchar(25),
    location                point,
    under_pressure          boolean,
    off_camera              boolean
);


-- Dribble
DROP TABLE IF EXISTS event_14;
CREATE TABLE event_14 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams,
    player_id               integer REFERENCES players,
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
DROP TABLE IF EXISTS event_39;
CREATE TABLE event_39 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams,
    player_id               integer REFERENCES players,
    position                varchar(25),
    location                point,
    off_camera              boolean,
    counterpress            boolean
);


-- Duel
DROP TABLE IF EXISTS event_4;
CREATE TABLE event_4 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams,
    player_id               integer REFERENCES players,
    position                varchar(25),
    location                point,
    under_pressure          boolean,
    off_camera              boolean,
    counterpress            boolean,
    type                    varchar(20),
    outcome                 varchar(20)
);


-- Error
DROP TABLE IF EXISTS event_37;
CREATE TABLE event_37 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams,
    player_id               integer REFERENCES players,
    position                varchar(25),
    location                point,
    under_pressure          boolean,
    off_camera              boolean
);


-- Foul Committed
DROP TABLE IF EXISTS event_22;
CREATE TABLE event_22 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams,
    player_id               integer REFERENCES players,
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
DROP TABLE IF EXISTS event_21;
CREATE TABLE event_21 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams,
    player_id               integer REFERENCES players,
    position                varchar(25),
    location                point,
    under_pressure          boolean,
    off_camera              boolean,
    advantage               boolean,
    defensive               boolean,
    penalty                 boolean
);


-- Goal Keeper
DROP TABLE IF EXISTS event_23;
CREATE TABLE event_23 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams,
    player_id               integer REFERENCES players,
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
DROP TABLE IF EXISTS event_34;
CREATE TABLE event_34 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams,
    under_pressure          boolean
);


-- Half Start
DROP TABLE IF EXISTS event_18;
CREATE TABLE event_18 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches,
    index                   integer,
    period                  integer, -- constraints: 1-5
    possession              integer,
    possession_team_id      integer REFERENCES teams,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams,
    late_video_start        boolean
);


-- Injury Stoppage
DROP TABLE IF EXISTS event_40;
CREATE TABLE event_40 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams,
    player_id               integer REFERENCES players,
    position                varchar(25),
    under_pressure          boolean,
    off_camera              boolean,
    in_chain                boolean
);


-- Interception
DROP TABLE IF EXISTS event_10;
CREATE TABLE event_10 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams,
    player_id               integer REFERENCES players,
    position                varchar(25),
    location                point,
    under_pressure          boolean,
    off_camera              boolean,
    outcome                 varchar(20)
);


-- Miscontrol
DROP TABLE IF EXISTS event_38;
CREATE TABLE event_38 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams,
    player_id               integer REFERENCES players,
    position                varchar(25),
    location                point,
    under_pressure          boolean,
    off_camera              boolean,
    out                     boolean,
    aerial_won              boolean
);


-- Offside
DROP TABLE IF EXISTS event_8;
CREATE TABLE event_8 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams,
    player_id               integer REFERENCES players,
    position                varchar(25),
    location                point
);


-- Own Goal Against
DROP TABLE IF EXISTS event_20;
CREATE TABLE event_20 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams,
    player_id               integer REFERENCES players,
    position                varchar(25),
    location                point
);


-- Own Goal For
DROP TABLE IF EXISTS event_25;
CREATE TABLE event_25 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams,
    player_id               integer REFERENCES players,
    position                varchar(25),
    location                point
);


-- Pass
DROP TABLE IF EXISTS event_30;
CREATE TABLE event_30 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams,
    player_id               integer REFERENCES players,
    position                varchar(25),
    location                point,
    duration                integer, -- event duration in seconds
    under_pressure          boolean,
    off_camera              boolean,
    out                     boolean,
    recipient               integer REFERENCES players,
    length                  float,
    angle                   float,
    height                  varchar(20),
    end_location            point,
    assisted_shot_id        integer REFERENCES event_16,
    backheel                boolean,
    deflected               boolean,
    miscommunication        boolean,
    "cross"                   boolean,
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
DROP TABLE IF EXISTS event_27;
CREATE TABLE event_27 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams,
    player_id               integer REFERENCES players,
    position                varchar(25),
    off_camera              boolean
);


-- Player On
DROP TABLE IF EXISTS event_26;
CREATE TABLE event_26 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams,
    player_id               integer REFERENCES players,
    position                varchar(25),
    off_camera              boolean
);


-- Pressure
DROP TABLE IF EXISTS event_17;
CREATE TABLE event_17 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams,
    player_id               integer REFERENCES players,
    position                varchar(25),
    location                point,
    duration                integer, -- event duration in seconds
    under_pressure          boolean,
    off_camera              boolean,
    counterpress            boolean
);


-- Referee Ball Drop
DROP TABLE IF EXISTS event_41;
CREATE TABLE event_41 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams,
    location                point,
    off_camera              boolean
);


-- Shield
DROP TABLE IF EXISTS event_28;
CREATE TABLE event_28 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams,
    player_id               integer REFERENCES players,
    position                varchar(25),
    location                point,
    under_pressure          boolean
);


-- Shot
DROP TABLE IF EXISTS event_16;
CREATE TABLE event_16 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams,
    player_id               integer REFERENCES players,
    position                varchar(25),
    location                point,
    duration                integer, -- event duration in seconds
    under_pressure          boolean,
    off_camera              boolean,
    out                     boolean,
    key_pass_id             integer REFERENCES event_30,
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


-- a lineup data type for events 35 and 36
CREATE TYPE lineup AS (
    player_id               integer, -- REFERENCES players
    position                varchar(25),
    jersey_number           int
);


-- Starting XI
DROP TABLE IF EXISTS event_35;
CREATE TABLE event_35 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches,
    index                   integer,
    team_id                 integer REFERENCES teams,
    duration                integer, -- event duration in seconds
    formation               integer,
    lineup                  lineup[]
);


-- Substitution
DROP TABLE IF EXISTS event_19;
CREATE TABLE event_19 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams,
    player_id               integer REFERENCES players,
    position                varchar(25),
    off_camera              boolean,
    replacement             integer REFERENCES players,
    outcome                 varchar(20)
);


-- Tactical Shift
DROP TABLE IF EXISTS event_36;
CREATE TABLE event_36 (
    event_id                uuid PRIMARY KEY,
    match_id                integer REFERENCES matches,
    index                   integer,
    period                  integer, -- constraints: 1-5
    timestamp               timestamp,
    possession              integer,
    possession_team_id      integer REFERENCES teams,
    play_pattern            varchar(14),
    team_id                 integer REFERENCES teams,
    duration                integer, -- event duration in seconds
    formation               integer,
    lineup                  lineup[]
);


DROP TABLE IF EXISTS related_events;
CREATE TABLE related_events (
    event_id_1              uuid REFERENCES events_by_type,
    event_id_2              uuid REFERENCES events_by_type
    -- primary key combined id 1 and 2
);


DROP TABLE IF EXISTS events_by_type;
CREATE TABLE events_by_type (
    event_id                uuid PRIMARY KEY,
    table_name              char(8)
);
