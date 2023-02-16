import streamlit as st
from plotly_plots.eudp import EUDP


st.title("Indsigter i EUDP Projekter")



eudp = EUDP()



st.markdown(
    """
    Dette dashboard viser en explorativ mini-analyse til at undersøge hvilke undertemaer, der findes i de EUDP-støttede projekter. 
    Der er kun medtaget projekter, som har slut-år i perioden 2015-2022, og IEA-projekter er udeladt. 
    \n
    For at undersøge hvilke emner, der findes, er lavet en cluster-analyse, som baseret på tekst fra projekttitel, intro-tekst, og evt. beskrivelse.
    Der bruges en unsupervised sprogmodel til at knytte projekterne sammen i grupper, der er sprogligt ens baseret på denne tekst. 

    -- Amsterdam Data Collective, 2023
    """
)

st.subheader("Hvilke emner har projekterne, som EUDP har støttet?")
color_var_option = st.selectbox(
    'Hvad skal projekterne farves efter?',
    ('Clusters','Fælles overordnet teknologiområde')
)
color_var_label_dict = {
    'Clusters': 'topics_name',
    'Fælles overordnet teknologiområde': 'Fælles overordnet teknologiområde'
}

label_bool = st.checkbox(
    'Tilføj navne på clusters?', 
    value=True
)
legend_bool = st.checkbox(
    'Tilføj dataforklaring?', 
    value=False
) 
st.plotly_chart(
    eudp.cluster_documents(
        color_var=color_var_label_dict.get(color_var_option),
        add_labels=label_bool,
        show_legend=legend_bool
    )
)

st.subheader("Antal projekter inden for hvert emne")
st.plotly_chart(
    eudp.cluster_freqs()
)

st.subheader('Hvad ligger inden for "Ikke kategoriseret"?')
groupby_var_option = st.selectbox(
    'Hvilken variabel skal grupperes?',
    ('Fælles overordnet teknologiområde','Bevillingsår','Slut (år)','Fokusområder EUDP')
)
st.plotly_chart(
    eudp.explore_noise_category(
        groupby_var=groupby_var_option
    )
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

sort_by = st.selectbox("Sortér efter:", ['Samlet tilskud','Antal projekter'])

temp = eudp.df_out[eudp.df_out['topics_name'].apply(lambda x: x in options)]

table = temp.groupby('Ansvarlig virksomhed')['Subsidy_total'].agg(['sum','count']).reset_index().rename(columns={'sum': 'Samlet tilskud', 'count': 'Antal projekter'})
table = table.sort_values(sort_by, ascending=False)

hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """
# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)

st.table(table)