import numpy as np
import pandas as pd


def docking_power_df(docking_power_df: pd.DataFrame,
                     rmsd_cutoff: float) -> dict:
    """Compute CASF 2016 Docking power

    Args:
        docking_power_df (pd.DataFrame): A DF containing all scores and rmsd
            for all docking power decoys
        rmsd_cutoff (float): The RMSD cutoff (in angstrom) to define near-native docking pose

    Returns:
        dict: A dictionnary containing SP[2-10] and TOP[1-3]
    """
    # Adapted from CASF 2016/Docking_power.py
    pdb_list = list(set(docking_power_df['pdb_id'].to_list()))
    Top1 = pd.DataFrame(index=pdb_list, columns=['success'])
    Top2 = pd.DataFrame(index=pdb_list, columns=['success'])
    Top3 = pd.DataFrame(index=pdb_list, columns=['success'])
    SP2 = pd.DataFrame(index=pdb_list, columns=['spearman'])
    SP3 = pd.DataFrame(index=pdb_list, columns=['spearman'])
    SP4 = pd.DataFrame(index=pdb_list, columns=['spearman'])
    SP5 = pd.DataFrame(index=pdb_list, columns=['spearman'])
    SP6 = pd.DataFrame(index=pdb_list, columns=['spearman'])
    SP7 = pd.DataFrame(index=pdb_list, columns=['spearman'])
    SP8 = pd.DataFrame(index=pdb_list, columns=['spearman'])
    SP9 = pd.DataFrame(index=pdb_list, columns=['spearman'])
    SP10 = pd.DataFrame(index=pdb_list, columns=['spearman'])
    docking_results_columns = ['code', 'Rank1', 'RMSD1', 'Rank2',
                               'RMSD2', 'Rank3', 'RMSD3']
    docking_results = pd.DataFrame(index=range(1, len(pdb_list) + 1),
                                   columns=docking_results_columns)

    tmp = 1
    for pdb in pdb_list:
        docking_power_df_pdb = docking_power_df.loc[docking_power_df['pdb_id'] == pdb]
        df_sorted = docking_power_df_pdb.sort_values(
            by=['score'], ascending=[False])
        docking_results.loc[tmp]['Rank1'] = ''.join(df_sorted[0:1]['#code'])
        docking_results.loc[tmp]['RMSD1'] = float(df_sorted[0:1]['rmsd'])
        docking_results.loc[tmp]['Rank2'] = ''.join(df_sorted[1:2]['#code'])
        docking_results.loc[tmp]['RMSD2'] = float(df_sorted[1:2]['rmsd'])
        docking_results.loc[tmp]['Rank3'] = ''.join(df_sorted[2:3]['#code'])
        docking_results.loc[tmp]['RMSD3'] = float(df_sorted[2:3]['rmsd'])
        docking_results.loc[tmp]['code'] = pdb
        tmp += 1
        for j in np.arange(1, 4):
            minrmsd = df_sorted[0:j]['rmsd'].min()
            varname = 'Top' + str(j)
            top = locals()[varname]
            if minrmsd <= rmsd_cutoff:
                top.loc[pdb]['success'] = 1
            else:
                top.loc[pdb]['success'] = 0
        for s in np.arange(2, 11):
            sptemp = docking_power_df_pdb[docking_power_df_pdb.rmsd <= s]
            varname2 = 'SP' + str(s)
            sp = locals()[varname2]
            if float(sptemp.shape[0]) >= 5:
                sp.loc[pdb]['spearman'] = np.negative(
                    sptemp.corr('spearman')['rmsd']['score'])
            else:
                continue

    SP2 = SP2.dropna(subset=['spearman'])
    SP3 = SP3.dropna(subset=['spearman'])
    SP4 = SP4.dropna(subset=['spearman'])
    SP5 = SP5.dropna(subset=['spearman'])
    SP6 = SP6.dropna(subset=['spearman'])
    SP7 = SP7.dropna(subset=['spearman'])
    SP8 = SP8.dropna(subset=['spearman'])
    SP9 = SP9.dropna(subset=['spearman'])
    SP10 = SP10.dropna(subset=['spearman'])

    top1_success = float(Top1['success'].sum()) / float(Top1.shape[0]) * 100
    top2_success = float(Top2['success'].sum()) / float(Top2.shape[0]) * 100
    top3_success = float(Top3['success'].sum()) / float(Top3.shape[0]) * 100

    sp2 = round(SP2['spearman'].mean(), 3)
    sp3 = round(SP3['spearman'].mean(), 3)
    sp4 = round(SP4['spearman'].mean(), 3)
    sp5 = round(SP5['spearman'].mean(), 3)
    sp6 = round(SP6['spearman'].mean(), 3)
    sp7 = round(SP7['spearman'].mean(), 3)
    sp8 = round(SP8['spearman'].mean(), 3)
    sp9 = round(SP9['spearman'].mean(), 3)
    sp10 = round(SP10['spearman'].mean(), 3)

    top1_correct = Top1['success'].sum()
    top2_correct = Top2['success'].sum()
    top3_correct = Top3['success'].sum()

    res_dict = {"sp2": sp2,
                "sp3": sp3,
                "sp4": sp4,
                "sp5": sp5,
                "sp6": sp6,
                "sp7": sp7,
                "sp8": sp8,
                "sp9": sp9,
                "sp10": sp10,
                "top1_correct": top1_correct,
                "top1_success": top1_success,
                "top2_correct": top2_correct,
                "top2_success": top2_success,
                "top3_correct": top3_correct,
                "top3_success": top3_success}

    return res_dict