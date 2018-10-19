# import the python modual to work with the database
import psycopg2
DBNAME = 'news'


def main():

    print("\n\nPopular articles\n")

    popular_articles = get_popular_articles()
    format_popular_articles(popular_articles)

    print("\n\nTop authors\n")

    top_authors = get_top_authors()
    format_top_authors(top_authors)

    print("\n\nError logs\n")

    error_logs = get_error_logs()
    format_error_log(error_logs)


# 1 What are the most popular three articles of all time?
def get_popular_articles():
    # Returns 3 most read articles of all time
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c. execute("""
        select title, views from
          (select substring(path, '[^/]*$'), count(*) as views from log
            where path !='/' group by path)
        as views, articles where substring = slug order by views desc limit 3;
    """)
    db.close
    return c.fetchall()


def format_popular_articles(popular_articles):
    for article in popular_articles:
        print(article[0] + " - " + str(article[1]))

# 2 Who are the most popular article authors of all time?
# That is when you sum up all of the articles each author has written , which authors get the most page views
# present this as a sorted list with the most popular author at the top
def get_top_authors():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""
       select name, sum(views) as page_views from
           (select name, author, title, views from
               (select substring(path, '[^/]*$'), count(*) as views from log
                       where path !='/' group by path)
                as views, articles, authors
                where substring = slug and author = authors.id
                order by views desc)
           as master group by name order by page_views desc;
       """)
    db.close
    return c.fetchall()


def format_top_authors(top_authors):
    for author in top_authors:
        name = author[0]
        views = author[1]
        print(name + " - " + str(views))


# 3 On which days did more than 1% of requests lead to errors?
# The log table includes a column status that indicates the HTTP status code that the news site sent
# to the user's browser
def get_error_logs():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""
        select * from
                (select hospital.date, requests, error_404, (error_404::float/requests::float * 100) as error_rate from
                (select date(time) as date, count(*) as requests from log group by date) as hospital,
                (select date(time) as date, count(*) as error_404 from log where status = '404 NOT FOUND' group by date) as errors
                where hospital.date = errors.date) as sub
        where sub.error_rate > 1;
        """)
    db.close
    return c.fetchall()


def format_error_log(error_logs):
    for error_log in error_logs:
        date = error_log[0]
        error = error_log[3]
        print(str(date) + " - " + str(round(error,1)))

if __name__ == "__main__":
    main()
