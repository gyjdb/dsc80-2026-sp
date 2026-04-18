# project.py


import pandas as pd
import numpy as np
from pathlib import Path

import plotly.express as px


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def get_assignment_names(grades):
    cols = grades.columns
    
    categories = ['lab', 'project', 'midterm', 'final', 'disc', 'checkpoint']
    
    result = {}

    for cat in categories:
        names = sorted(
            col for col in cols if col.lower().startswith(cat) and ' - ' not in col and '_free_response' not in col
        )
        result[cat] = names

    return result


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def projects_total(grades):
    assignment_names = get_assignment_names(grades)
    # 拿到纯 project 名，排除 checkpoint
    projects = [p for p in assignment_names['project'] if '_checkpoint' not in p]
    
    project_scores = []

    for proj in projects:
        proj_scores = grades[proj].fillna(0)
        proj_max_scores = grades[proj + ' - Max Points']

        fr = proj + '_free_response'

        if fr in grades.columns:
            proj_scores = proj_scores + grades[fr].fillna(0)
            proj_max_scores = proj_max_scores + grades[fr + ' - Max Points']
        
        project_scores.append(proj_scores / proj_max_scores)

    return pd.concat(project_scores, axis=1).mean(axis=1)


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def lateness_penalty(col):
    def get_multiplier(time_str):
        parts = time_str.split(':')
        hours = int(parts[0]) + int(parts[1]) / 60 + int(parts[2]) / 3600
        
        if hours <= 2:
            return 1.0
        elif hours <= 170:
            return 0.9
        elif hours <= 338:
            return 0.7
        else:
            return 0.4
    
    return col.apply(get_multiplier)


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def process_labs(grades):
    assignment_names = get_assignment_names(grades)
    labs = assignment_names['lab']
    
    result = {}
    for lab in labs:
        score = grades[lab].fillna(0)
        max_pts = grades[lab + ' - Max Points']
        lateness = lateness_penalty(grades[lab + ' - Lateness (H:M:S)'])
        
        result[lab] = (score / max_pts) * lateness
    
    return pd.DataFrame(result)


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def lab_total(processed):

    row_sum = processed.sum(axis=1)
    row_min = processed.min(axis=1)
    n = processed.shape[1]
    return (row_sum - row_min) / (n - 1)


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def total_points(grades):
    assignment_names = get_assignment_names(grades)
    
    def simple_average(category):
        names = assignment_names[category]
        if not names:
            return 0
        scores = []
        for name in names:
            score = grades[name].fillna(0) / grades[name + ' - Max Points']
            scores.append(score)
        return pd.concat(scores, axis=1).mean(axis=1)
    
    lab = lab_total(process_labs(grades))
    project = projects_total(grades)
    midterm = simple_average('midterm')
    final = simple_average('final')
    
    checkpoints = [p for p in assignment_names['project'] if '_checkpoint' in p]
    cp_scores = []
    for cp in checkpoints:
        cp_scores.append(grades[cp].fillna(0) / grades[cp + ' - Max Points'])
    checkpoint = pd.concat(cp_scores, axis=1).mean(axis=1)
    
    disc = simple_average('disc')
    
    return (0.20 * lab + 0.30 * project + 0.025 * checkpoint 
            + 0.025 * disc + 0.15 * midterm + 0.30 * final)


# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def final_grades(total):
    def to_letter(grade):
        if grade >= 0.9:
            return 'A'
        elif grade >= 0.8:
            return 'B'
        elif grade >= 0.7:
            return 'C'
        elif grade >= 0.6:
            return 'D'
        else:
            return 'F'
    
    return total.apply(to_letter)

def letter_proportions(total):
    letters = final_grades(total)
    proportions = letters.value_counts(normalize=True)

    for grade in ['A', 'B', 'C', 'D', 'F']:
        if grade not in proportions.index:
            proportions[grade] = 0
    return proportions.sort_values(ascending=False)


# ---------------------------------------------------------------------
# QUESTION 8
# ---------------------------------------------------------------------


def raw_redemption(final_breakdown, question_numbers):
    all_cols = final_breakdown.columns
    
    redemption_cols = [all_cols[q] for q in question_numbers]
    
    redemption_df = final_breakdown[redemption_cols]

    max_pts = redemption_df.columns.str.extract(r'\((\d+\.?\d*) pts\)')[0].astype(float)

    total_score = redemption_df.sum(axis=1)
    total_max = max_pts.sum()
    
    return pd.DataFrame({
        'PID': final_breakdown['PID'],
        'Raw Redemption Score': (total_score / total_max).fillna(0)
    })


def combine_grades(grades, raw_redemption_df):

    return grades.merge(raw_redemption_df, on='PID', how='left')


# ---------------------------------------------------------------------
# QUESTION 9
# ---------------------------------------------------------------------


def z_score(s):
    return (s - s.mean()) / s.std(ddof=0)


def add_post_redemption(grades_combined):
    midterm_raw = grades_combined['Midterm'].fillna(0)
    midterm_max = grades_combined['Midterm - Max Points']
    midterm_prop = midterm_raw / midterm_max  # 0到1之间的比例

    midterm_prop_with_nan = grades_combined['Midterm'] / midterm_max
    
    midterm_z = z_score(midterm_prop_with_nan)
    redemption_z = z_score(grades_combined['Raw Redemption Score'])

    midterm_mean = midterm_prop_with_nan.mean()
    midterm_std = midterm_prop_with_nan.std(ddof=0)
    
    redeemed = redemption_z * midterm_std + midterm_mean
    
    post_redemption = midterm_prop_with_nan.copy()
    mask = redemption_z > midterm_z
    post_redemption[mask] = redeemed[mask]
    post_redemption = post_redemption.clip(upper=1.0)
    
    result = grades_combined.copy()
    result['Midterm Score Pre-Redemption'] = midterm_prop_with_nan
    result['Midterm Score Post-Redemption'] = post_redemption
    
    return result


# ---------------------------------------------------------------------
# QUESTION 10
# ---------------------------------------------------------------------


def total_points_post_redemption(grades_combined):
    combined = add_post_redemption(grades_combined)
    
    original_total = total_points(grades_combined)
    
    pre = combined['Midterm Score Pre-Redemption'].fillna(0)
    post = combined['Midterm Score Post-Redemption'].fillna(0)
    
    return original_total - 0.15 * pre + 0.15 * post


def proportion_improved(grades_combined):
    before = final_grades(total_points(grades_combined))
    after = final_grades(total_points_post_redemption(grades_combined))
    
    grade_order = {'A': 4, 'B': 3, 'C': 2, 'D': 1, 'F': 0}
    
    before_num = before.map(grade_order)
    after_num = after.map(grade_order)
    
    improved = (after_num > before_num).sum()
    return improved / len(grades_combined)


# ---------------------------------------------------------------------
# QUESTION 11
# ---------------------------------------------------------------------


def section_most_improved(grades_analysis):
    grade_order = {'A': 4, 'B': 3, 'C': 2, 'D': 1, 'F': 0}
    
    pre = grades_analysis['Letter Grade Pre-Redemption'].map(grade_order)
    post = grades_analysis['Letter Grade Post-Redemption'].map(grade_order)
    
    improved = post > pre

    proportion = grades_analysis.groupby('Section')['Letter Grade Pre-Redemption'].transform('count')

    result = grades_analysis.assign(improved=improved).groupby('Section')['improved'].mean()
    
    return result.idxmax()


def top_sections(grades_analysis, t, n):
    final_score = grades_analysis['Final'].fillna(0) / grades_analysis['Final - Max Points']
    
    df = grades_analysis.assign(final_score=final_score)

    def count_above(group):
        return (group['final_score'] >= t).sum()
    
    counts = df.groupby('Section').apply(count_above)

    qualifying = counts[counts >= n].index
    return np.array(sorted(qualifying))


# ---------------------------------------------------------------------
# QUESTION 12
# ---------------------------------------------------------------------


def rank_by_section(grades_analysis):
    def assign_ranks(group):
        ranked = group.sort_values('Total Points Post-Redemption', ascending=False)
        ranked = ranked.reset_index(drop=True)
        ranked['Section Rank'] = ranked.index + 1
        return ranked
    
    ranked_df = grades_analysis.groupby('Section', group_keys=False).apply(assign_ranks)
    
    result = ranked_df.pivot(index='Section Rank', columns='Section', values='PID')
    
    result = result.fillna('')
    
    result = result.reindex(sorted(result.columns), axis=1)
    
    return result







# ---------------------------------------------------------------------
# QUESTION 13
# ---------------------------------------------------------------------


def letter_grade_heat_map(grades_analysis):
    grades = ['A', 'B', 'C', 'D', 'F']
    sections = sorted(grades_analysis['Section'].unique())
    
    data = []
    for grade in grades:
        row = []
        for section in sections:
            section_df = grades_analysis[grades_analysis['Section'] == section]
            prop = (section_df['Letter Grade Post-Redemption'] == grade).mean()
            row.append(prop)
        data.append(row)

    heatmap_df = pd.DataFrame(data, index=grades, columns=sections)
    
    fig = px.imshow(
        heatmap_df,
        color_continuous_scale='Blues',
        title='Distribution of Letter Grades by Section',
        labels={'x': 'Section', 'y': 'Letter Grade Post-Redemption', 'color': 'color'}
    )
    
    return fig
