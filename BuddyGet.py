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
suma = df['Kwota [PLN]'].sum()
st.metric(label="Łączne wydatki", value=f"{suma} PLN")
