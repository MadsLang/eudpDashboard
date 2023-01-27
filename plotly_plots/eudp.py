import pandas as pd
import plotly.express as px


class EUDP:

    def __init__(self):
        self.df_out =  pd.read_csv('data/data_with_topics.csv')

        self.color_dict = {}
        self.unique_topics = list(self.df_out['topics_name'].unique())
        self.noise_label = self.df_out[self.df_out['topics'] == -1]['topics_name'].values[0]
        for i in range(len(self.unique_topics)):

            if self.unique_topics[i] == self.noise_label:
                self.color_dict[self.unique_topics[i]] = "#ededed"
            else:
                self.color_dict[self.unique_topics[i]] = px.colors.qualitative.Dark24[i]



    def cluster_documents(self):
        fig = px.scatter(self.df_out, 
            x='x', 
            y='y', 
            color='topics_name', 
            hover_data=['text_br','Bevillingsår','Fælles overordnet teknologiområde','Ansvarlig virksomhed','Fokusområder EUDP'], 
            width=800, 
            height=600,
            color_discrete_map=self.color_dict,
            template='plotly_white', 
        )
        fig.update_traces(marker={'size': 5})
        fig.update_layout(
            showlegend=False,
            xaxis_title=None,
            yaxis_title=None
        )

        for t in list(self.df_out['topics_name'].unique()):
            if t != 'Ikke Kategoriseret':
                temp = self.df_out[self.df_out['topics_name'] == t]

                fig.add_annotation( # add a text callout with arrow
                    text=t, 
                    x=temp['x'].mean(), 
                    y=temp['y'].mean(), 
                    showarrow=False,
                )

        return fig
    
    def cluster_freqs(self):
        temp = self.df_out.groupby('topics_name').count()['ID'].reset_index().sort_values('ID', ascending=False)
        temp = temp.rename(
            columns={
            'ID': 'Antal',
            'topics_name': 'Navn på tema'
            }
        )

        fig = px.bar(
            temp,
            x = 'Antal',
            y = 'Navn på tema',
            color='Navn på tema',
            width=800, 
            height=600,
            color_discrete_map=self.color_dict,
            template='plotly_white', 
        )
        fig.update_layout(
            showlegend=False,
            xaxis_title=None,
            yaxis_title=None
        )

        return fig
    
    def clusters_over_time(self):
        temp = self.df_out.groupby(['topics_name','Slut (år)']).count()['ID'].reset_index().sort_values('ID', ascending=False)

        temp = temp.rename(
            columns={
            'ID': 'Antal',
            'topics_name': 'Navn på tema',
            }
        ).sort_values(['Slut (år)','Navn på tema'])

        fig = px.line(
            temp,
            x = 'Slut (år)',
            y = 'Antal',
            color='Navn på tema',
            width=800, 
            height=600,
            markers=True,
            color_discrete_map=self.color_dict,
            template='plotly_white', 
        )
        fig.update_layout(
            showlegend=True,
            xaxis_title=None,
            yaxis_title=None,
            yaxis_range=[0,35],
            xaxis_range=[2015,2022]
        )

        return fig
    
    def clusters_subsidy(self):
        temp = self.df_out.rename(columns={
            'topics_name': 'Navn på emne',
            'Subsidy_total': 'Tilskud'
        })

        fig = px.strip(
            temp,
            y='Navn på emne',
            x='Tilskud',
            color='Navn på emne',
            stripmode='overlay',
            hover_data=['text_br','Bevillingsår','Fælles overordnet teknologiområde','Ansvarlig virksomhed','Fokusområder EUDP'], 
            width=800, 
            height=600,
            color_discrete_map=self.color_dict,
            template='plotly_white', 
        )
        fig.update_layout(
            showlegend=False,
            xaxis_title='Tilskud (mio. kr)',
            yaxis_title=None
        )

        return fig
    
    def clusters_total_financing(self):
        temp = self.df_out.rename(columns={
            'topics_name': 'Navn på emne',
            'Total_financing': 'Samlet beløb'
        })

        fig = px.strip(
            temp,
            y='Navn på emne',
            x='Samlet beløb',
            color='Navn på emne',
            stripmode='overlay',
            hover_data=['text_br','Bevillingsår','Fælles overordnet teknologiområde','Ansvarlig virksomhed','Fokusområder EUDP'], 
            width=800, 
            height=600,
            color_discrete_map=self.color_dict,
            template='plotly_white', 
        )
        fig.update_layout(
            showlegend=False,
            xaxis_title='Samlet beløb (mio. kr)',
            yaxis_title=None
        )

        return fig