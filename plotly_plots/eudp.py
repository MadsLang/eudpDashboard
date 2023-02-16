import pandas as pd
import plotly.express as px
import random
import re


class EUDP:

    def __init__(self):
        self.df_out =  pd.read_csv('data/data_with_topics.csv')
        self.df_out['Ansvarlig virksomhed'] = self.df_out['Ansvarlig virksomhed'].apply(self.fix_company_names)

        self.color_dict = {}
        self.unique_topics = list(self.df_out['topics_name'].unique())
        self.noise_label = self.df_out[self.df_out['topics'] == -1]['topics_name'].values[0]
        for i in range(len(self.unique_topics)):

            if self.unique_topics[i] == self.noise_label:
                self.color_dict[self.unique_topics[i]] = "#ededed"
            else:
                try:
                    self.color_dict[self.unique_topics[i]] = px.colors.qualitative.Dark24[i]
                except IndexError:
                    new_i = random.randint(0,len(px.colors.qualitative.Dark24))
                    self.color_dict[self.unique_topics[i]] = px.colors.qualitative.Dark24[new_i]

    
    def fix_company_names(self, company_name: str) -> str:
        if any([i in company_name for i in ['DTU', 'Danmarks Tekniske Universitet','Technical University of Denmark']]):
            return 'Danmarks Tekniske Universitet (DTU)'
        elif 'SIEMENS WIND POWER A/S' in company_name:
            return 'Siemens Gamesa Renuable Energy A/S'
        elif 'AAU' in company_name:
            return 'Aalborg Universitet' 
        elif 'Rambøll' in company_name:
            return 'RAMBØLL DANMARK A/S'
        elif 'Mærsk' in company_name:
            return 'A.P. MØLLER - MÆRSK A/S'
        else:
            parenthesis = re.findall('\(.+\)', company_name)
            for match in parenthesis:
                company_name = company_name.replace(match, '')
            return company_name.strip()

    def cluster_documents(self, color_var = 'topics_name', add_labels = True, show_legend = False):
        if color_var == 'topics_name':
            fig = px.scatter(self.df_out, 
                x='x', 
                y='y', 
                color=color_var, 
                hover_data=['text_br','Bevillingsår','Fælles overordnet teknologiområde','Ansvarlig virksomhed','Fokusområder EUDP'], 
                width=800, 
                height=600,
                color_discrete_map=self.color_dict,
                template='plotly_white', 
            )
        else:
            fig = px.scatter(self.df_out, 
                x='x', 
                y='y', 
                color=color_var, 
                hover_data=['text_br','Bevillingsår','Fælles overordnet teknologiområde','Ansvarlig virksomhed','Fokusområder EUDP'], 
                width=800, 
                height=600,
                color_discrete_sequence=px.colors.qualitative.Dark24,
                template='plotly_white', 
            )


        fig.update_traces(marker={'size': 5})
        fig.update_layout(
            showlegend=show_legend,
            xaxis_title=None,
            yaxis_title=None
        )

        if add_labels:
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

    def explore_noise_category(self, groupby_var):
        temp = self.df_out[self.df_out['topics'] == -1]
        temp = temp.groupby(groupby_var).count()['ID'].reset_index()
        
        temp = temp.rename(
            columns={
            'ID': 'Antal'
            }
        )

        fig = px.bar(
            temp,
            x = groupby_var,
            y = 'Antal',
            color_discrete_sequence=["#ededed"],
            width=800, 
            height=600,
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
        }).sort_values('Navn på emne')

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
    
    def clusters_subsidy_sum(self):
        temp = self.df_out.groupby('topics_name').sum()['Subsidy_total'].reset_index()

        temp = temp.rename(columns={
            'topics_name': 'Navn på emne',
            'Subsidy_total': 'Tilskud samlet'
        }).sort_values('Navn på emne')

        fig = px.bar(
            temp,
            x = 'Tilskud samlet',
            y = 'Navn på emne',
            color='Navn på emne',
            width=800, 
            height=600,
            color_discrete_map=self.color_dict,
            template='plotly_white', 
        )
        fig.update_layout(
            showlegend=False,
            xaxis_title='Tilskud samlet (mio. kr)',
            yaxis_title=None
        )

        return fig
    
    def clusters_total_financing(self):
        temp = self.df_out.rename(columns={
            'topics_name': 'Navn på emne',
            'Total_financing': 'Samlet beløb'
        }).sort_values('Navn på emne')

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
    
    def clusters_total_financing_sum(self):
        temp = self.df_out.groupby('topics_name').sum()['Total_financing'].reset_index()

        temp = temp.rename(columns={
            'topics_name': 'Navn på emne',
            'Total_financing': 'Samlet beløb'
        }).sort_values('Navn på emne')

        fig = px.bar(
            temp,
            x = 'Samlet beløb',
            y = 'Navn på emne',
            color='Navn på emne',
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