import streamlit as st
import pickle
import psycopg2

conn = psycopg2.connect(st.secrets["connection"])
cur = conn.cursor()
sql = """INSERT INTO feedback(help, input_items, output_items)
             VALUES(%s, %s, %s) RETURNING id;"""

file = open('model', 'rb')
data = pickle.load(file)
file.close()

st.title('Sistem Rekomendasi')

opt = data['items']
symbols = st.multiselect("Pilih item yang akan dibeli (Maksimal 2): ", opt, opt[:2], max_selections=2)

def find(items, frequent_itemsets):
  out = []
  for i in range(len(frequent_itemsets)):
    if set(items).issubset(frequent_itemsets['itemsets'].iloc[i]):
      out.extend(frequent_itemsets['itemsets'].iloc[i])
  out = list(set([x for x in out if x not in items])) 
  return out

res = find(symbols, data['model'])
st.write('Biasanya orang yang membeli ', symbols, 'juga membeli: ')
st.write(res)

with st.form("my_form"):
  helps = st.radio(
    "Apakah anda terbantu dengan rekomendasi ini?",
    ('Ya', 'Tidak'))

  submitted = st.form_submit_button("Submit")
  if submitted:
    h = 0
    if helps == 'Ya': h = 1 
    cur.execute(sql, (h, symbols, res))
    id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    st.write("Terima Kasih")