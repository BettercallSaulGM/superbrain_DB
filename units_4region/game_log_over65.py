import numpy as np
import pymysql
import pandas as pd
import seaborn as sns

from tqdm import tqdm

# 시각화 모듈 임포트
import matplotlib.pyplot as plt
import seaborn as sns


# unicode minus를 사용하지 않기 위한 설정 (minus 깨짐현상 방지)
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.family'] = 'Malgun Gothic'
sns.set(rc={'figure.figsize':(11.7,8.27)})


def unit_stats(x):
    df = {}
    idx = ['edu', 'age']

    df['unit' + '_speed'] = x['game_log_speed'].mean() * (2 - x['game_log_success'].mean() / 100) \
                            * (1 - x['game_log_level'].mean() / 10)
    df['edu'] = x.iloc[0]['education']
    df['age'] = x.iloc[0]['age']
    df['unit' + '_level'] = x['game_log_level'].mean()

    idx.append('unit' + '_speed')
    #     idx.append('unit' + str(unit) + '_score')
    idx.append('unit' + '_level')
    return pd.Series(df, index=idx)


def main(x, title):

    game_log = pd.read_csv("../game_log.csv", encoding='utf-8-sig', index_col='game_log_idx')
    unit_df = [game_log[game_log['unit']==n ] for n in x]
    unit = pd.concat(unit_df)

    unit_log = unit.groupby(['user_idx']).apply(unit_stats)

    unit_log.loc[unit_log['edu'] >= 7, 'Category'] = "High_Edu"
    unit_log.loc[unit_log['edu'] < 7, 'Category'] = "Low_Edu"

    temp = unit_log[unit_log['unit_speed'] > 100].index
    unit_log = unit_log.drop(temp)

    low_edu_min_age = unit_log.loc[unit_log['Category'] == 'Low_Edu', 'age'].min()
    unit_log_over65 = unit_log[unit_log['age'] > low_edu_min_age]

    unit_log = unit_log_over65

    plt.figure(figsize=(10, 10))
    plt.title(title, fontsize=25)
    plt.ylabel('Speed')
    sns.scatterplot(unit_log['age'], unit_log['unit_speed'], hue=unit_log['Category'])
    plt.show()

    plt.figure(figsize=(10, 10))
    plt.title(title, fontsize=25)
    plt.ylabel('Speed')
    sns.boxplot(unit_log['Category'], unit_log['unit_speed'], showfliers=False)
    plt.show()

if __name__=="__main__":
    main()