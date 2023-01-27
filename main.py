import streamlit as st
from plotly_plots.eudp import EUDP


st.title("Indsigter i EUDP Projekter")



eudp = EUDP()



st.markdown("Her kan tilføjes en lille beskrivelse")

st.subheader("Hvilke emner har projekterne, som EUDP har støttet?")
st.plotly_chart(
    eudp.cluster_documents()
)


st.subheader("Antal projekter inden for hvert emne")
st.plotly_chart(
    eudp.cluster_freqs()
)


st.subheader("Hvilke emner er støttet over tid?")
st.plotly_chart(
    eudp.clusters_over_time()
)

st.subheader("Hvilke emner har fået mest tilskud?")
option_tilskud = st.selectbox(
    'Vis tilskud for projekter eller samlet',
    ('Projekter','Samlet')
)
if option_tilskud == 'Projekter':
    st.plotly_chart(
        eudp.clusters_subsidy()
    )
else:
    st.plotly_chart(
        eudp.clusters_subsidy_sum()
    )

st.subheader("Hvilke emner har størst budget? (Inkl. EUDP-tilskud, egenfinansiering og anden finansiering)")
option_budget = st.selectbox(
    'Vis budget for projekter eller samlet',
    ('Projekter', 'Samlet')
)
if option_budget == 'Projekter':
    st.plotly_chart(
        eudp.clusters_total_financing()
    )
else:
    st.plotly_chart(
        eudp.clusters_total_financing_sum()
    )


st.subheader("Hvem er de ansvarlige virksomheder inden for hvert emne?")
options = st.multiselect(
    'Vælg et eller flere emner',
    list(eudp.df_out['topics_name'].unique()),
    list(eudp.df_out['topics_name'].unique()),
)

temp = eudp.df_out[eudp.df_out['topics_name'].apply(lambda x: x in options)]

table = temp['Ansvarlig virksomhed'].value_counts().reset_index().rename(columns={'Ansvarlig virksomhed': 'Antal'}).rename(columns={'index': 'Ansvarlig virksomhed'})

hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """
# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)

st.table(table)