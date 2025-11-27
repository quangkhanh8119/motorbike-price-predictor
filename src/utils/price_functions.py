import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os

# ============================================================
# CÁC HÀM SUPPORT GIÁ
# ============================================================
def format_vnd(x):
    try:
        return f"{int(x):,} VND"
    except:
        return str(x)

def format_trieu_vnd(x):
    try:
        return f"{int(x):,} Triệu"
    except:
        return int(0.0)


def suggest_price(g):
    return dict(
        recommended=g,
        fast_sell=int(g*0.95),
        max_profit=int(g*1.05),
        fair_low=int(g*0.9),
        fair_high=int(g*1.1),
        fair_min=int((g*0.9)-(g/2)),
        fair_max=int((g*1.1)+(g/2)),
    )