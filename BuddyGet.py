import streamlit as st
import pandas as pd
import plotly.express as px

#Tytuł aplikacji
st.title("BuddGet - asystent twoich finansów💰")
# Przygotowanie "słownika"
if 'wydatki' not in st.session_state:
    st.session_state['wydatki'] = {
        'Jedzenie': 0,
        'Transport': 0,
        'Czynsz': 0,
        'Rozrywka': 0,
        'Nauka': 0,
        'Inne': 0
    }

# Panel boczny - tutaj dodajemy nowy produkt
st.sidebar.header('Dodaj nowy wydatek')
# Pobieramy kategorie z kluczy naszego słownika
kategorie_lista = list(st.session_state['wydatki'].keys())
new_category = st.sidebar.selectbox('Kategoria', kategorie_lista)
new_price = st.sidebar.number_input('Kwota [PLN]', min_value=0, value=50)

if st.sidebar.button('Dodaj do listy'):
    st.sidebar.success(f'Dodano: {new_category} - {new_price} PLN')
    st.session_state['wydatki'][new_category] += new_price
    #potem dodać baze danych i przekazanie wartości
        

# Zamiana danych na tabelę (DataFrame)
to_table = list(st.session_state['wydatki'].items())
df = pd.DataFrame(to_table, columns=['Kategoria', 'Kwota [PLN]'])

st.sidebar.divider()
st.sidebar.header('Wgraj dane')
uploaded_file = st.sidebar.file_uploader('Wybierz plik CSV', type=['csv'])

if uploaded_file is not None:
    if st.sidebar.button('Załaduj CSV'):
        try:
            df_upload = pd.read_csv(uploaded_file)

            if 'Kategoria' in df_upload.columns and 'Kwota [PLN]' in df_upload.columns:
                for index, row in df_upload.iterrows():
                    category = row['Kategoria']
                    price = row['Kwota [PLN]']

                    if category in st.session_state['wydatki']:
                        st.session_state['wydatki'][category] += price
                    else:
                        # Jak kategoria jest dziwna, wrzucamy do Inne
                        st.session_state['wydatki']['Inne'] += price

                st.rerun()
            else:
                st.sidebar.error("Błąd: Plik musi mieć kolumny 'Kategoria' i 'Kwota [PLN]'")
        except Exception as e:
            st.sidebar.error(f"Coś poszło nie tak: {e}")

col1, col2 = st.columns(2, vertical_alignment = 'center') #podział na 2 kolumny, wyśrodkowanie

# Wyświetlamy prosty wykres słupkowy
with col1:
    st.write("Tabela z wydatakmi:")
    st.dataframe(df)
with col2:
    st.write('Wykres:')
    if df['Kwota [PLN]'].sum() > 0:
        fig = px.pie(df, values='Kwota [PLN]', names='Kategoria')
        st.plotly_chart(fig,use_container_width=True)
    else:
        st.info('Aby wyświetlić wykres dodaj pierwszy wydatek')

#Podsumowanie budżetu
limit = 2000 #pozniej dodac wybór limitu
b_sum = df['Kwota [PLN]'].sum()
st.metric(label="Łączne wydatki", value=f"{b_sum} PLN")

#pasek budżetu
left = limit - b_sum
percent = b_sum/limit

if percent > 1.0:
    percent = 1.0 #blokada paska 

col_sum1, col_sum2, col_sum3 = st.columns(3)
col_sum1.metric('Wydano', f'{b_sum} PLN')
col_sum2.metric('Limit', f'{limit} PLN')
col_sum3.metric('Pozostało', f'{left} PLN')

st.progress(percent)
st.write(f'Zużycie budżetu: {int(percent * 100)}%')

#eksport do csv
st.header('Eksport danych - CSV (Excel)')
csv_data = df.to_csv(index=False).encode('utf-8')

st.download_button(
    label = 'Pobierz dane',
    data = csv_data,
    file_name = 'moj_budzet.csv',
    mime = 'text/csv' 
)