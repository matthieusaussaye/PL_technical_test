# Content
import pandas as pd
import numpy as np

from unittest.mock import patch
import pytest


def test_remove_duplicate(previous_date,t,xr_final_t,horizons,items):
    """
    Assert that jump_month type are float or int. 
    """
    with patch("backtest_prod.OptimizerProd.__init__",
                return_value=None) :

        with patch("backtest_prod.OptimizerProd._preprocess_predictions",
                    return_value=xr_final_t) :

            BP = OptimizerProd()
            BP.previous_date = previous_date
            BP.horizons = horizons
            BP.t = t
            BP.items = items

            jump_month_dict = BP._update_jump_month()

    assert all(isinstance(jump_month_dict[keys],(int,float)) for keys in jump_month_dict.keys())

def test_jump_month_update_values(self,previous_date,t,xr_final_t,horizons,items):
    """
    Assert that jump_month are = 1 for h>0 and = 0 for h = 0.
    Since fixture t = '2021-05-31'.
    """
    with patch("backtest_prod.OptimizerProd.__init__",
                return_value=None) :

        with patch("backtest_prod.OptimizerProd._preprocess_predictions",
                    return_value=xr_final_t) :

            BP = OptimizerProd()
            BP.previous_date = previous_date
            BP.horizons = horizons
            BP.t = t 
            BP.items = items

            jump_month_dict = BP._update_jump_month()

            test_jump_month = {}
            test_jump_month.update({'jump_month:0': 0,'jump_month:11': 1, 'jump_month:16': 1, 'jump_month:21': 1, 'jump_month:6': 1})
            test_jump_month.update({f'jump_month:{h}': 1 for h in horizons[1:]})

    assert test_jump_month==jump_month_dict

def test_price_df_columns(self,t,xr_final_t,horizons,items) :
    """
    Test that columns name are good.
    """
    with patch("backtest_prod.OptimizerProd.__init__",
                return_value=None) :

        BP = OptimizerProd()
        BP.xr_final_t = xr_final_t
        BP.horizons = horizons
        BP.t = t
        BP.items = items

        price_df = BP._prices_to_dataframe()

        assert list(price_df.columns.values)==['price','quarter']

def test_price_df_values(self,t,xr_final_t,horizons,items) :
    """
    Test that contract index is well defined and that the transformation does not change prices
    """
    with patch("backtest_prod.OptimizerProd.__init__",
                return_value=None) :

        BP = OptimizerProd()
        BP.xr_final_t = xr_final_t
        BP.horizons = horizons
        BP.t = t
        BP.items = items

        price_df = BP._prices_to_dataframe()
        
        contract_date = list(pd.to_datetime(dict(year=[t.year],
                                                    day=[1],
                                                    month=[t.month+1])))[0]

        real_price = price_df.loc[(0, 1),:].price.values
        test_price = xr_final_t.sel(ref_time=t,contract_time=contract_date).values 
    assert all(real_price==test_price)

def test_update_quarter_constraint_bin(self,previous_date,t,xr_final_t,horizons,items,contracts,jump_month) :
        """
        Assert that quarter constraint numbers are all 0 or 1. 
        """
        with patch("backtest_prod.OptimizerProd.__init__",
                return_value=None) :

            with patch("backtest_prod.OptimizerProd._preprocess_predictions",
                        return_value=xr_final_t) :

                BP = OptimizerProd()
                BP.previous_date = previous_date
                BP.horizons = horizons
                BP.contracts = contracts
                BP.t = t
                BP.items = items
                BP.jump_months = jump_month 

                quarter_constraint = BP._update_quarter_constraint()

        assert all(quarter_constraint[keys] in (0,1) for keys in quarter_constraint.keys())

def test_update_quarter_constraint_h0(self,previous_date,t,xr_final_t,horizons,items,contracts,jump_month,quarters_h0) :
        """
        Assert that quarter constraint values for horizon 0 are right (no jump month). 
        """
        with patch("backtest_prod.OptimizerProd.__init__",
                return_value=None) :

            with patch("backtest_prod.OptimizerProd._preprocess_predictions",
                        return_value=xr_final_t) :

                BP = OptimizerProd()
                BP.previous_date = previous_date
                BP.horizons = horizons
                BP.contracts = contracts
                BP.t = t
                BP.items = items
                BP.jump_months = jump_month


                quarter_constraint = BP._update_quarter_constraint()
                test_quarter_h0 = quarters_h0

        assert all(quarter_constraint[keys]==test_quarter_h0[keys] for keys in test_quarter_h0.keys())

def test_update_quarter_constraint_total(self,previous_date,t,xr_final_t,horizons,items,contracts,jump_month,quarters_full_test) :
    """
    Assert that quarter constraint values for every horizons are right values. 
    """
    with patch("backtest_prod.OptimizerProd.__init__",
            return_value=None) :

        with patch("backtest_prod.OptimizerProd._preprocess_predictions",
                    return_value=xr_final_t) :

            BP = OptimizerProd()
            BP.previous_date = previous_date
            BP.horizons = horizons
            BP.contracts = contracts
            BP.t = t
            BP.items = items
            BP.jump_months = jump_month


            quarter_constraint = BP._update_quarter_constraint()

    assert all(quarters_full_test[keys]==quarter_constraint[keys] for keys in quarter_constraint.keys())

def test_non_existing_values(self,t,xr_final_t,horizons,items,contracts,non_existing_price_dict_test) :
    """
    Test that at t : non existing price bin values are right : 1 for h=0 (since day is 31) and 0 for others.
    """
    with patch("backtest_prod.OptimizerProd.__init__",
                return_value=None) :

            with patch("backtest_prod.OptimizerProd._preprocess_predictions",
                        return_value=xr_final_t) :

                BP = OptimizerProd()
                BP.horizons = horizons
                BP.contracts = contracts
                BP.t = t
                BP.items = items
                BP.xr_final_t = xr_final_t
                BP.price_df = BP._prices_to_dataframe()
                non_existing_price_predictions = BP._non_existing_price_predictions()

                assert all(non_existing_price_predictions[keys]==non_existing_price_dict_test[keys] for keys in non_existing_price_dict_test.keys())

def test_no_month_change_exposure_propagation(self,last_day_exposure,previous_date,t,horizons,items,contracts,BU,null_initial_exposure_test) :
    """
    Test class for "_non_existing_price_predictions" method if no month change
    """
    with patch("backtest_prod.OptimizerProd.__init__",
                return_value=None) :

            with patch("backtest_prod.OptimizerProd._preprocess_predictions",
                        return_value=xr_final_t) :

                BP = OptimizerProd()
                BP.previous_date = previous_date
                BP.params = last_day_exposure
                BP.horizons = horizons
                BP.contracts = contracts
                BP.business_units = BU
                BP.t = t
                BP.items = items
                BP.xr_final_t = xr_final_t

                initial_exposure = BP._propagate_initial_exposure()

                assert(all(null_initial_exposure_test[keys]==initial_exposure[keys] for keys in initial_exposure.keys()))

def test_month_change_exposure_propagation(self, BU, items, horizons, contracts, change_month_previous_date, last_day_exposure_month_change,change_month_t) :
    """
    Test class for "_non_existing_price_predictions" method when month change
    """
    with patch("backtest_prod.OptimizerProd.__init__",
                return_value=None) :

            with patch("backtest_prod.OptimizerProd._preprocess_predictions",
                        return_value=xr_final_t) :
                
                BP = OptimizerProd()
                BP.previous_date = change_month_previous_date
                BP.params = last_day_exposure_month_change
                BP.horizons = horizons
                BP.contracts = contracts
                BP.business_units = BU
                BP.t = change_month_t
                BP.items = items

                initial_exposure = BP._propagate_initial_exposure()

                assert(all(initial_exposure[f'exposure_init_{item}_{c}_{bu}']==c+1 for item in items for bu in BU for c in range(1,12)))

def test_month_change_exposure_c12(self,last_day_exposure_month_change, BU, items, contracts, horizons, change_month_previous_date, change_month_t,) :
    """
    Test class for "_non_existing_price_predictions" method when month change. Exposure contract 12 must be 0
    """
    with patch("backtest_prod.OptimizerProd.__init__",
                return_value=None) :

            with patch("backtest_prod.OptimizerProd._preprocess_predictions",
                        return_value=xr_final_t) :

                BP = OptimizerProd()
                BP.previous_date = change_month_previous_date
                BP.params = last_day_exposure_month_change
                BP.horizons = horizons
                BP.contracts = contracts
                BP.business_units = BU
                BP.t = change_month_t
                BP.items = items

                initial_exposure = BP._propagate_initial_exposure()

                assert(initial_exposure[f'exposure_init_{item}_{12}_{bu}']==0 for items in items for bu in BU)
    assert True

def test_update_calendar_weight_bin(self,previous_date,t,xr_final_t,horizons,items,contracts,jump_month) :
    """
    Assert that quarter constraint numbers are all 0 or 1. 
    """
    with patch("backtest_prod.OptimizerProd.__init__",
            return_value=None) :

        with patch("backtest_prod.OptimizerProd._preprocess_predictions",
                    return_value=xr_final_t) :

            BP = OptimizerProd()
            BP.previous_date = previous_date
            BP.horizons = horizons
            BP.contracts = contracts
            BP.t = t
            BP.items = items
            BP.jump_months = jump_month
            BP.xr_final_t = xr_final_t

            BP.price_df = BP._prices_to_dataframe()
            
            calendar_weights = BP._update_calendar_weights()

            assert all(calendar_weights[keys] in (0,1) for keys in calendar_weights.keys())

def test_update_calendar_weight_value(self,previous_date,t,xr_final_t,horizons,items,contracts,jump_month,calendar_weights_test) :
    """
    Assert that quarter constraint method compute right calendar weight binary numbers. 
    """
    with patch("backtest_prod.OptimizerProd.__init__",
            return_value=None) :

        with patch("backtest_prod.OptimizerProd._preprocess_predictions",
                    return_value=xr_final_t) :
            
            BP = OptimizerProd()
            BP.previous_date = previous_date
            BP.horizons = horizons
            BP.contracts = contracts
            BP.t = t
            BP.items = items
            BP.jump_months = jump_month
            BP.xr_final_t = xr_final_t
            
            BP.price_df = BP._prices_to_dataframe()

            calendar_weights = BP._update_calendar_weights()

            assert all(calendar_weights[keys]==calendar_weights_test[keys] for keys in calendar_weights_test.keys())


@pytest.fixture
def horizons() :
    return [0,1,2,3,4,5,10,15,20]

@pytest.fixture
def contracts() :
    return [i for i in range(1,14)]

@pytest.fixture
def items() :
    return ['RSO','SBO']

@pytest.fixture
def BU() :
    return(['Crush','Ester'])

@pytest.fixture
def t() :
    return(pd.to_datetime('2021-05-31'))

@pytest.fixture
def jump_month(horizons) :
    jump_month_dict = {}
    jump_month_dict.update({'jump_month:0': 0,'jump_month:11': 1, 'jump_month:16': 1, 'jump_month:21': 1, 'jump_month:6': 1})
    jump_month_dict.update({f'jump_month:{h}': 1 for h in horizons[1:]})
    return(jump_month_dict)

@pytest.fixture
def xr_final_t(t,horizons) :

    ref_time = np.datetime64(t)
    horizons = [[0,1,2,3,4,5,10,15,20]*12]*2
    horizons = list(np.array(horizons).flat)
    maturity = [i for i in range(1,13)]*len(horizons)*2
    user = ['RSO']*9*12+['SBO']*9*12
    mock_values = [np.random.randint(50000,100000) for i in range(216)]

    pred_time = pd.to_datetime(list(pd.to_datetime(ref_time) + BDay(h) for h in horizons))
    pred_time_m = pd.to_datetime(list(pd.to_datetime(ref_time) + BDay(h) for h in [0,1,2,3,4,5,10,15,20]))

    L=[]
    for m in maturity[:12] :
            
        contract_time_m = pd.to_datetime((dict(year=pred_time_m.year + (pred_time_m.month+m-1)//12,
                                                day=1,
                                                month=(pred_time_m.month+m-1)%12+1)))
        L.append(contract_time_m)

    contract_time = list(np.array(L).flat)+list(np.array(L).flat)

    final_index = pd.MultiIndex.from_arrays([contract_time,
                                            list(pred_time),
                                            pd.to_datetime([ref_time]*216),
                                            horizons,
                                            user],
                                            names=('contract_time', "pred_time",'ref_time','horizons','user'))

    da = xr.DataArray(data = mock_values,
                    dims = ['time'],
                    coords = dict(time=final_index),
                    indexes=final_index)

    da = da.reset_index(dims_or_levels='user')

    return(da)

@pytest.fixture
def previous_date() :
    return None

@pytest.fixture
def change_month_previous_date() :
    return pd.to_datetime('2019-07-31')

@pytest.fixture
def correct_exposure_month_change() :
    exposure = {f'exposure_{i}_{c}_{bu}_h:0': c  for i in {'RSO','SBO'} 
                                                                 for c in [i for i in range(1,14)] 
                                                                 for bu in {'Crush','Ester'}}
    exposure.update({'exposure_{i}_13_{bu}_h:0':0 for i in {'RSO','SBO'}  for bu in {'Crush','Ester'}})
    return exposure 

@pytest.fixture
def last_day_exposure_month_change() :
    last_day_exp = {f'exposure_{i}_{c}_{bu}_end_of_last_day': c for i in {'RSO','SBO'} 
                                                                 for c in [i for i in range(1,14)]
                                                                 for bu in {'Crush','Ester'}}
    return last_day_exp

@pytest.fixture
def last_day_exposure() :
    last_day_exp = {f'exposure_{i}_{c}_{bu}_end_of_last_day': 0. for i in {'RSO','SBO'} 
                                                                 for c in [i for i in range(1,14)]
                                                                 for bu in {'Crush','Ester'}}
    return last_day_exp



@pytest.fixture
def change_month_t() :
    return pd.to_datetime('2019-08-01')

@pytest.fixture
def liquidities_index() :
    liquidities_index = {
        'SBO' : { 
                #defining the Q index and the contract corresponding for SBO.
                1 : [1,2,3],
                2 : [4,5,6],
                3 : [7,8,9],
                4 : [10,11,12]
                },
        'RSO' : { 
                #defining the Q index and the contract corresponding for RSO.
                1 : [1,2,3],
                2 : [4,5,6,7,8,9],
                3 : [10,11,12]
                }
    }
    return liquidities_index
    
@pytest.fixture
def quarters_h0(liquidities_index, items) :
    liq = liquidities_index.copy()
    test_quarter_h0 = {f"liq_bin_Q_{j}:{item}_{c}_h:0":1
                                       for item in items
                                       for j in liq[item].keys()
                                       for c in liq[item][j]
                                       for h in {0}}
    return test_quarter_h0
    
@pytest.fixture
def quarters_h(liquidities_index, items, horizons) :
    test_quarter = {f"liq_bin_Q_{j}:{item}_{c+1}_h:{h}":1
                                    for item in items
                                    for j in liquidities_index[item].keys()
                                    for c in liquidities_index[item][j]
                                    for h in horizons[1:]}
    return test_quarter

@pytest.fixture
def quarters_full_test(liquidities_index, items, contracts, quarters_h0, quarters_h, horizons) :

    d = {f"liq_bin_Q_{j}:{item}_{c}_h:{h}":0
                 for item in items
                 for j in liquidities_index[item].keys()
                 for c in contracts
                 for h in horizons}

    d.update(quarters_h0)
    d.update(quarters_h)

    return d

@pytest.fixture
def non_existing_price_dict_test(horizons, items) :
    d = {f'price13_bin_{i}_h:0':1 for i in items}
    d.update({f'price13_bin_{i}_h:{h}':0 for i in items for h in horizons[1:]})
    return(d)

@pytest.fixture
def null_initial_exposure_test(items, contracts, BU) :
    return {f'exposure_init_{i}_{c}_{bu}': 0 for i in items for c in contracts for bu in BU} 

@pytest.fixture
def month_change_initial_exposure_test(items, contracts, BU) :
    return {f'exposure_init_{i}_{c}_{bu}': 0 for i in items for c in contracts for bu in BU} 
    
@pytest.fixture
def calendar_weights_test(items,contracts) :
    quarter_test_bins=['quarter_bin_SBO_1_Q:2_y:+0',
                    'quarter_bin_SBO_2_Q:3_y:+0',
                    'quarter_bin_SBO_3_Q:3_y:+0',
                    'quarter_bin_SBO_4_Q:3_y:+0',
                    'quarter_bin_SBO_5_Q:4_y:+0',
                    'quarter_bin_SBO_6_Q:4_y:+0',
                    'quarter_bin_SBO_7_Q:4_y:+0',
                    'quarter_bin_SBO_8_Q:1_y:+1',
                    'quarter_bin_SBO_9_Q:1_y:+1',
                    'quarter_bin_SBO_10_Q:1_y:+1',
                    'quarter_bin_SBO_11_Q:2_y:+1',
                    'quarter_bin_SBO_12_Q:2_y:+1',
                    'quarter_bin_SBO_13_Q:2_y:+1',
                    'quarter_bin_RSO_1_Q:2_y:+0',
                    'quarter_bin_RSO_2_Q:3_y:+0',
                    'quarter_bin_RSO_3_Q:3_y:+0',
                    'quarter_bin_RSO_4_Q:3_y:+0',
                    'quarter_bin_RSO_5_Q:4_y:+0',
                    'quarter_bin_RSO_6_Q:4_y:+0',
                    'quarter_bin_RSO_7_Q:4_y:+0',
                    'quarter_bin_RSO_8_Q:1_y:+1',
                    'quarter_bin_RSO_9_Q:1_y:+1',
                    'quarter_bin_RSO_10_Q:1_y:+1',
                    'quarter_bin_RSO_11_Q:2_y:+1',
                    'quarter_bin_RSO_12_Q:2_y:+1',
                    'quarter_bin_RSO_13_Q:2_y:+1']

    cal_w_test = {f'quarter_bin_{item}_{c}_Q:{q}_y:+{y}':0 for q in range(1,5) 
                                                            for item in items 
                                                            for y in [0,1,2] 
                                                            for c in contracts}

    cal_w_test.update({keys:1 for keys in quarter_test_bins})
       
    return cal_w_test
