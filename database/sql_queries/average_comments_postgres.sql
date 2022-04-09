WITH user_avg_monthly_comments AS
(
   SELECT
      c.user_id,
      AVG(c.total_comments) AS avg_comments
   FROM
      (
         SELECT
            user_id,
            Count(*) AS total_comments,
            EXTRACT(MONTH from creation_date) AS mnth
         FROM
            comments
         GROUP BY
            user_id,
            mnth
      )
      AS c
   GROUP BY
      c.user_id
)
UPDATE
   users
SET
   avg_monthly_comments =
   (
      SELECT
         temp.avg_comments
      FROM
         user_avg_monthly_comments temp
      WHERE
         users.id = temp.user_id
   )
