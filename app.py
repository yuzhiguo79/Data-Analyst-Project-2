import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.title('視覺圖表展示')

#讀取資料
order = pd.read_csv('data/raw/orders.csv')
items = pd.read_csv('data/raw/order_items.csv')
df = order.merge(items, on='order_id')

st.write('### 訂單明細表')  
st.write(df.head())

df['amount'] = df['quantity'] * df['unit_price'] * (1-df['discount_rate'])
df['order_date'] = pd.to_datetime(df['order_date'])

#取出訂單狀態
status_list = df['status'].unique()
status = st.selectbox("付款狀態", status_list)
data = df[ df['status']== status ]
st.write(data.head())

chart_type = st.selectbox("圖表選擇", 
                 ['每月銷售金額','付款-訂單數','訂單金額','不同付款方式小計'] )

#
if st.button("顯示圖表"):
    #st.info(chart_type)
    #線條圖
    if chart_type == '每月銷售金額':
        data = data.copy()
        data['month'] = data['order_date'].dt.to_period('M')
        m_sales = data.groupby('month')['amount'].sum()
        m_sales.index = m_sales.index.astype(str)

        fig,ax = plt.subplots()
        ax.plot(
            m_sales.index,
            m_sales.values,
            marker = 'o'
        )
        ax.set_title("Sales for month")
        ax.set_xlabel('month')
        ax.set_ylabel('$')
        st.pyplot(fig)

    #長條圖
    elif chart_type == '付款-訂單數':
        pay_count = data.groupby('payment_type')['order_id'].nunique()

        fig,ax = plt.subplots()
        ax.bar(
            pay_count.index,
            pay_count.values
        )
        ax.set_title("Count of payment type")
        ax.set_xlabel('payment_type')
        ax.set_ylabel('$')
        st.pyplot(fig)

    #直方圖
    elif chart_type == '訂單金額':
        order_amount = data.groupby('order_id')['amount'].sum()
        
        fig,ax = plt.subplots()
        ax.hist(
            order_amount,
            bins = 40
        )
        ax.set_title("Order Amount")
        ax.set_xlabel('order amount')
        ax.set_ylabel('$')
        st.pyplot(fig)

    #箱形圖
    elif chart_type == '不同付款方式小計':
        order_amount = (
            data.groupby(['order_id','payment_type'])['amount']
            .sum()
            .reset_index()
        )
        pays = order_amount['payment_type'].unique()
        boxdata = []
        for i in pays:
            values = order_amount[order_amount['payment_type'] == i]['amount']
            boxdata.append(values)

        fig,ax = plt.subplots()
        ax.boxplot(boxdata)

        ax.set_title("Payment type subtotal")
        ax.set_xlabel('payment_type')
        ax.set_ylabel('$')
        ax.set_xticks([1,2,3,4],['atm','card','cod','wallet'])
        st.pyplot(fig)
else:
    st.info("尚未選擇")




