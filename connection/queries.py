users_query = """
SELECT users.id, creation_at AS sign_up_date , strikes, countries.name AS country, countries.iso AS country_iso, genders.name AS gender 
     FROM sch_comm.users
     JOIN sch_comm.countries ON users.country_id_id = countries.id
     JOIN sch_comm.genders ON users.gender_id_id = genders.id 
"""

networking_query = """
SELECT id, title, number_of_likes
FROM (
	SELECT discussion_id, COUNT(user_id) AS number_of_likes
FROM sch_comm.netw_discussion_likes
GROUP BY discussion_id
) AS likes_count
RIGHT JOIN
sch_comm.netw_discussions AS discussions ON likes_count.discussion_id = discussions.id
LIMIT 7
"""

queries_dict = {
     "users" : users_query,
     "users_columns": ['id', 'sign_up_date', 'strikes', 'country', 'country_iso', 'gender'],
     "networking" : networking_query,
     "networking_columns" : ['id', 'title', 'number_of_likes']
}