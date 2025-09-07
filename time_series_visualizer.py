import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

# cara, por algum motivo divino ta dando erro no numpy, sendo q o numpy n foi nem importado, eu n sei como nem porque, esse codigo em baixo corrige o erro de n existir atributo 'float' no numpy (sendo q tem?), sei la.
try:
    import numpy as np
    if not hasattr(np, 'float'): # isso aq basicamente checa se 'np.float' existe, isso retorna falso nas versoes mais novas do numpy
        np.float = float # pra n ter erro, a gente faz com q 'np.float' seja igual a 'float' q ja eh built in no python
except ImportError:
    pass
# basicamente, tudo isso eh por causa de incompatibilidade de versao, por isso q eu gosto de Docker e venv, ai n teria esse erro

register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
# importar os dados colocando as datas como indices
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# Clean data
# tirar os outliers os 2.5% menores e 2.5% maiores 
df = df[
    (df['value'] >= df['value'].quantile(0.025)) & 
    (df['value'] <= df['value'].quantile(0.975))
]


def draw_line_plot():
    # Draw line plot
    # plota o grafico
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df.index, df['value'], color='red', linewidth=1) # faz uma linha vermelha conectando todos os pontos
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019') # coloca o titulo e as labels
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')


    # Save image and return fig (don't change this part)
    # salva o grafico como uma image
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    # copia dados e adiciona as colunas de 'ano' e 'mes'
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack() # agrupa por ano e mes, calcula a media e reorganiza as colunas

    # Draw bar plot
    # plota o grafico
    fig, ax = plt.subplots(figsize=(15, 8))
    df_bar.plot(kind='bar', ax=ax)
    ax.set_title('Media das Visualizacoes Diaria da Pagina por Mes')
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.legend(title='Months', labels=['January', 'February', 'March', 'April', 'May', 'June', 
                                      'July', 'August', 'September', 'October', 'November', 'December'])
    ax.set_xticklabels(df_bar.index, rotation=0)

    # Save image and return fig (don't change this part)
    # salva o grafico como imagem
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    # prepara os dados criando as colunas de ano e mes
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    # faz um box plot usando o seaborn
    # dois subplots lado a lado
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # Year-wise box plot
    # grafico do ano
    sns.boxplot(data=df_box, x='year', y='value', ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')
    
    # Month-wise box plot
    # grafico do mes
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    sns.boxplot(data=df_box, x='month', y='value', order=month_order, ax=axes[1])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')


    # Save image and return fig (don't change this part)
    # salva o grafico como imagem
    fig.savefig('box_plot.png')
    return fig


# Coisas q podem ser melhoradas
#
#   tem como fazer o cacheamento de quantis pra calcular somente uma vez
#   fazer o uso de 'Categorical' para 'month'
#   tem como fazer um agrupamento mais eficiente usando 'agg'
#   da pra fazer uma pre-alocacao de arrays
#   deve dar pra deixar o runtime como O(n) ou O(n log n)
#