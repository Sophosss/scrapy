import psycopg2 

conn = psycopg2.connect(database='SYH',user='postgres',password='bigdata123',host='10.20.1.50',port='5432')  
cur = conn.cursor()  

def get_keywords():
    cur.execute("SELECT * FROM biz_keyword;")  
    rows = cur.fetchall() 
    return rows

def save_keyword_index(data):
    cur.execute('SELECT * FROM biz_keyword_index where keyword_id=%s and index_date=\'%s\' and site=\'%s\';' % (data['keyword_id'],data['index_date'],data['site']))  
    rows = cur.fetchall() 
    if not len(rows):
        # print('save:',data['index_date'])
        cur.execute("INSERT INTO biz_keyword_index (keyword_id,site,keyword_type,index_date,index_value) values (%s,\'%s\',%s,\'%s\',%s);" % (data['keyword_id'],data['site'],data['keyword_type'],data['index_date'],data['index_value']))  
        conn.commit()
    return rows