from fastapi import APIRouter, Depends, HTTPException
from typing import Dict
from ..internal.auth import check_token_exp_time
import random

router = APIRouter(dependencies=[Depends(check_token_exp_time)])

probability_map = {
    '1': [0.6827, 0.2673, 0.05, 0, 0],
    '1.25': [0.57885, 0.37115, 0.05, 0, 0],
    '1.5': [0.475, 0.475, 0.05, 0, 0],
    '1.75': [0.37115, 0.57885, 0.05, 0, 0],
    '2': [0.13365, 0.6827, 0.13365, 0.05, 0],
    '2.25': [0.025, 0.57885, 0.37115, 0.025, 0],
    '2.5': [0.025, 0.475, 0.475, 0.025, 0],
    '2.75': [0.025, 0.37115, 0.57885, 0.025, 0],
    '3': [0.025, 0.13365, 0.6827, 0.13365, 0.025],
    '3.25': [0, 0.025, 0.57885, 0.37115, 0.025],
    '3.5': [0, 0.025, 0.475, 0.475, 0.025],
    '3.75': [0, 0.025, 0.37115, 0.57885, 0.025],
    '4': [0, 0.05, 0.13365, 0.6827, 0.13365],
    '4.25': [0, 0.025, 0.37115, 0.57885, 0.025],
    '4.5': [0, 0, 0.5, 0.475, 0.475],
    '4.75': [0, 0, 0.05, 0.37115, 0.57885],
    '5': [0, 0, 0.05, 0.2673, 0.6827]
}
sequence = [1, 2, 3, 4, 5]


def number_of_certain_probability(seq, probability):
    x = random.uniform(0, 1)
    cumulative_probability = 0.0
    item = None
    for item, item_probability in zip(seq, probability):
        cumulative_probability += item_probability
        if x < cumulative_probability:
            break
    return item


@router.post("/mc_for_fce/")
async def mc_for_fce(form_data: Dict):
    try:
        experts_tab = []
        # membership_tab = []
        for _ in form_data['idx_num']:
            probability = probability_map[str(_)]
            arr = []
            for __ in range(int(form_data['experts_num'])):
                result = number_of_certain_probability(sequence, probability)
                arr.append(result)
            experts_distributed = [
                arr.count(1),
                arr.count(2),
                arr.count(3),
                arr.count(4),
                arr.count(5),
            ]
            experts_tab.append(experts_distributed)
            # membership_tab.append(
            #     list(map(lambda x: " %.4f " % float(x / form_data['experts_num']), experts_distributed)))
        # return {"experts_tab": experts_tab, "membership_tab": membership_tab}
        return experts_tab
    except (KeyError, TypeError):
        raise HTTPException(status_code=500, detail="out of range")
