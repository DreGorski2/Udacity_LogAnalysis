# Udacity_LogAnalysis

#**Project Description:**
Create a reporting tool that prints out reports (in plain text) based on the data in the database. This reporting tool is a Python program using the psycopg2 module to connect to the database.

##**Questions:**
1. What are the most popular three articles of all time? Which articles have been accessed the most? Present this information as a sorted list with the most popular article at the top.

2. Who are the most popular article authors of all time? That is, when you sum up all of the articles each author has written, which authors get the most page views? Present this as a sorted list with the most popular author at the top.

3. On which days did more than 1% of requests lead to errors? The log table includes a column status that indicates the HTTP status code that the news site sent to the user's browser. (Refer to this lesson for more information about the idea of HTTP status codes.)

###**Project Setup**
1. Install Vagrant 
2. Install Virtual Box
3. Download the Virtual machine config files (https://github.com/udacity/fullstack-nanodegree-vm)
4. Start up the Virtual machine (vagrant up--> vagrant ssh)
5. Download the newsdata.sql data 
6. Unzip the newsdata.sql and place the file within vagrant directory
7. Load the newsdata by running the following in the command terminal: psql -d news -f newsdata.sql
8. Connect to the database so you can start entering queries: psql -d news


####**The Queries**

**1.** _What are the most popular three articles of all time? Which articles have been accessed the most? Present this information as a sorted list with the most popular article at the top_

'''sql
 news=> select title, views from (select substring(path, '[^/]*$'), count(*) as views from log where path !='/' group by path) as views, articles where substring = slug order by views desc limit 3;
'''

joining the articles and log table where the slug equales the path by removing the '/article/' from the path by starting the after the / and removing any incomplete path's with does not equal '/'. 


**2.** _Who are the most popular article authors of all time? That is, when you sum up all of the articles each author has written, which authors get the most page views? Present this as a sorted list with the most popular author at the top._

'''sql
news=> select name, sum(views) as page_views from
          (select name, author, title, views from 
            (select substring(path, '[^/]*$'), count(*) as views from log
                where path != '/  group by path)
             as views, articles, authors 
             where substring = slug and author = author.id
             order by views desc)
           as master group by name order by page_views desc; 
'''

 Joining articles, log , and authors into one table useing 2 subqueries. The first being the subquery from question 1 the second is modified to join where the substring(path) equales the slug as well as where the the author = author(id). We then parse this master table down to just name and and sum of views for each author grouping by name from authors table and page views. 
 





































