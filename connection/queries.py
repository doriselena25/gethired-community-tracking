users_query = """
SELECT users.id, creation_at AS sign_up_date , strikes, countries.name AS country, countries.iso AS country_iso, genders.name AS gender 
     FROM sch_comm.users
     JOIN sch_comm.countries ON users.country_id_id = countries.id
     JOIN sch_comm.genders ON users.gender_id_id = genders.id 
"""

networking_query_populuar_posts = """
SELECT title, number_of_likes as likes
FROM (
	SELECT discussion_id, COUNT(user_id) AS number_of_likes
     FROM sch_comm.netw_discussion_likes
     GROUP BY discussion_id
     ORDER BY number_of_likes
) AS likes_count
RIGHT JOIN
sch_comm.netw_discussions AS discussions ON likes_count.discussion_id = discussions.id
LIMIT 7
"""

networking_query_populuar_categories = """
SELECT netw_categories.description as category, COUNT(category_id) as posts
FROM sch_comm.netw_discussions
JOIN sch_comm.netw_categories ON netw_discussions.category_id = netw_categories.id
GROUP BY category
ORDER BY posts DESC
"""


challenges_query = """
SELECT name as title, description as challenge
FROM sch_comm.challenges
WHERE name <> 'Palindrome'
"""


queries_dict = {
     "users" : users_query,
     "users_columns": ['id', 'sign_up_date', 'strikes', 'country', 'country_iso', 'gender'],
     "networking_posts" : networking_query_populuar_posts,
     "networking_posts_columns" : ['title', 'likes'],
     "networking_categories" : networking_query_populuar_categories,
     "networking_categories_columns" : ['category', 'posts'],
     "challenges": challenges_query,
     "challenges_columns": ['title', 'challenge']
}