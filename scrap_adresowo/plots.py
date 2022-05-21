import pandas as pd
from scrap_adresowo.models import session_maker, Apartment
import matplotlib.pyplot as plt
from collections import Counter

session = session_maker()


query = session.query(Apartment)
apartments_df = pd.read_sql(query.statement, query.session.bind)
cracow_apartments_df = apartments_df[apartments_df['city'] == 'Kraków']
# basic stats
df = cracow_apartments_df[['price', 'rooms', 'floor', 'squares', 'price_per_square']]
d = {'Mean': df.mean(), 'Min': df.min(), 'Max': df.max(), 'Median': df.median()}
stats = pd.DataFrame.from_dict(d, dtype='int32')[["Min", "Max", "Mean", "Median"]].transpose()
print(stats)

# avg price per district
df_mean = cracow_apartments_df.groupby(['district']).mean()
df_mean['price'] = df_mean['price'].astype(int)
fig, (ax, ax2) = plt.subplots(ncols=2, sharey=False)
ax.ticklabel_format(useOffset=False, style='plain')
ax2.ticklabel_format(useOffset=False, style='plain')
df_mean[:20].plot.barh(x=None, y="price", color="royalblue", ax=ax, grid=True, )
df_mean[:20].plot.barh(x=None, y="price_per_square", color="red", ax=ax2, grid=True, )

# Correlation between price_per_square and floor in cracow
y = cracow_apartments_df["price_per_square"].tolist()
x = cracow_apartments_df["floor"].tolist()
c = Counter(zip(x, y))
s = [10 * c[(xx, yy)] for xx, yy in zip(x, y)]
fig1, ax = plt.subplots()
ax.ticklabel_format(useOffset=False, style='plain')
cracow_apartments_df.plot(kind="scatter", x="floor", y="price_per_square", s=s, color="blue", ax=ax)
yy, locs = plt.yticks()
ll = ['%.0f' % a for a in yy]
plt.yticks(yy, ll)

# Correlation between price_per_square and squares in cracow
y = cracow_apartments_df["price_per_square"].tolist()
x = cracow_apartments_df["squares"].tolist()
c = Counter(zip(x, y))
s = [10 * c[(xx, yy)] for xx, yy in zip(x, y)]
fig1, ax = plt.subplots()
ax.ticklabel_format(useOffset=False, style='plain')
cracow_apartments_df.plot(kind="scatter", x="squares", y="price_per_square", s=s, color="blue", ax=ax)
yy, locs = plt.yticks()
ll = ['%.0f' % a for a in yy]
plt.yticks(yy, ll)


# ratio of rooms in cracow
fig1, ax1 = plt.subplots()
ax1.ticklabel_format(useOffset=False, style='plain')
df_count = cracow_apartments_df.groupby(['rooms']).count()
df_to_delete = df_count[df_count['id'] < df_count['id'].sum() / 50]  # below 2%
df_count = df_count[df_count['id'] > df_count['id'].sum() / 50]
df_count = df_count['id']
df_count.append(pd.Series([df_to_delete['id'].sum()]), ignore_index=True)
df_count.index = [f"{i} pokojowe" for i in df_count.index[:-1]] + ['pozostałe']


df_count.plot.pie(y="id", autopct="%1.1f%%", figsize=(7, 7))


# Stats of cities
cities_df = apartments_df.groupby(['city']).mean()
fig1, ax1 = plt.subplots()
ax1.ticklabel_format(useOffset=False, style='plain')
cities_df[:15].plot.barh(x=None, y="price", color="royalblue", ax=ax1, grid=True)


plt.show()
session.close()
