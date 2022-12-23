# -*- coding:utf-8 -*-
'''
# File: speclib.py
# Project: /Users/li/work_github/pkgspc
# Created Date: 2022/12/01
# Author: ssdxj
# -----
# Last Modified: 2022/12/23 23:27:57
# Modified By: ssdxj (purewangli@gmail.com) at mac.local
# -----
# HISTORY:
# Date        	By  	Comments
# ------------	-----	-------------------------------------------------
'''


import pandas as pd
import numpy.typing as npt
import numpy as np
import re


class Speclib:
    def __init__(self, fpath) -> None:
        self._fpath = fpath
        self._wavelength, self._wavelength_name, self._reflectance, self._meta = self._load_csv(
            fpath)

    @property
    def wavelength(self) -> npt.ArrayLike:
        return self._wavelength

    @property
    def wavelength_name(self) -> npt.ArrayLike:
        return self._wavelength_name

    @property
    def reflectance(self) -> pd.DataFrame:
        return self._reflectance

    @property
    def meta(self) -> pd.DataFrame:
        return self._meta

    @staticmethod
    def _load_csv(fpath) -> tuple[npt.ArrayLike, npt.ArrayLike, pd.DataFrame, pd.DataFrame]:
        """Parse csv spectra data

        Args:
            fpath (str): csv file path in wide table format.

        Returns:
            tuple[npt.ArrayLike, npt.ArrayLike, npt.DataFrame, pd.DataFrame]: Wavelength array (1d), Wavelength name array (1d), reflectance dataframe, meta dataframe.
        """
        df = pd.read_csv(fpath)
        all_colnames = df.columns.values.tolist()
        reflectance_columns = Speclib._extract_number_colnames(
            all_colnames, False)
        meta_colnames = Speclib._extract_number_colnames(all_colnames, True)

        df_reflectance = df.loc[:, reflectance_columns]
        df_meta = df.loc[:, meta_colnames]
        wl = [float(x) for x in reflectance_columns]

        return wl, reflectance_columns, df_reflectance, df_meta

    @staticmethod
    def _extract_number_colnames(colnames: npt.ArrayLike, reverse: bool = False) -> npt.ArrayLike:
        """Extract spectra or meta columns names from wide spectra table by RE.

        Args:
            colnames (npt.ArrayLike): Table column names.
            reverse (bool, optional): False for spectra column names, while True for meta column names. Defaults to False.

        Returns:
            npt.ArrayLike: List of columns.
        """
        if not reverse:
            out = [x for x in colnames if re.match('^[0-9]+(\.[0-9]+)*', x)]
        else:
            out = [x for x in colnames if not re.match(
                '^[0-9]+(\.[0-9]+)*', x)]

        return out

    def plot(self, index: list = None):
        if index is None:
            df = self.reflectance
            alpha = 1/3
        else:
            df = self.reflectance.iloc[index, :]
            alpha = 1

        df.reset_index(inplace=True)
        df = df.melt(id_vars="index", value_vars=self.wavelength_name)
        # df.index = df.index.astype('category')
        df.variable = [float(x) for x in df.variable]

        p = ggplot(df, aes('variable', 'value', group='index'))

        if index is None:
            p += geom_line(alpha=1/3)
        else:
            p += geom_line(aes(color='factor(index)'), alpha=1)

        p += labs(x='Wavelength(nm)', y='Reflectance')
        p += theme_bw()
        p += theme(
            legend_title=element_blank(),
            legend_position='top'
        )

        return p


# ----------------------------------- main ----------------------------------- #
fpath = "spc.csv"

spc = Speclib(fpath)
spc.plot(index=[1, 10, 20])
