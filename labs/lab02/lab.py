# lab.py


import os
import io
from pathlib import Path
import pandas as pd
import numpy as np


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def trick_me():
    tricky_1 = pd.DataFrame(
        [['A','B',1],['C','D',2],['E','F',3],['G','H',4],['I','J',5]],
        columns=['Name','Name','Age']
    )
    tricky_1.to_csv('tricky_1.csv', index=False)
    tricky_2 = pd.read_csv('tricky_1.csv')
    return 3


def trick_bool():
    return [4, 10, 13]


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def population_stats(df):
    num_nonnull = df.notna().sum()
    prop_nonnull = num_nonnull / len(df)
    num_distinct = df.nunique()
    prop_distinct = num_distinct / num_nonnull
    
    return pd.DataFrame({
        'num_nonnull': num_nonnull,
        'prop_nonnull': prop_nonnull,
        'num_distinct': num_distinct,
        'prop_distinct': prop_distinct
    })


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def most_common(df, N=10):
    result = pd.DataFrame(index=range(N))
    for col in df.columns:
        vc = df[col].value_counts().iloc[:N]
        padding = [np.nan] * (N - len(vc))
        result[f'{col}_values'] = list(vc.index) + padding
        result[f'{col}_counts'] = list(vc.values) + padding
    return result


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def super_hero_powers(powers):
    df = powers.set_index('hero_names')
    
    hero_most = df.sum(axis=1).idxmax()
    
    flyers = df[df['Flight']].drop(columns=['Flight'])
    most_common_flyer = flyers.sum(axis=0).idxmax()
    
    single = df[df.sum(axis=1) == 1]
    most_common_single = single.idxmax(axis=1).value_counts().idxmax()
    
    return [hero_most, most_common_flyer, most_common_single]


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def clean_heroes(heroes):
    return heroes.replace(['-', -99], np.nan)


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def super_hero_stats():
    return ['Onslaught', 'George Lucas', 'bad', 'Marvel Comics', 'NBC - Heroes', 'Groot']


# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def clean_universities(df):
    df = df.copy()

    df['institution'] = df['institution'].str.replace('\n', ', ', regex=False)
    
    df['broad_impact'] = df['broad_impact'].astype(int)
    
    split = df['national_rank'].str.split(', ', n=1, expand=True)
    df['nation'] = split[0].replace({
        'Czechia': 'Czech Republic',
        'USA': 'United States',
        'UK': 'United Kingdom',
    })
    df['national_rank_cleaned'] = split[1].astype(int)
    df = df.drop(columns=['national_rank'])
    
    has_all = df['control'].notna() & df['city'].notna() & df['state'].notna()
    is_public = df['control'] == 'Public'
    df['is_r1_public'] = has_all & is_public
    
    return df

def university_info(cleaned):
    counts = cleaned['state'].value_counts()
    big = counts[counts >= 3].index
    means = cleaned[cleaned['state'].isin(big)].groupby('state')['score'].mean()
    ans1 = means.idxmin()
    
    top100 = cleaned[cleaned['world_rank'] <= 100]
    ans2 = float((top100['quality_of_faculty'] <= 100).mean())
    
    priv_prop = cleaned.groupby('state')['is_r1_public'].apply(lambda x: (~x).mean())
    ans3 = int((priv_prop >= 0.5).sum())
    
    nr1 = cleaned[cleaned['national_rank_cleaned'] == 1]
    ans4 = nr1.loc[nr1['world_rank'].idxmax(), 'institution']
    
    return [ans1, ans2, ans3, ans4]

