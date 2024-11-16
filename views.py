from fastapi import APIRouter, HTTPException
from typing import List
from models import Target, UpdateTarget
from data_manager import load_data, save_data

targets = APIRouter()

targets_df = load_data()


@targets.get("/todo", response_model=List[Target])
def get_all_targets():
    return targets_df.to_dict(orient='records')


@targets.post('/todo', response_model=Target)
def add_target(target: Target):
    new_target = target.dict()
    targets_df.loc[len(targets_df)] = new_target
    save_data(targets_df)
    return new_target


@targets.put("/todo/{target_title}", response_model=Target)
def update_target(target_title: str, updated_target: UpdateTarget):
    target_row = targets_df[targets_df['title'] == target_title]
    if target_row.empty:
        raise HTTPException(status_code=404, detail='Target not found')
    target_index = target_row.index[0]
    for field, value in updated_target.dict(exclude_unset=True).items():
        targets_df.at[target_index, field] = value
    save_data(targets_df)
    return targets_df.loc[target_index].to_dict()


@targets.delete('/todo/{target_title}', response_model=Target)
def delete_target(target_title: str):
    target_row = targets_df[targets_df['title'] == target_title]
    if target_row.empty:
        raise HTTPException(status_code=404, detail='Target is not found')
    target_index = target_row.index[0]
    deleted_target = targets_df.loc[target_index].to_dict()
    targets_df.drop(target_index, inplace=True)
    save_data(targets_df)
    return deleted_target
