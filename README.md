# Udacity_LogAnalysis

**Project Description:**
Create a reporting tool that prints out reports (in plain text) based on the data in the database. This reporting tool is a Python program using the psycopg2 module to connect to the database.

**Questions:**
1. What are the most popular three articles of all time? Which articles have been accessed the most? Present this information as a sorted list with the most popular article at the top.

2. Who are the most popular article authors of all time? That is, when you sum up all of the articles each author has written, which authors get the most page views? Present this as a sorted list with the most popular author at the top.

3. On which days did more than 1% of requests lead to errors? The log table includes a column status that indicates the HTTP status code that the news site sent to the user's browser. (Refer to this lesson for more information about the idea of HTTP status codes.)

**Project Setup**
1. Install Vagrant 
2. Install Virtual Box
3. Download the Virtual machine config files (https://github.com/udacity/fullstack-nanodegree-vm)
4. Start up the Virtual machine (vagrant up--> vagrant ssh)
5. Download the newsdata.sql data 
6. Unzip the newsdata.sql and place the file within vagrant directory
7. Load the newsdata by running the following in the command terminal: psql -d news -f newsdata.sql
8. Connect to the database so you can start entering queries: psql -d news


**The Queries**

**1. What are the most popular three articles of all time? Which articles have been accessed the most? Present this information as a sorted list with the most popular article at the top**

```sql

 news=> select title, views from (select substring(path, '[^/]*$'), count(*) as views from log where path !='/' group by path) as views, articles where substring = slug order by views desc limit 3;
```

joining the articles and log table where the slug equals the path and removing the '/article/' from the path by starting the after the / , and removing any incomplete path's with does not equal '/'. 





**2. Who are the most popular article authors of all time? That is, when you sum up all of the articles each author has written, which authors get the most page views? Present this as a sorted list with the most popular author at the top.**

```sql
news=> select name, sum(views) as page_views from
          (select name, author, title, views from 
            (select substring(path, '[^/]*$'), count(*) as views from log
                where path != '/  group by path)
             as views, articles, authors 
             where substring = slug and author = author.id
             order by views desc)
           as master group by name order by page_views desc;
```

Joining articles, log , and authors into one table useing 2 subqueries. The first being the subquery from question 1 the second is modified to join where the substring(path) equales the slug as well as where the the author = author(id). We then parse this master table down to just name and and sum of views for each author grouping by name from authors table and page views. 



 
**3. On which days did more than 1% of requests lead to errors? The log table includes a column status that indicates the HTTP status code that the news site sent to the user's browser.**

```sql
select * from
   news=> select hospital.date, requests, error_404, (error_404::float/requests::float * 100) as error_rate from
   (select date(time) as date, count(*) as requests from log group by date) as hospital,
   (select date(time) as date, count(*) as error_404 from log where status = '404 NOT FOUND' group by date) as errors
   where hospital.date = errors.date) as sub
where sub.error_rate > 1;
```

Gather timestamps(requests) and group them by date, gather status(error_404) that display the "404 NOT FOUND' error, and divide the error_404 column by requests to get the error_rate. Put the entire query into the a sub-query and filter that to get the result needed by only showing error-rate greater than 1.


**Run the Queries**

Queries found the SQl.py are formated with Python3 

Run the following commands in the terminal window to execute the python script uing pyscopg2 as the db client 

**1. List the files**
```
vagrant@vagrant:~$ ls
```
assignment.py  redis-stable  redis-stable.tar.gz  test2.py  test3.py  test4.py  test.py

**2. To find the current directory path**
```
vagrant@vagrant:~$ pwd
```
/home/vagrant

**3. Run the script calling out python**
```
vagrant@vagrant:~$ python assignment.py
```

**4.Then python will display the formated query results.** 
```
Popular articles

Candidate is jerk, alleges rival - 338647
Bears love berries, alleges bear - 253801
Bad things gone, say good people - 170098


Top authors

Ursula La Multa - 507594
Rudolf von Treppenwitz - 423457
Anonymous Contributor - 170098
Markoff Chaney - 84557


Error logs

2016-07-17 - 2.3
```

































