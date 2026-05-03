import pandas as pd # импортируем основную библиотеку для работы с Эксель
import matplotlib.pyplot as plt # импортируем библиотеку для построения графиков
import numpy as np # импортируем библиотеку для массивов

# Загрузка данных
df = pd.read_csv('5_train.csv') # импортируем таблицу Эксель, сохраняем данные таблицы в переменную
df['datetime'] = pd.to_datetime(df['datetime']) #

# ЗАДАНИЕ 1. Находим час/суток с максимальным числом поездок в выходные дни.

df['hour'] = df['datetime'].dt.hour # разбиваем на столбики время и дату
df['dayofweek'] = df['datetime'].dt.dayofweek  # 0=Пн, 6=Вс # извлекаем дни недели

weekend_df = df[df['dayofweek'].isin([5, 6])] # Фильтруем выходные дни
hourly_stats = weekend_df.groupby('hour')['count'].sum() # Группируем по часу и суммируем количество поездок

# Находим час с максимумом
max_hour = hourly_stats.idxmax()
max_trips = hourly_stats.max()

# Выводим результат
print(f"Час с максимальным числом поездок в выходные: {max_hour}:00")
print(f"Общее количество поездок в этот час: {max_trips}")

# ЗАДАНИЕ 2. Строим столбчатую диаграмму.

# Группируем по сезону и считаем среднее число для casual и registered
seasonal_avg = df.groupby('season')[['casual', 'registered']].mean()

# Строим столбчатую диаграмму
ax = seasonal_avg.plot(kind='bar', figsize=(10, 6), width=0.8, 
                       color=["#AA304C", "#8B4581"])

# Оформление графика
plt.title('Среднее число поездок по сезонам', fontsize=14, fontweight='bold') # Заголовок графика
plt.xlabel('Сезон (1=зима, 2=весна, 3=лето, 4=осень)', fontsize=11) # Подписи оси Х
plt.ylabel('Среднее количество поездок', fontsize=11) # Подписи оси У
plt.xticks(rotation=0) # Поворот подписи оси х на всякий слайчай
plt.legend(title='Тип пользователя', title_fontsize=10) # Заголовок
plt.grid(axis='y', alpha=0.3, linestyle='--') # Добавление сетки
plt.tight_layout() # отступы для текста

# Добавляем значения на столбцы
for container in ax.containers:
    ax.bar_label(container, fmt='%.1f', fontsize=9)

plt.show() # отображение графика в окне

# Выводим числовые значения для справки
print("\n Средние значения по сезонам:")
print(seasonal_avg.round(2))

# ЗАДАНИЕ 3. Находим все наблюдения, где count > 500.

high_demand = df[df['count'] > 500].copy() # Фильтруем строки, где count > 500

# Количество таких наблюдений
total_high = len(high_demand)
print(f"Наблюдений с count > 500: {total_high}")

# Анализируем распределение по сезонам
season_counts = high_demand['season'].value_counts().sort_index()
print(f"\nРаспределение по сезонам:")
for season, count in season_counts.items():
    season_name = {1: 'зима', 2: 'весна', 3: 'лето', 4: 'осень'}[season]
    print(f"   Сезон {season} ({season_name}): {count} наблюдений")

# Определяем самый частый сезон
most_common_season = high_demand['season'].mode()[0]
season_names = {1: 'зима', 2: 'весна', 3: 'лето', 4: 'осень'}
print(f"\nЧаще всего высокий спрос наблюдается в: {season_names[most_common_season]} (сезон {most_common_season})")

# ЗАДАНИЕ 4. Сохраняем в CSV таблицу: среднюю температуру и среднее число поездок по каждому месяцу.

# Извлекаем месяц из даты
df['month'] = df['datetime'].dt.month

# Группируем по месяцу и считаем среднюю температуру и среднее число поездок
monthly_stats = df.groupby('month').agg({
    'temp': 'mean',
    'count': 'mean'
}).round(2)

# Переименовываем колонки для удобства
monthly_stats.columns = ['avg_temperature', 'avg_trips']

# Добавим названия месяцев для удобства
month_names = {
    1: 'January', 2: 'February', 3: 'March', 4: 'April',
    5: 'May', 6: 'June', 7: 'July', 8: 'August',
    9: 'September', 10: 'October', 11: 'November', 12: 'December'
}
monthly_stats['month_name'] = monthly_stats.index.map(month_names)

# Сохраняем в CSV
monthly_stats.to_csv('monthly_bike_stats.csv', index_label='month')
print("Данные сохранены в файл 'monthly_bike_stats.csv'")

# Показываем результат
print("\nСредние значения по месяцам:")
print(monthly_stats)
