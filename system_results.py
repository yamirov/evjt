from dash import html, dcc
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import os
import glob

# This class is aligned to debug.domains.memory.system_status fields 
# class provides API to load dataframes with system_status columns and filter data accordingly 

# class responsible to provide abstraction to pull volume test results data frames
# could be that dedicated wrappers may be needed due to code complexity 

class SystemResults():
    SAGV = 'sagv'
    HOST = 'Host Name'
    MRC = 'mrc ver'
    def __init__(self,data_frame) -> None:
        self._dataFrame = data_frame
        pass

    def load_data_frames(self,dataFrame) -> None:
        self._dataFrame = dataFrame
    
    def get_SAGV_values(self) -> list:
        # Get the unique values for the sagv filter dropdown
        return self._dataFrame['sagv'].unique() # system result

    def get_host_values(self) -> list:
        # Get the unique values for the sagv filter dropdown
        return self._dataFrame['Host Name'].unique() # system result

    def get_mrc_values(self) -> list:
        return sorted(self._dataFrame['mrc ver'].astype('str').unique())  # system result

    def filter_data_frame(self,data_frame,sagv_filter=False,host_filter=False,mrc_ver_filter=False) -> object:
        filtered_df = data_frame
        if sagv_filter:
            filtered_df = filtered_df[filtered_df['sagv'].astype(str).str.contains(sagv_filter)]
       
        if host_filter:
            filtered_df = filtered_df[filtered_df['Host Name'].astype(str).isin(host_filter)]

        if mrc_ver_filter:
            filtered_df = filtered_df[filtered_df['mrc ver'].astype('str').isin(mrc_ver_filter)]
        return filtered_df

