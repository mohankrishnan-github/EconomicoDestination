from plotly.graph_objs import Layout
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from chart_studio.plotly import plotly as py
import seaborn as sns
import processReviews
import plotly



def barplot_ratings(dfs):
    """
    INPUT:
    dfs: dataframes of airlines to use for mean representation of particular
        attribute of flight rating

    OUTPUT:
    figure with barplot subplots of mean star rating for each attribute among
        airlines
    """
    southwest_df, american_df, delta_df, united_df, ana_df, japan_df, qatar_df = dfs
    fig, ax = plt.subplots(figsize=(20, 10), ncols=5, nrows=2)
    i, j = 0, 0
    for col in southwest_df._get_numeric_data().columns[1:-2]:
        ax[i][j].set_title(col.replace('_', ' ').title())
        ax[i][j].set_ylim([0, 5])
        if j == 4:
            ax[i][j].set_ylim([0, 10])
        elif col == 'positive':
            ax[i][j].set_ylim([0, 1])
        sns.barplot(x=['Southwest Airlines', 'American Airlines',
                       'Delta Air Lines', 'United Airlines',
                       'All Nippon Airways', 'Japan Airlines',
                       'Qatar Airways'],
                    y=[southwest_df[col].mean(), american_df[col].mean(),
                       delta_df[col].mean(), united_df[col].mean(),
                       ana_df[col].mean(), japan_df[col].mean(),
                       qatar_df[col].mean()], palette='magma', ax=ax[i, j])
        j += 1
        if j >= 5:
            j = 0
            i = 1
    for i, ax in enumerate(fig.axes):
        ax.set_xticklabels(ax.get_xticklabels(), rotation=42)
    plt.tight_layout()
    plt.show()


def single_barplot(dfs, col, palette='magma'):
    """
    INPUT:
    dfs: dataframes of airlines to take data of a particular attribute of
        flight review
    col: specified attribute to create barplot on
    palette: colormap sequence for use on graph

    OUTPUT
    barplot with average rating of col for all airlines!
    """
    labels = ['Southwest Airlines', 'American Airlines', 'Delta Air Lines',
              'United Airlines', 'All Nippon Airways', 'Japan Airlines',
              'Qatar Airways']
    sns.barplot(x=labels,
                y=[southwest_df[col].mean(), american_df[col].mean(),
                   delta_df[col].mean(), united_df[col].mean(),
                   ana_df[col].mean(), japan_df[col].mean(),
                   qatar_df[col].mean()], palette=palette)
    if col == 'positive':
        plt.ylim(0, 1)
    else:
        plt.ylim(0, 5)
    plt.xticks(range(0, 7), labels, rotation='vertical')
    plt.title(col.replace('_', ' ').title())
    plt.tight_layout()
    plt.show()


def single_countplot(df, col, airline, palette='magma'):
    """
    INPUT:
    df: dataframe of airline to take data from
    col: specified attribute to create a countplot on
    airline: airline name in string format to pass to graph title
    palette: colormap sequence for use on graph

    OUTPUT:
    countplot of reviews with given rating for attribute (col) for specific
        airline
    """
    sns.countplot(df[col], palette=palette)
    plt.title(f"{airline} : {col.replace('_',' ').title()}")
    plt.show()


def boxplot_ratings(dfs, col):
    """
    INPUT:
    dfs: dataframes of airlines to take data of a particular attribute of
        flight review
    col: specified attribute to create boxplot on

    OUTPUT:
    boxplots, displayed in webpage, for each airline based on col attribute
    """

    southwest_df, american_df, delta_df, united_df, ana_df, japan_df, qatar_df = dfs

    y0 = southwest_df[col]
    y1 = american_df[col]
    y2 = delta_df[col]
    y3 = united_df[col]
    y4 = ana_df[col]
    y5 = japan_df[col]
    y6 = qatar_df[col]

    trace0 = go.Box(y=y0, name='Southwest Airlines')
    trace1 = go.Box(y=y1, name='American Airlines')
    trace2 = go.Box(y=y2, name='Delta Air Lines')
    trace3 = go.Box(y=y3, name='United Airlines')
    trace4 = go.Box(y=y4, name='All Nippon Airways')
    trace5 = go.Box(y=y5, name='Japan Airlines')
    trace6 = go.Box(y=y6, name='Qatar Airways')

    data = [trace0, trace1, trace2, trace3, trace4, trace5, trace6]

    plotly.offline.plot({
        "data": data,
        "layout": Layout(title=f"Ratings ({col.replace('_', ' ').title()})")
    })


def rating_dist(df, airline):
    """
    INPUT:
    df: which airline we would like to analyze
    airline: name of the airline as a string

    OUTPUT:
    subplots of countplot for each attribute to see distribution of possible
        rating options
    """
    fig, ax = plt.subplots(figsize=(20, 10), ncols=5, nrows=2)
    i, j = 0, 0
    for col in df._get_numeric_data().columns[1:-2]:
        ax[i][j].set_title(f"{airline} : {col.replace('_', ' ').title()}")
        sns.countplot(df[col], ax=ax[i, j], palette='magma')
        j += 1
        if j >= 5:
            j = 0
            i = 1
    # for i, ax in enumerate(fig.axes):
    #     ax.set_xticklabels(ax.get_xticklabels(), rotation = 90)
    plt.tight_layout()
    plt.show()


def violin_ratings(dfs, col, country='United States'):
    """
    INPUT:
    dfs: dataframes of all airlines
    col: attribute of airline reviews to analyze

    OUTPUT:
    violin plots of 'col' data for each airline split on country of origin
        (USA or other)
    """
    fig, ax = plt.subplots(figsize=(20, 10), ncols=4, nrows=2)
    i, j = 0, 0
    airlines = ['Southwest Airlines', 'American Airlines', 'Delta Air Lines',
                'United Airlines', 'All Nippon Airways', 'Japan Airlines',
                'Qatar Airways']
    for ind, df in enumerate(dfs):
        df['Country of Origin'] = df['country'] == country
        df['Country of Origin'] = df['Country of Origin'].apply(
            lambda x: country if x is True else 'Other')
        df[''] = airlines[ind]
        df.sort_values(by=['Country of Origin'], ascending=0, inplace=True)
        ax[i][j].set_title(f"{airlines[ind]} : {col.replace('_', ' ').title()}")
        sns.violinplot(x='', y=col, hue='Country of Origin', data=df,
                       palette='coolwarm', ax=ax[i, j], split=True)
        j += 1
        if j >= 4:
            j = 0
            i = 1
    plt.tight_layout()
    plt.show()


def rating_by_year(dfs, rating='rating'):
    """
    INPUT:
    dfs: dataframes of all airlines

    OUTPUT:
    graph plotting mean rating by year (2015,2016,2017) for each airline
    """
    sns.set()
    markers = ['p', '*', '^', 'H', 'P', 'o', 'X']
    colors = ['b', 'r', 'g', 'c', 'm', 'k', 'y']
    airlines = ['Southwest Airlines', 'American Airlines', 'Delta Air Lines',
                'United Airlines', 'All Nippon Airways', 'Japan Airlines',
                'Qatar Airways']
    i = 0
    for df in dfs:
        dates = [2015, 2016, 2017]
        values = [
            df[df['year'] == 2015][rating].mean(),
            df[df['year'] == 2016][rating].mean(),
            df[df['year'] == 2017][rating].mean()
        ]

        xticks = [2015, 2016, 2017]
        ticklabels = ['2015', '2016', '2017']
        plt.xticks(xticks, ticklabels)

        yticks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        ticklabels_y = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        plt.yticks(yticks, ticklabels_y)

        plt.xlim(2014.9, 2017.1)
        plt.ylim(2, 9)

        plt.plot(dates, values, f'{markers[i]}{colors[i]}-.',
                 markersize=12, label=airlines[i])

        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
                   ncol=3, mode="expand", borderaxespad=0.)
        i += 1
    plt.show()


def united_incident(united_df):
    """
    INPUT:
    united_df: dataframe of united datapoints

    OUTPUT:
    graph plotting mean rating by month in 2017 highlighting effects of
        incidents by united
    """
    sns.set()
    dates = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    values = [
        united_df[
            (united_df['month'] == 1) & (united_df['year'] == 2017)
        ]['rating'].mean(),
        united_df[
            (united_df['month'] == 2) & (united_df['year'] == 2017)
        ]['rating'].mean(),
        united_df[
            (united_df['month'] == 3) & (united_df['year'] == 2017)
            ]['rating'].mean(),
        united_df[
            (united_df['month'] == 4) & (united_df['year'] == 2017)
            ]['rating'].mean(),
        united_df[
            (united_df['month'] == 5) & (united_df['year'] == 2017)
            ]['rating'].mean(),
        united_df[
            (united_df['month'] == 6) & (united_df['year'] == 2017)
            ]['rating'].mean(),
        united_df[
            (united_df['month'] == 7) & (united_df['year'] == 2017)
            ]['rating'].mean(),
        united_df[
            (united_df['month'] == 8) & (united_df['year'] == 2017)
            ]['rating'].mean(),
        united_df[
            (united_df['month'] == 9) & (united_df['year'] == 2017)
            ]['rating'].mean(),
        united_df[
            (united_df['month'] == 10) & (united_df['year'] == 2017)
            ]['rating'].mean(),
        united_df[
            (united_df['month'] == 11) & (united_df['year'] == 2017)
            ]['rating'].mean(),
        united_df[
            (united_df['month'] == 12) & (united_df['year'] == 2017)
            ]['rating'].mean()]

    xticks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    ticklabels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 
                  'Sept', 'Oct', 'Nov', 'Dec']
    plt.xticks(xticks, ticklabels, rotation=90)

    yticks = [1, 2, 3, 4]
    ticklabels_y = ['1', '2', '3', '4']
    plt.yticks(yticks, ticklabels_y)

    plt.xlim(1, 12)
    plt.ylim(1, 4)

    plt.title('Overall Rating by Month (United Airlines - 2017)')
    plt.plot(dates, values, 'ob--', label='Mean Rating')
    plt.plot(4+9/30, 3.04, marker='P', color='r',
             markersize=15, label='incident')
    plt.plot(9+7/30, 3.13, marker='X', color='r',
             markersize=15, label='exoneration')

    plt.legend(bbox_to_anchor=(1, 0.1, -.01, 0),
               ncol=3, borderaxespad=0.)

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    southwest_df, american_df, delta_df, united_df, ana_df, japan_df, qatar_df, dfs = pull_data.get_data()
    barplot_ratings(dfs)
    boxplot_ratings(dfs, 'value_for_money')
    rating_dist(united_df, 'United Airlines')
    violin_ratings(dfs, 'rating', 'United States')
    rating_by_year(dfs, 'rating')
    united_incident(united_df)
    single_countplot(ana_df, 'rating', 'All Nippon Airlines', 'Greens')
    single_barplot(dfs, 'ground_service', palette='YlGnBu_r')
