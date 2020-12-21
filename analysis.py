import numpy as np
import pandas as pd


def weighted_average_agg(df):
    wam = {
        'WAM': (df['Weight'] * df['Mark']).sum() / df['Weight'].sum()
    }
    return pd.Series(wam, index=['WAM'])

def summary(df):
    return df.describe()

def get_wam(df):
    return (df['Weight'] * df['Mark']).sum() / df['Weight'].sum()

def get_wam_by_year(df):
    return df.groupby(by=['Year']).apply(weighted_average_agg)

def get_wam_by_sem(df):
    return df.groupby(by=['Year', 'Teaching period']).apply(weighted_average_agg)

def get_wam_by_faculty(df):
    return df.groupby(by=['Faculty']).apply(weighted_average_agg)

def get_wam_by_level(df):
    return df.groupby(by=['Level']).apply(weighted_average_agg)

def get_top_k_scores(df, k=20):
    return df.sort_values(by=['Mark'], ascending=False).iloc[:k][['Unit code', 'Unit title', 'Mark']].reset_index(drop=True)

def generate_report(df):
    cat = [
        'Summary:',
        'WAM:',
        'WAM by Year:', 
        'WAM by Semester:', 
        'WAM by faculty:',
        'WAM by unit level:',
        'Top Units:'
    ]
    fun = [
        summary,
        get_wam,
        get_wam_by_year,
        get_wam_by_sem,
        get_wam_by_faculty,
        get_wam_by_level,
        get_top_k_scores
    ]
    for c, f in zip(cat, fun):
        print(c)
        print(f(df))
        print()


if __name__ == '__main__':
    dtype = {
        "Year": np.int32,
        "Unit code": str, 
        "Unit title": str, 
        "Teaching period": str, 
        "Credit points": np.int16, 
        "Mark": np.int16, 
        "Grade": str
    }

    df = pd.read_csv('./academic_records/latest_record.csv', dtype=dtype)
    df['Faculty'] = df['Unit code'].str.extract('(\\w\\w\\w)')
    df['Level'] = df['Unit code'].str.extract('(\\d)').values.reshape(-1).astype(np.int16)
    df['Weight'] = np.minimum(df['Level'], 2)
    generate_report(df)