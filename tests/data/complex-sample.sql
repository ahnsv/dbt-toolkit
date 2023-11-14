with stg1 as (select *
              from `your-project.your_dataset2.your_table`),
     stg2 as (select *
              from (select id, name, age
                    from `your-project.your_dataset3.your_user_table`
                             CROSS JOIN (SELECT ci.corp_number
                                              , cmt.*
                                         FROM `your-project.your_dataset.your_corporate_mapping_table` as cmt
                                                  LEFT JOIN `your-project.your_dataset.your_corporate_table` as ci
                                                            ON cmt.user_id = ci.user_id) as br
                    GROUP BY date))
select
from stg1
         left join stg2 on stg1.date = stg2.date
ORDER BY date desc
