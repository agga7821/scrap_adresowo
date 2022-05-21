import pandas as pd
from scrap_adresowo.models import session_maker, Apartment
import matplotlib.pyplot as plt

session = session_maker()


query = session.query(Apartment)
apartments_df = pd.read_sql(query.statement, query.session.bind)

# basic stats
df = apartments_df[['price', 'rooms', 'floor', 'squares', 'price_per_square']]
d = {'Mean': df.mean(), 'Min': df.min(), 'Max': df.max(), 'Median': df.median()}
stats = pd.DataFrame.from_dict(d, dtype='int32')[["Min", "Max", "Mean", "Median"]].transpose()


# avg price per district
df_mean = apartments_df.groupby(['district']).mean()
df_mean['price'] = df_mean['price'].astype(int)
fig, (ax, ax2) = plt.subplots(ncols=2, sharey=False)
ax.ticklabel_format(useOffset=False, style='plain')
ax2.ticklabel_format(useOffset=False, style='plain')
df_mean[:20].plot.barh(x=None, y="price", color="royalblue", ax=ax, grid=True, )
df_mean[:20].plot.barh(x=None, y="price_per_square", color="red", ax=ax2, grid=True, )

plt.show()


session.close()
