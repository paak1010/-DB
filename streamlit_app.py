import streamlit as st
import pandas as pd

st.title("마당서점 주문 검색 (Streamlit)")

# 1. st.connection을 사용하여 secrets.toml에 설정된 DB에 연결
# "mydb"라는 이름의 연결 정보를 secrets.toml에서 가져옵니다.
try:
    conn = st.connection("mydb", type="sql") # <--- 이 부분이 secrets.toml의 [mydb] 섹션을 사용합니다.
except Exception as e:
    st.error(f"데이터베이스 연결 설정에 문제가 있습니다: {e}")
    st.stop()


# 2. 사용자 입력 받기
customer_name = st.text_input("주문 내역을 검색할 고객 이름을 입력하세요:", key="name_input")
search_button = st.button("검색")


# 3. 검색 로직
if search_button and customer_name:
    # 쿼리 작성 (SQL 파라미터 처리로 보안 강화)
    sql = """
    SELECT 
        o.orderid, 
        c.name, 
        b.bookname, 
        o.saleprice, 
        o.orderdate 
    FROM 
        Customer c, Orders o, Book b
    WHERE 
        c.name = %s 
        AND c.custid = o.custid 
        AND b.bookid = o.bookid;
    """
    
    try:
        # conn.query를 사용하여 DB에서 데이터를 가져옵니다.
        # params=[customer_name]로 SQL 인젝션을 방지합니다.
        df = conn.query(sql, params=[customer_name], ttl=600) 

        if not df.empty:
            st.success(f"'{customer_name}'님의 주문 내역 ({len(df)}건)을 찾았습니다.")
            st.dataframe(df)
        else:
            st.warning(f"'{customer_name}'님의 주문 내역을 찾을 수 없습니다.")

    except Exception as e:
        st.error(f"쿼리 실행 중 오류가 발생했습니다: {e}")
