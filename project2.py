
import pandas as pd
import psycopg2 
import matplotlib.pyplot as plt


import streamlit as st
st.write("BookScape Explorer")
a=st.selectbox("Question", ['1.Check Availability of eBooks vs Physical Books',
'2.Find the Publisher with the Most Books Published',
'3.Identify the Publisher with the Highest Average Rating',
'4.Get the Top 5 Most Expensive Books by Retail Price',
'5.Find Books Published After 2010 with at Least 500 Pages',
'6.List Books with Discounts Greater than 20%',
'7.Find the Average Page Count for eBooks vs Physical Books',
'8.Find the Top 3 Authors with the Most Books',
'9.List Publishers with More than 10 Books',
'10.Find the Average Page Count for Each Category',
'11.Retrieve Books with More than 3 Authors',
'12.Books with Ratings Count Greater Than the Average',
'13.Books with the Same Author Published in the Same Year',
'14.Books with a Specific Keyword in the Title',
'15.Year with the Highest Average Book Price',
'16.Count Authors Who Published 3 Consecutive Years',
'17.Write a SQL query to find authors who have published books in the same year but under different publishers. Return the authors, year, and the COUNT of books they published in that year',
'18.Create a query to find the average amount_retailPrice of eBooks and physical books. Return a single result set with columns for avg_ebook_price and avg_physical_price. Ensure to handle cases where either category may have no entries',
'19.Write a SQL query to identify books that have an averageRating that is more than two standard deviations away from the average rating of all books. Return the title, averageRating, and ratingsCount for these outliers',
'20.Create a SQL query that determines which publisher has the highest average rating among its books, but only for publishers that have published more than 10 books. Return the publisher, average_rating, and the number of books published'])


connection = psycopg2.connect(
        database="project2db",  # Replace with your database name
        user="postgres",          # Replace with your PostgreSQL username
        password="061101",      # Replace with your PostgreSQL password
        host="localhost",              # Replace with your host (default: localhost)
        port="5432"                    # Replace with your port (default: 5432)
    )
cursor = connection.cursor()

if a=='1.Check Availability of eBooks vs Physical Books':
    st.write(a)

    cursor.execute  (''' 
    
    SELECT
        "Book_id", COUNT(*) AS ebook_count 
    FROM 
        "df0" 
    GROUP BY 
        "Book_id";
    ''')


    cursor.execute ('''
    SELECT
        "Book_id", COUNT(*) AS physical_book_count
    FROM 
        "df0"  
    GROUP BY
        "Book_id";
    ''')



    ebooks = cursor.fetchall()
    df_ebooks = pd.DataFrame(ebooks, columns=['Book_id', 'ebook_count'])



    table1 = cursor.fetchall()
    answer_1 = pd.DataFrame(table1, columns=['Book_id', 'physical_book_count'])


    answer_1 = pd.merge(df_ebooks, answer_1, on='Book_id', how='outer').fillna(0)

    answer_1['ebook_count'] = answer_1['ebook_count'].astype(int)
    answer_1['physical_book_count'] = answer_1['physical_book_count'].astype(int)

    st.dataframe(answer_1)


if a=='2.Find the Publisher with the Most Books Published':
    st.write(a)
    cursor.execute ( '''
    SELECT 
        "Publisher", COUNT(*) AS book_count
    FROM 
        "df0"
    GROUP BY 
        "Publisher"
    ORDER BY 
        book_count DESC
    LIMIT 1;
    ''')

    table1 = cursor.fetchone()


    answer_2 = pd.DataFrame([table1], columns=['Publisher', 'Book Count'])

    st.dataframe(answer_2)

if a=='3.Identify the Publisher with the Highest Average Rating':
    st.write(a)
     
    cursor.execute('''
    SELECT 
            "Publisher", 
            AVG("Average_rating"::FLOAT) AS avg_rating  -- Correctly cast to FLOAT
        FROM 
            "df0"
        WHERE 
            "Average_rating" IS NOT NULL AND  -- Exclude NULL values
            "Average_rating" ~ '^[0-9.]+$'  -- Exclude non-numeric values
        GROUP BY 
            "Publisher"
        ORDER BY 
            avg_rating DESC  -- Sort by highest rating
        LIMIT 1;
    ''')
    
       
    table1 = cursor.fetchone()
       
    answer_3 = pd.DataFrame([table1], columns=['Publisher', 'Average_rating'])

    st.dataframe(answer_3)

if a=='4.Get the Top 5 Most Expensive Books by Retail Price':
    st.write(a)
    cursor.execute('''
    SELECT 
            "Book_id", 
            "Title", 
            "Publisher", 
            "Retail_Price", 
            "Currency_Retail_Price"
        FROM 
            "df0"
        WHERE 
            "Retail_Price" IS NOT NULL  
        ORDER BY 
            "Retail_Price" DESC  
        LIMIT 5;
    ''')


    table1 = cursor.fetchall()

    answer_4 = pd.DataFrame(table1, columns=['Book_id', 'Title', 'Publisher', 'Retail_Price', 'Currency'])

    st.dataframe(answer_4)

if a=='5.Find Books Published After 2010 with at Least 500 Pages':
    st.write(a)
    cursor.execute('''
    
        SELECT 
            "Book_id", 
            "Title", 
            "Publisher", 
            "Published_Date", 
            "Page_Count"
        FROM 
            "df0"
        WHERE 
            "Published_Date" > '2010-01-01'  -- Books published after 2010
            AND "Page_Count" >= 500  -- Books with at least 500 pages
        ORDER BY 
            "Published_Date" DESC;  -- Sort by most recent first
    ''')
    table1 = cursor.fetchall()

    
    answer_5 = pd.DataFrame(table1, columns=["Book ID", "Title", "Publisher", "Published Date", "Page Count"])

    st.dataframe(answer_5)
    
if a== '6.List Books with Discounts Greater than 20%':
    st.write(a)
    cursor.execute('''
    SELECT 
            "Book_id", 
            "Title", 
            "Publisher", 
            "List_Price", 
            "Retail_Price", 
            ROUND((("List_Price" - "Retail_Price") / "List_Price")::numeric, 2) AS discount_percentage
        FROM 
            "df0"
        WHERE 
            "List_Price" > 0  
            AND "Retail_Price" > 0  
            AND (("List_Price" - "Retail_Price") / "List_Price") > 0.20  
        ORDER BY 
            discount_percentage DESC;  
    ''')

    
    
    table1 = cursor.fetchall()

    
    answer_6 = pd.DataFrame(table1, columns=["Book ID", "Title", "Publisher", "List Price", "Retail Price", "Discount Percentage"])

    st.dataframe(answer_6)
if a== '7.Find the Average Page Count for eBooks vs Physical Books':
    st.write(a)
    cursor.execute('''
    SELECT 
            CASE 
                WHEN "Is_ebook" = 'TRUE' THEN 'eBook'
                ELSE 'Physical Book'
            END AS book_type,
            AVG("Page_Count") AS avg_page_count
        FROM 
            "df0"
        WHERE 
            "Page_Count" IS NOT NULL  -- Ensure Page_Count is not NULL
        GROUP BY 
            book_type
        ORDER BY 
            book_type;
    ''')

    table1 = cursor.fetchall()

   
    answer_7 = pd.DataFrame(table1, columns=["Book Type", "Average Page Count"])
    st.dataframe(answer_7)

if a== '8.Find the Top 3 Authors with the Most Books':
    st.write(a)
    cursor.execute('''
    SELECT 
            "Authors", 
            COUNT("Book_id") AS book_count
        FROM 
            "df0"
        WHERE 
            "Authors" IS NOT NULL  
        GROUP BY 
            "Authors"
        ORDER BY 
            book_count DESC  
        LIMIT 3;  
    ''')
    
    table1 = cursor.fetchall()

    answer_8 = pd.DataFrame(table1, columns=["Author", "Book Count"])
    st.dataframe(answer_8)
if a== '9.List Publishers with More than 10 Books':
    st.write(a)

    cursor.execute('''
        SELECT 
            "Publisher", 
            COUNT("Book_id") AS book_count
        FROM 
            "df0"
        WHERE 
            "Publisher" IS NOT NULL   
        GROUP BY 
            "Publisher"
        HAVING 
            COUNT("Book_id") > 10  
        ORDER BY 
            book_count DESC;  
    ''')

    table1 = cursor.fetchall()

    answer_9 = pd.DataFrame(table1, columns=["Publisher", "Book Count"])
    st.dataframe( answer_9 )
if a == '10.Find the Average Page Count for Each Category':
    st.write(a)
    cursor.execute('''
        SELECT 
            "Categories", 
            AVG("Page_Count") AS avg_page_count
        FROM 
            "df0"
        WHERE 
            "Page_Count" IS NOT NULL 
        GROUP BY 
            "Categories"
        ORDER BY 
            avg_page_count DESC; 
    ''')

    table1 = cursor.fetchall()

    answer_10 = pd.DataFrame(table1, columns=["Category", "Average Page Count"])
    st.dataframe(answer_10)

if a == '11.Retrieve Books with More than 3 Authors':
    st.write(a)
    cursor.execute('''
        SELECT 
            "Book_id", 
            "Title", 
            "Authors",
            LENGTH("Authors") - LENGTH(REPLACE("Authors", ',', '')) + 1 AS author_count
        FROM 
            "df0"
        WHERE 
            LENGTH("Authors") - LENGTH(REPLACE("Authors", ',', '')) + 1 > 3  
        ORDER BY 
            author_count DESC;  
    ''')
    table1 = cursor.fetchall()
   
    answer_11 = pd.DataFrame(table1, columns=["Book ID", "Title", "Authors", "Author Count"])

    st.dataframe(answer_11)
if a== '12.Books with Ratings Count Greater Than the Average':
    st.write(a)
    cursor.execute('''
    SELECT 
            "Book_id", 
            "Title", 
            "Ratings_count"
        FROM 
            "df0"
        WHERE 
            "Ratings_count" > (SELECT AVG("Ratings_count") FROM "df0" WHERE "Ratings_count" IS NOT NULL)  
        ORDER BY 
            "Ratings_count" DESC;  
    ''')

   
    table1 = cursor.fetchall()

    answer_12 = pd.DataFrame(table1, columns=["Book ID", "Title", "Ratings Count"])
    st.dataframe(answer_12)
if a== '13.Books with the Same Author Published in the Same Year':
    st.write(a)
    cursor.execute('''
    SELECT 
            "Authors", 
            "Published_Date", 
            COUNT(*) AS book_count
        FROM 
            "df0"
        WHERE 
            "Authors" IS NOT NULL 
            AND "Published_Date" IS NOT NULL
        GROUP BY 
            "Authors", "Published_Date"
        HAVING 
            COUNT(*) > 1  
        ORDER BY 
            "Published_Date" DESC, book_count DESC;
    ''')

   
    table1 = cursor.fetchall()

    
    answer_13 = pd.DataFrame(table1, columns=["Authors", "Published Year", "Book Count"])

    st.dataframe(answer_13)
if a== '14.Books with a Specific Keyword in the Title':
    st.write(a)

    st.title("Search Books by Title Keyword")

    keyword = st.text_input("Enter a keyword to search for in book titles:")
  
    query = '''
        SELECT 
        "Book_id", 
        "Title", 
        "Authors", 
        "Published_Date"
        FROM 
        "df0"
        WHERE 
        "Title" ILIKE %s
        ORDER BY 
        "Published_Date" DESC;
    '''

    cursor.execute(query, (f"%{keyword}%",))  # Parameterized query

    table1 = cursor.fetchall()
    answer_14 = pd.DataFrame(table1, columns=["Book ID", "Title", "Authors", "Published Date"])

        

    st.write(f"Books containing '{keyword}' in the title:")
    st.dataframe(answer_14)

if a=='15.Year with the Highest Average Book Price':
    st.write(a)


    st.title(" Year with the Highest Average Book Price")

    query = '''
      SELECT 
        EXTRACT(YEAR FROM "Published_Date"::DATE) AS year, 
        AVG("Retail_Price") AS avg_price
    FROM 
        "df0"
    WHERE 
        "Retail_Price" IS NOT NULL
        AND "Published_Date" ~ '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'  -- Ensure valid dates
    GROUP BY 
        year
    ORDER BY 
        avg_price DESC
    LIMIT 1;
    '''

    cursor.execute(query)
    result = cursor.fetchall()  

    
    answer_15 = pd.DataFrame(result, columns=["Year", "Average Price"])

   
    if not answer_15.empty:
        st.write(" Year with the Highest Average Book Price:")
        st.dataframe(answer_15)
if a== '16.Count Authors Who Published 3 Consecutive Years':  
    st.write(a)
    query = '''
    WITH author_years AS (
        SELECT 
            "Authors", 
            EXTRACT(YEAR FROM "Published_Date"::DATE) AS year
        FROM 
            "df0"
        WHERE 
            "Published_Date" ~ '^[0-9]{4}-[0-9]{2}-[0-9]{2}$' -- Ensure valid dates
        GROUP BY 
            "Authors", year
    )
    SELECT 
        COUNT(DISTINCT a1."Authors") AS author_count
    FROM 
        author_years a1
    JOIN 
        author_years a2 ON a1."Authors" = a2."Authors" AND a1.year = a2.year - 1
    JOIN 
        author_years a3 ON a1."Authors" = a3."Authors" AND a1.year = a3.year - 2;
    '''

    cursor.execute(query)
    table1 = cursor.fetchone()

    
    answer_16 = pd.DataFrame([table1], columns=["Authors with 3 Consecutive Years"])

    
    if not answer_16.empty:
        st.write("  Number of Authors Who Published 3 Consecutive Years:")
        st.dataframe(answer_16) 
        
if a== '17.Write a SQL query to find authors who have published books in the same year but under different publishers. Return the authors, year, and the COUNT of books they published in that year':
    st.write(a)


    st.title(" Authors with Books Published in the Same Year Under Different Publishers")


    
    query = '''
    SELECT 
        "Authors", 
        EXTRACT(YEAR FROM "Published_Date"::DATE) AS year, 
        COUNT(*) AS book_count
    FROM 
        "df0"
    WHERE 
        "Published_Date" ~ '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'  -- Valid date check
    GROUP BY 
        "Authors", year
    HAVING 
        COUNT(DISTINCT "Publisher") > 1  -- More than one publisher
    ORDER BY 
        year DESC, book_count DESC;
    '''

    cursor.execute(query)
    table17 = cursor.fetchall()

   
    answer_17 = pd.DataFrame(table17, columns=["Authors", "Year", "Book Count"])

   
    if not answer_17.empty:
        st.write(" Authors with Books Published in the Same Year Under Different Publishers:")
        st.dataframe(answer_17)

if a== '18.Create a query to find the average amount_retailPrice of eBooks and physical books. Return a single result set with columns for avg_ebook_price and avg_physical_price. Ensure to handle cases where either category may have no entries':

    st.write(a)
    

    st.title(" Average Retail Price of eBooks vs Physical Books")


    query = '''
    SELECT 
        COALESCE(AVG(CASE WHEN "Is_ebook" = TRUE THEN "Retail_Price" END), 0) AS avg_ebook_price,
        COALESCE(AVG(CASE WHEN "Is_ebook" = FALSE THEN "Retail_Price" END), 0) AS avg_physical_price
    FROM 
        "df0"
    WHERE 
        "Retail_Price" IS NOT NULL;
    '''

    cursor.execute(query)
    result = cursor.fetchone()

    
    if result:
        avg_ebook_price, avg_physical_price = result
        answer_18 = pd.DataFrame({
            "Category": ["eBooks", "Physical Books"],
            "Average Price": [avg_ebook_price, avg_physical_price]
        })

        # Display results
        st.write("Average Retail Price Comparison")
        st.dataframe(answer_18)

if a == '19.Write a SQL query to identify books that have an averageRating that is more than two standard deviations away from the average rating of all books. Return the title, averageRating, and ratingsCount for these outliers':
    st.write(a)
        
    

    st.title(" Books with Exceptional Ratings (Outliers)")


    
    query = '''
    WITH rating_stats AS (
        SELECT 
            AVG("Average_rating"::NUMERIC) AS avg_rating,
            STDDEV("Average_rating"::NUMERIC) AS stddev_rating
        FROM 
            "df0"
        WHERE 
            "Average_rating" ~ '^[0-9.]+$'
    )
    SELECT 
        "Title", 
        "Average_rating", 
        "Ratings_count"
    FROM 
        "df0", rating_stats
    WHERE 
        "Average_rating" ~ '^[0-9.]+$'
        AND ABS("Average_rating"::NUMERIC - rating_stats.avg_rating) > 2 * rating_stats.stddev_rating
    ORDER BY 
        "Average_rating" DESC;
    '''

    cursor.execute(query)
    table19 = cursor.fetchall()

    # Convert result to DataFrame
    if table19:
        answer_19 = pd.DataFrame(table19, columns=["Title", "Average Rating", "Ratings Count"])
        st.dataframe(answer_19)
    else:
        st.warning("⚠️ No outliers found in the dataset.")
    
if a== '20.Create a SQL query that determines which publisher has the highest average rating among its books, but only for publishers that have published more than 10 books. Return the publisher, average_rating, and the number of books published':
    st.write(a)
    

    st.title(" Publisher with the Highest Average Rating")
    
    query = '''
    WITH publisher_stats AS (
        SELECT 
            "Publisher",
            COUNT(*) AS book_count,
            AVG("Average_rating"::NUMERIC) AS avg_rating
        FROM 
            "df0"
        WHERE 
            "Average_rating" ~ '^[0-9.]+$'
        GROUP BY 
            "Publisher"
        HAVING 
            COUNT(*) > 10
    )
    SELECT 
        "Publisher",
        avg_rating,
        book_count
    FROM 
        publisher_stats
    ORDER BY 
        avg_rating DESC
    LIMIT 1;
    '''

    cursor.execute(query)
    table20 = cursor.fetchall()

    
    if table20:
        answer_20 = pd.DataFrame(table20, columns=["Publisher", "Average Rating", "Books Published"])
        st.dataframe(answer_20)
    else:
        st.warning("⚠️ No publisher found with more than 10 books.")

