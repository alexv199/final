-- Q1
/*
SELECT
    name, AVG(statsbomb_xg) AS average_xg
FROM
    players AS p
    INNER JOIN LATERAL (
        SELECT
            player_id, e.statsbomb_xg
        FROM
            event_16 AS e
            INNER JOIN LATERAL (
                SELECT
                    m.match_id, m.season
                FROM
                    matches AS m
                    INNER JOIN LATERAL (
                        SELECT
                            competition_id
                        FROM competitions AS c
                        WHERE c.name = 'La Liga'
                    ) AS t ON m.competition_id = t.competition_id
            ) AS t ON e.match_id = t.match_id AND t.season = '2020/2021'
    ) AS t ON p.player_id = t.player_id
WHERE statsbomb_xg > 0
GROUP BY name
ORDER BY average_xg DESC
;
*/

-- Q2
/*
SELECT
    name, COUNT(*) AS num_shots
FROM
    players AS p
    INNER JOIN LATERAL (
        SELECT
            player_id, e.statsbomb_xg
        FROM
            event_16 AS e
            INNER JOIN LATERAL (
                SELECT
                    m.match_id, m.season
                FROM
                    matches AS m
                    INNER JOIN LATERAL (
                        SELECT
                            competition_id
                        FROM competitions AS c
                        WHERE c.name = 'La Liga'
                    ) AS t ON m.competition_id = t.competition_id
            ) AS t ON e.match_id = t.match_id AND t.season = '2020/2021'
    ) AS t ON p.player_id = t.player_id
WHERE statsbomb_xg > 0
GROUP BY name
ORDER BY num_shots DESC
;
*/

-- Q3
/*
SELECT
    name, COUNT(*) AS num_first_time
FROM
    players AS p
    INNER JOIN LATERAL (
        SELECT
            player_id, e.first_time
        FROM
            event_16 AS e
            INNER JOIN LATERAL (
                SELECT
                    m.match_id, m.season
                FROM
                    matches AS m
                    INNER JOIN LATERAL (
                        SELECT
                            competition_id
                        FROM competitions AS c
                        WHERE c.name = 'La Liga'
                    ) AS t ON m.competition_id = t.competition_id
            ) AS t ON e.match_id = t.match_id
    ) AS t ON p.player_id = t.player_id
WHERE first_time = TRUE
GROUP BY name
ORDER BY num_first_time DESC
;
*/

--Q4
SELECT
    name, COUNT(*) AS num_first_time
FROM
    teams AS t0
    INNER JOIN LATERAL (
        SELECT
            team_id
        FROM
            event_30 AS e
            INNER JOIN LATERAL (
                SELECT
                    m.match_id, m.season
                FROM
                    matches AS m
                    INNER JOIN LATERAL (
                        SELECT
                            competition_id
                        FROM competitions AS c
                        WHERE c.name = 'La Liga'
                    ) AS t ON m.competition_id = t.competition_id
            ) AS t ON e.match_id = t.match_id AND t.season = '2020/2021'
    ) AS t ON t0.team_id = t.team_id
WHERE first_time = TRUE
GROUP BY name
ORDER BY num_first_time DESC
;


--q10
/*
SELECT
    p.name, COUNT(*) AS num_of_dribbles
FROM
    players AS p
    INNER JOIN LATERAL (
        SELECT
            player_id
        FROM
            event_39 AS e
            INNER JOIN LATERAL (
                SELECT
                    m.match_id, m.season
                FROM
                    matches AS m
                    INNER JOIN LATERAL (
                        SELECT
                            competition_id
                        FROM competitions AS c
                        WHERE c.name = 'La Liga'
                    ) AS t ON m.competition_id = t.competition_id
            ) AS t ON e.match_id = t.match_id AND t.season = '2020/2021'
    ) AS t ON p.player_id = t.player_id
GROUP BY p.name
ORDER BY number_of_dribbles_past ASC
;
*/
