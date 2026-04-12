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
    ...
    
def combine_grades(grades, raw_redemption_scores):
    ...


# ---------------------------------------------------------------------
# QUESTION 9
# ---------------------------------------------------------------------


def z_score(ser):
    ...
    
def add_post_redemption(grades_combined):
    ...


# ---------------------------------------------------------------------
# QUESTION 10
# ---------------------------------------------------------------------


def total_points_post_redemption(grades_combined):
    ...
        
def proportion_improved(grades_combined):
    ...


# ---------------------------------------------------------------------
# QUESTION 11
# ---------------------------------------------------------------------


def section_most_improved(grades_analysis):
    ...
    
def top_sections(grades_analysis, t, n):
    ...


# ---------------------------------------------------------------------
# QUESTION 12
# ---------------------------------------------------------------------


def rank_by_section(grades_analysis):
    ...







# ---------------------------------------------------------------------
# QUESTION 13
# ---------------------------------------------------------------------


def letter_grade_heat_map(grades_analysis):
    ...
