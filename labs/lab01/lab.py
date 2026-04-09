# lab.py


from pathlib import Path
import io
import pandas as pd
import numpy as np
np.set_printoptions(legacy='1.21')


# ---------------------------------------------------------------------
# QUESTION 0
# ---------------------------------------------------------------------


def consecutive_ints(ints):
    if len(ints) == 0:
        return False

    for k in range(len(ints) - 1):
        diff = abs(ints[k] - ints[k+1])
        if diff == 1:
            return True

    return False


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def median_vs_mean(nums):
    nums = sorted(nums)
    mean = sum(nums) / len(nums)
    if len(nums) % 2 == 1:
        median = nums[len(nums) // 2]
    else:
        median = (nums[(len(nums) - 1) // 2] + nums[len(nums) // 2]) / 2
    return median <= mean


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def n_prefixes(s, n):
    result = ''
    for length in range(n, 0, -1):
        result += s[:length]
    return result


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def exploded_numbers(ints, n):
    width = len(str(max(ints) + n))
    results = []
    for x in ints:
        nums = []
        for k in range(x - n, x + n + 1):
            nums.append(str(k).zfill(width))
        results.append(" ".join(nums))
    return results


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def last_chars(fh):
    s = ''
    for line in fh:
        s += line.strip()[-1]
    return s


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def add_root(A):
    root =  np.arange(len(A))
    return A + np.sqrt(root)

def where_square(A):
    return np.round(np.sqrt(A)) ** 2 == A
        


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def filter_cutoff_loop(matrix, cutoff):
    length = matrix.shape[1]
    target = []
    for i in range(length):
        if(sum(matrix[:,i]) / matrix.shape[0] > cutoff):
            target.append(i)
    return matrix[:,target]

# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def filter_cutoff_np(matrix, cutoff):
    return matrix[:, np.mean(matrix, axis = 0) > cutoff]


# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def growth_rates(A):
    return (np.round((A[1:] - A[:-1]) / A[:-1], 2))


# def with_leftover(A):
#     day = -1
#     cumulative = np.cumsum(20 % A)
#     for i in range(len(A)):
#         if cumulative[i] >= A[i]:
#             day = i
#             return day
#     return day
def with_leftover(A):
    left_over = np.cumsum(20 % A) >= A
    if left_over.any():
        return np.argmax(left_over)
    return -1

# ---------------------------------------------------------------------
# QUESTION 8
# ---------------------------------------------------------------------


def salary_stats(salary):
    num_players = salary.shape[0]
    # num_teams = salary.groupby()['Team'].shape[0]
    num_teams = salary['Team'].nunique()

    total_salary = salary['Salary'].sum()
    
    idx = salary['Salary'].idxmax()
    highest_salary = salary.loc[idx, 'Player']

    avg_los = np.round(salary[salary['Team'] == 'Los Angeles Lakers']['Salary'].mean(), 2)

    row = salary.sort_values('Salary').iloc[4]
    fifth_lowest = row['Player'] + ', ' + row['Team']

    names = salary['Player'].str.replace(r'\s+(Jr\.|Sr\.|III|II|IV)$', '', regex = True)
    duplicates = names.str.split().str[-1].duplicated().any()

    top_team = salary.loc[salary['Salary'].idxmax(), 'Team']

    total_highest = salary[salary['Team'] == top_team]['Salary'].sum()

    return pd.Series({
        'num_players': num_players, 'num_teams': num_teams, 'total_salary': total_salary, 'highest_salary': highest_salary, 'avg_los': avg_los, 'fifth_lowest': fifth_lowest, 'duplicates': duplicates,
        'top_team': top_team, 'total_highest': total_highest
    })


# ---------------------------------------------------------------------
# QUESTION 9
# ---------------------------------------------------------------------


def parse_malformed(fp):
    ...
