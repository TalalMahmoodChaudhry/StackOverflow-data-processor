UPDATE
   users 
SET
   total_posts = nullif(COALESCE(users.total_posts, 0) + COALESCE(( 
   SELECT
      temp.total_posts 
   FROM
      (
        SELECT
           u.id,
           COUNT(p.id) AS total_posts
        FROM
           users u
           INNER JOIN
              posts p
              ON u.id =p.owner_user_id
        WHERE p.record_insert_date_time > '{last_timestamp}'
        GROUP BY
           u.id
        ) temp
   WHERE
      users.id = temp.id ), 0), 0);