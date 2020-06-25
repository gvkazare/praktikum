С какими актерами работал режиссер Jørgen Lerdam?

SELECT name FROM actors 
WHERE id IN (
	SELECT actor_id FROM movie_actors 
	WHERE movie_id = (
		SELECT id FROM movies 
		WHERE director LIKE '%Jørgen Lerdam%'));



Кто из сценаристов принял участие в большинстве фильмов?

SELECT name FROM (
	SELECT writer AS writer_id FROM movies 	
	WHERE writer_id != ''		
	UNION ALL		
	SELECT json_extract(writers_t.value, "$.id") AS writer_id FROM (
		SELECT writers FROM movies 
		WHERE writers != '') AS writers_json_array, json_each(writers_json_array.writers) AS writers_t		
	)		
	JOIN writers AS wrt_t ON writer_id = wrt_t.id
	WHERE wrt_t.name != 'N/A'	
GROUP BY writer_id 
ORDER BY count(writer_id) DESC LIMIT 1;



Кто из актеров снялся в большинстве фильмов?

SELECT act_t.name
FROM movie_actors AS mov_act_t
	JOIN actors AS act_t ON act_t.id = mov_act_t.actor_id 
	WHERE act_t.name != 'N/A'
GROUP BY act_t.name
ORDER BY COUNT(act_t.name) DESC LIMIT 1;
