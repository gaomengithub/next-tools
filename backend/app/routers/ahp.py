import random
import re
from fastapi import APIRouter, Depends, HTTPException
from typing import List
import numpy as np
import geatpy as ea
from ..internal.auth import check_token_exp_time

dim_map = {2: 1, 3: 3, 4: 6, 5: 10, 6: 15, 7: 21, 8: 28, 9: 36}
val_map = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 1 / 2, 11: 1 / 3, 12: 1 / 4, 13: 1 / 5, 14: 1 / 6,
           15: 1 / 7, 16: 1 / 8, 17: 1 / 9, }
to_map = {1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 1 / 2: '1/2', 1 / 3: '1/3',
          1 / 4: '1/4', 1 / 5: '1/5', 1 / 6: '1/6', 1 / 7: '1/7', 1 / 8: '1/8', 1 / 9: '1/9'}
dim_map_re = dict(zip(dim_map.values(), dim_map.keys()))
RI_list = [0, 0, 0.52, 0.89, 1.12, 1.26, 1.36, 1.41, 1.46, 1.49, 1.52, 1.54, 1.56, 1.58, 1.59]

router = APIRouter(dependencies=[Depends(check_token_exp_time)])


@router.post("/ga_for_ahp/")
async def ga_for_ahp(form_data: List):
    problem = MyProblem(form_data)
    encoding = 'RI'
    nind = 50
    field = ea.crtfld('RI', problem.varTypes, problem.ranges, problem.borders)  # 创建区域描述器
    population = ea.Population(encoding, field, nind)
    if problem.M == 1:
        my_algorithm = ea.soea_DE_best_1_L_templet(problem, population)
    else:
        my_algorithm = ea.moea_MOEAD_DE_templet(problem, population)
    my_algorithm.MAXGEN = 400
    my_algorithm.logTras = 0
    my_algorithm.verbose = False
    my_algorithm.drawing = 0
    [best_indi, _] = my_algorithm.run()
    return format_data(best_indi.Phen[0], len(form_data))


def format_data(best_res, des):
    el = list(map(lambda x: val_map[x], best_res))
    if des == 2:
        matrix = np.array([
            [1, el[0]],
            [1 / el[0], 1]
        ])
        return list(map(lambda x: [to_map[_] for _ in x], matrix))
    elif des == 3:
        matrix = np.array([
            [1, el[0], el[1]],
            [1 / el[0], 1, el[2]],
            [1 / el[1], 1 / el[2], 1]
        ])
        return list(map(lambda x: [to_map[_] for _ in x], matrix))
    elif des == 4:
        matrix = np.array([
            [1, el[0], el[1], el[2]],
            [1 / el[0], 1, el[3], el[4]],
            [1 / el[1], 1 / el[3], 1, el[5]],
            [1 / el[2], 1 / el[4], 1 / el[5], 1],
        ])
        return list(map(lambda x: [to_map[_] for _ in x], matrix))
    elif des == 5:
        matrix = np.array([
            [1, el[0], el[1], el[2], el[3]],
            [1 / el[0], 1, el[4], el[5], el[6]],
            [1 / el[1], 1 / el[4], 1, el[7], el[8]],
            [1 / el[2], 1 / el[5], 1 / el[7], 1, el[9]],
            [1 / el[3], 1 / el[6], 1 / el[8], 1 / el[9], 1]
        ])
        return list(map(lambda x: [to_map[_] for _ in x], matrix))
    elif des == 6:
        matrix = np.array([
            [1, el[0], el[1], el[2], el[3], el[4]],
            [1 / el[0], 1, el[5], el[6], el[7], el[8]],
            [1 / el[1], 1 / el[5], 1, el[9], el[10], el[11]],
            [1 / el[2], 1 / el[6], 1 / el[9], 1, el[12], el[13]],
            [1 / el[3], 1 / el[7], 1 / el[10], 1 / el[12], 1, el[14]],
            [1 / el[4], 1 / el[8], 1 / el[11], 1 / el[13], 1 / el[14], 1]
        ])
        return list(map(lambda x: [to_map[_] for _ in x], matrix))
    elif des == 7:
        matrix = np.array([
            [1, el[0], el[1], el[2], el[3], el[4], el[5]],
            [1 / el[0], 1, el[6], el[7], el[8], el[9], el[10]],
            [1 / el[1], 1 / el[6], 1, el[11], el[12], el[13], el[14]],
            [1 / el[2], 1 / el[7], 1 / el[11], 1, el[15], el[16], el[17]],
            [1 / el[3], 1 / el[8], 1 / el[12], 1 / el[15], 1, el[18], el[19]],
            [1 / el[4], 1 / el[9], 1 / el[13], 1 / el[16], 1 / el[18], 1, el[20]],
            [1 / el[5], 1 / el[10], 1 / el[14], 1 / el[17], 1 / el[19], 1 / el[20], 1]
        ])
        return list(map(lambda x: [to_map[_] for _ in x], matrix))
    elif des == 8:
        matrix = np.array([
            [1, el[0], el[1], el[2], el[3], el[4], el[5], el[6]],
            [1 / el[0], 1, el[7], el[8], el[9], el[10], el[11], el[12]],
            [1 / el[1], 1 / el[7], 1, el[13], el[14], el[15], el[16], el[17]],
            [1 / el[2], 1 / el[8], 1 / el[13], 1, el[18], el[19], el[20], el[21]],
            [1 / el[3], 1 / el[9], 1 / el[14], 1 / el[18], 1, el[22], el[23], el[24]],
            [1 / el[4], 1 / el[10], 1 / el[15], 1 / el[19], 1 / el[22], 1, el[25], el[26]],
            [1 / el[5], 1 / el[11], 1 / el[16], 1 / el[20], 1 / el[23], 1 / el[25], 1, el[27]],
            [1 / el[6], 1 / el[12], 1 / el[17], 1 / el[21], 1 / el[24], 1 / el[26], 1 / el[27], 1]
        ])
        return list(map(lambda x: [to_map[_] for _ in x], matrix))
    elif des == 9:
        matrix = np.array([
            [1, el[0], el[1], el[2], el[3], el[4], el[5], el[6], el[7]],
            [1 / el[0], 1, el[8], el[9], el[10], el[11], el[12], el[13], el[14]],
            [1 / el[1], 1 / el[8], 1, el[15], el[16], el[17], el[18], el[19], el[20]],
            [1 / el[2], 1 / el[9], 1 / el[15], 1, el[21], el[22], el[23], el[24], el[25]],
            [1 / el[3], 1 / el[10], 1 / el[16], 1 / el[21], 1, el[26], el[27], el[28], el[29]],
            [1 / el[4], 1 / el[11], 1 / el[17], 1 / el[22], 1 / el[26], 1, el[30], el[31], el[32]],
            [1 / el[5], 1 / el[12], 1 / el[18], 1 / el[23], 1 / el[27], 1 / el[30], 1, el[33], el[34]],
            [1 / el[6], 1 / el[13], 1 / el[19], 1 / el[24], 1 / el[28], 1 / el[31], 1 / el[33], 1, el[35]],
            [1 / el[7], 1 / el[14], 1 / el[20], 1 / el[25], 1 / el[29], 1 / el[32], 1 / el[34], 1 / el[35], 1]
        ])
        return list(map(lambda x: [to_map[_] for _ in x], matrix))
    else:
        raise HTTPException(status_code=500, detail="矩阵维度小于2或者大于9")


def generator_matrix(el: list, des: int):
    if des == 2:
        matrix = np.array([
            [1, el[0]],
            [1 / el[0], 1]
        ])
        return matrix
    elif des == 3:
        matrix = np.array([
            [1, el[0], el[1]],
            [1 / el[0], 1, el[2]],
            [1 / el[1], 1 / el[2], 1]
        ])
        return matrix
    elif des == 4:
        matrix = np.array([
            [1, el[0], el[1], el[2]],
            [1 / el[0], 1, el[3], el[4]],
            [1 / el[1], 1 / el[3], 1, el[5]],
            [1 / el[2], 1 / el[4], 1 / el[5], 1],
        ])
        return matrix
    elif des == 5:
        matrix = np.array([
            [1, el[0], el[1], el[2], el[3]],
            [1 / el[0], 1, el[4], el[5], el[6]],
            [1 / el[1], 1 / el[4], 1, el[7], el[8]],
            [1 / el[2], 1 / el[5], 1 / el[7], 1, el[9]],
            [1 / el[3], 1 / el[6], 1 / el[8], 1 / el[9], 1]
        ])
        return matrix
    elif des == 6:
        matrix = np.array([
            [1, el[0], el[1], el[2], el[3], el[4]],
            [1 / el[0], 1, el[5], el[6], el[7], el[8]],
            [1 / el[1], 1 / el[5], 1, el[9], el[10], el[11]],
            [1 / el[2], 1 / el[6], 1 / el[9], 1, el[12], el[13]],
            [1 / el[3], 1 / el[7], 1 / el[10], 1 / el[12], 1, el[14]],
            [1 / el[4], 1 / el[8], 1 / el[11], 1 / el[13], 1 / el[14], 1]
        ])
        return matrix
    elif des == 7:
        matrix = np.array([
            [1, el[0], el[1], el[2], el[3], el[4], el[5]],
            [1 / el[0], 1, el[6], el[7], el[8], el[9], el[10]],
            [1 / el[1], 1 / el[6], 1, el[11], el[12], el[13], el[14]],
            [1 / el[2], 1 / el[7], 1 / el[11], 1, el[15], el[16], el[17]],
            [1 / el[3], 1 / el[8], 1 / el[12], 1 / el[15], 1, el[18], el[19]],
            [1 / el[4], 1 / el[9], 1 / el[13], 1 / el[16], 1 / el[18], 1, el[20]],
            [1 / el[5], 1 / el[10], 1 / el[14], 1 / el[17], 1 / el[19], 1 / el[20], 1]
        ])
        return matrix
    elif des == 8:
        matrix = np.array([
            [1, el[0], el[1], el[2], el[3], el[4], el[5], el[6]],
            [1 / el[0], 1, el[7], el[8], el[9], el[10], el[11], el[12]],
            [1 / el[1], 1 / el[7], 1, el[13], el[14], el[15], el[16], el[17]],
            [1 / el[2], 1 / el[8], 1 / el[13], 1, el[18], el[19], el[20], el[21]],
            [1 / el[3], 1 / el[9], 1 / el[14], 1 / el[18], 1, el[22], el[23], el[24]],
            [1 / el[4], 1 / el[10], 1 / el[15], 1 / el[19], 1 / el[22], 1, el[25], el[26]],
            [1 / el[5], 1 / el[11], 1 / el[16], 1 / el[20], 1 / el[23], 1 / el[25], 1, el[27]],
            [1 / el[6], 1 / el[12], 1 / el[17], 1 / el[21], 1 / el[24], 1 / el[26], 1 / el[27], 1]
        ])
        return matrix
    elif des == 9:
        matrix = np.array([
            [1, el[0], el[1], el[2], el[3], el[4], el[5], el[6], el[7]],
            [1 / el[0], 1, el[8], el[9], el[10], el[11], el[12], el[13], el[14]],
            [1 / el[1], 1 / el[8], 1, el[15], el[16], el[17], el[18], el[19], el[20]],
            [1 / el[2], 1 / el[9], 1 / el[15], 1, el[21], el[22], el[23], el[24], el[25]],
            [1 / el[3], 1 / el[10], 1 / el[16], 1 / el[21], 1, el[26], el[27], el[28], el[29]],
            [1 / el[4], 1 / el[11], 1 / el[17], 1 / el[22], 1 / el[26], 1, el[30], el[31], el[32]],
            [1 / el[5], 1 / el[12], 1 / el[18], 1 / el[23], 1 / el[27], 1 / el[30], 1, el[33], el[34]],
            [1 / el[6], 1 / el[13], 1 / el[19], 1 / el[24], 1 / el[28], 1 / el[31], 1 / el[33], 1, el[35]],
            [1 / el[7], 1 / el[14], 1 / el[20], 1 / el[25], 1 / el[29], 1 / el[32], 1 / el[34], 1 / el[35], 1]
        ])
        return matrix
    else:
        raise HTTPException(status_code=500, detail="矩阵维度小于2或者大于9")


def computer_cr_wg(kws, matrix_des, form_data):
    cr_val_list = []
    eigen_list = []
    ctr_idx = {}
    not_ctr = []
    for index, item in enumerate(form_data):
        if item != '不控制':
            ctr_idx[index] = item
        if item == '不控制':
            not_ctr.append(index)
    for idx in range(len(kws[0])):
        elem = [kws[_][idx][0] for _ in range(len(kws))]
        elem = list(map(lambda x: val_map[x], elem))
        # for em_index, em in enumerate(elem):
        #     if em > 6:
        #         elem[em_index] = 1.0 / (em - 6)
        matrix = generator_matrix(elem, matrix_des)
        # print(matrix)
        eig_val, eig_vector = np.linalg.eig(matrix)
        max_idx = np.argmax(eig_val)
        max_eig_val = np.max(eig_val.real)
        eigen = eig_vector[:, max_idx].real
        eigen = eigen / eigen.sum()
        eigen_list.append(eigen)
        ci_val = (max_eig_val - matrix_des) / (matrix_des - 1)
        cr_val = 0 if matrix_des <= 2 else ci_val / RI_list[matrix_des - 1] - 0.095
        cr_val_list.append([cr_val])
    ob = []
    # cv_ctr = []
    for key, val in ctr_idx.items():
        ob_eigen = np.abs(
            np.array(eigen_list)[:, key] - float(re.findall(r'0.\d+', val)[0]))
        ob.append(ob_eigen)
    # for i in not_ctr:
    #     cv = np.array(eigen_list)[:, i] - 1 / len(form_data)
    #     cv_ctr.append(cv)
    # print(np.array(ob).T)
    # , np.array(cv_ctr).T
    return np.array(cr_val_list).reshape(-1, 1), np.array(ob).T


class MyProblem(ea.Problem):
    def __init__(self, form_data):
        name = 'MyProblem'  # 初始化name（函数名称，可以随意设置）
        m = sum(_ != '不控制' for _ in form_data)
        if m == 0:
            form_data[random.randint(0, len(form_data) - 1)] = str(round(random.uniform(0.2, 0.8), 4))
            m = 1
        # raise HTTPException(status_code=500, detail="需要至少控制一个")

        self.form_data = form_data
        dim = dim_map[len(form_data)]
        maxormins = [1] * m  # 初始化目标最小最大化标记列表，1：min；-1：max
        var_types = [1] * dim  # 初始化决策变量类型，0：连续；1：离散
        lb = [1] * dim  # 决策变量下界
        ub = [17] * dim  # 决策变量上界
        lbin = [1] * dim  # 决策变量下边界 开闭区间...
        ubin = [1] * dim  # 决策变量上边界
        # 调用父类构造方法完成实例化
        ea.Problem.__init__(self, name, m, maxormins, dim, var_types, lb, ub, lbin, ubin)

    def aimFunc(self, pop):  # 目标函数，pop为传入的种群对象
        _vars = pop.Phen
        mm = computer_cr_wg([_vars[:, [_]] for _ in range(self.Dim)], dim_map_re[self.Dim], self.form_data)
        pop.ObjV = mm[1]
        # print(pop.ObjV)
        # 采用可行性法则处理约束，生成种群个体违反约束程度矩阵
        pop.CV = mm[0]
        # print(pop.CV)
