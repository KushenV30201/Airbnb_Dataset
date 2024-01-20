import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tkinter import *

# Plotting average price per neighborhood group
def price_nf():
    plt.figure(figsize=(10, 6))
    avg_price_neighborhood.plot(kind='bar', color='skyblue')
    plt.title('Средняя цена по районам')
    plt.xlabel('Район')
    plt.ylabel('Средняя цена')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def rasp_nf():
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='neighbourhood_group', y='price', data=list_clean)
    plt.title('Распределение цен по районам')
    plt.xlabel('Район')
    plt.ylabel('Цена')
    plt.xticks(rotation=45)
    plt.show()


def col_ob():
    plt.figure(figsize=(10, 6))
    list_clean['neighbourhood_group'].value_counts().plot(kind='bar', color='salmon')
    plt.title('Количество объявлений на район')
    plt.xlabel('Район')
    plt.ylabel('Количество объявлений')
    plt.xticks(rotation=45)
    plt.show()


# List the neighborhoods offering short-term rentals within 10 days and illustrate with a bar graph
def krat_ar():
    short_term_rentals = list_clean[list_clean['minimum_nights'] <= 10]['neighbourhood'].value_counts().head(10)
    plt.figure(figsize=(10, 6))
    short_term_rentals.plot(kind='bar', color='salmon')
    plt.title('Районы, предлагающие краткосрочную аренду (<= 10 дней)')
    plt.xlabel('Район')
    plt.ylabel('Количество предложений')
    plt.xticks(rotation=45)
    plt.show()

# List the prices with respect to room type using a bar graph and state your inferences
def price_type_room():
    plt.figure(figsize=(8, 6))
    sns.barplot(x='room_type', y='price', data=list_clean, ci=None)
    plt.title('Цены в зависимости от типа номера')
    plt.xlabel('Тип номера')
    plt.ylabel('Стоимость')
    plt.show()

# Scatter plot for service price vs room price
def ser_vs_room():
    plt.figure(figsize=(8, 6))
    plt.scatter(list_clean['service_fee'], list_clean['price'], alpha=0.5, color='blue')
    plt.title('Соотношение между стоимостью услуг и стоимостью номера')
    plt.xlabel('Стоимость услуг')
    plt.ylabel('Стоимость номера')
    plt.grid(True)
    plt.show()

def otz_price():
    plt.figure(figsize=(8, 6))
    plt.boxplot([list_clean[list_clean['review_rate_number'] == i]['price'].dropna() for i in
                 list_clean['review_rate_number'].unique()],
                labels=list_clean['review_rate_number'].unique())
    plt.title('Влияние отзывов на цену')
    plt.xlabel('Оценка')
    plt.ylabel('Цена')
    plt.grid(True)
    plt.show()

# Create a bar plot for maximum number of reviews per neighborhood group
def max_numb():
    plt.figure(figsize=(10, 6))
    plt.bar(data['Neighbourhood Group'], data['Max Number of Reviews'], color='skyblue')
    plt.xlabel('Район')
    plt.ylabel('Максимальное количество отзывов')
    plt.title('Максимальное количество отзывов на район')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

window = Tk()
window.title("Airbnb Dataset")

btn = Button(window, text="Средняя цена по районам", command=price_nf)
btn.grid(column=0, row=0)

btn1 = Button(window, text="Распределение цен по районам", command=rasp_nf)
btn1.grid(column=1, row=0)

btn2 = Button(window, text="Количество объявлений на район", command=col_ob)
btn2.grid(column=0, row=1)

btn3 = Button(window, text="Районы, предлагающие краткосрочную аренду", command=krat_ar)
btn3.grid(column=1, row=1)

btn4 = Button(window, text="Цены в зависимости от типа номера", command=price_type_room)
btn4.grid(column=0, row=2)

btn5 = Button(window, text="Соотношение между стоимостью услуг и номера", command=ser_vs_room)
btn5.grid(column=1, row=2)

btn6 = Button(window, text="Влияние отзывов на цену", command=otz_price)
btn6.grid(column=0, row=3)

btn7 = Button(window, text="Максимальное количество отзывов на район", command=max_numb)
btn7.grid(column=1, row=3)

list = pd.read_csv("Airbnb_dataset.csv")

# Display the first 5 rows
list.head(5)

# List of columns to drop
columns_to_drop = ['host id', 'id', 'country', 'country code', 'license', 'lat', 'long']

# Drop the unwanted columns
list_clean = list.drop(columns=columns_to_drop, errors='ignore')

# List the prices by neighborhood group and also mention which is the most expensive neighborhood group for rentals
avg_price_neighborhood = list_clean.groupby('neighbourhood_group')['price'].mean().sort_values(ascending=False)

# Check whether there are any duplicate values in the dataframe and if present remove them.
# Impute missing values based on data types of columns
for col in list_clean.columns:
    if list_clean[col].dtype == 'object':
        list_clean[col].fillna('Unknown', inplace=True)  # For object columns, fill missing values with 'Unknown'
    else:
        list_clean[col].fillna(list_clean[col].median(),
                               inplace=True)  # For numerical columns, fill missing values with median

max_reviews_per_group = list_clean.groupby('neighbourhood_group')['number_of_reviews'].max()
max_reviews_missing = list_clean[list_clean['neighbourhood_group'].isna()]['number_of_reviews'].max()

data = pd.DataFrame({
    'Neighbourhood Group': max_reviews_per_group.index,
    'Max Number of Reviews': max_reviews_per_group.values
})

missing_neighborhood_data = pd.DataFrame({
    'Neighbourhood Group': 'Missing Neighborhoods',
    'Max Number of Reviews': max_reviews_missing
}, index=[0])

data = pd.concat([data, missing_neighborhood_data], ignore_index=True)

window.mainloop()

