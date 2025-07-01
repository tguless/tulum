#!/usr/bin/env python3

from datetime import datetime

# Property details
purchase_price = 190000
closing_costs_pct = 0.08
closing_costs = purchase_price * closing_costs_pct
total_investment = purchase_price + closing_costs

# Monthly costs
hoa_tax_monthly = 500
property_mgmt_pct = 0.25
maintenance_monthly = 150
insurance_monthly = 100
fideicomiso_annual = 600
monthly_fixed_costs = hoa_tax_monthly + maintenance_monthly + insurance_monthly + (fideicomiso_annual/12)

# Rental income modeling
high_season_months = 5  # Nov-Mar
shoulder_season_months = 3  # Apr, May, Oct
low_season_months = 4  # Jun-Sep

# Occupancy rates scenarios
occupancy_scenarios = {
    'conservative': {'high': 0.65, 'shoulder': 0.45, 'low': 0.30},
    'base': {'high': 0.75, 'shoulder': 0.55, 'low': 0.40},
    'optimistic': {'high': 0.85, 'shoulder': 0.65, 'low': 0.50}
}

# Nightly rates scenarios
nightly_rate_scenarios = {
    'conservative': {'high': 150, 'shoulder': 120, 'low': 100},
    'base': {'high': 180, 'shoulder': 140, 'low': 120},
    'optimistic': {'high': 210, 'shoulder': 160, 'low': 140}
}

# Calculate annual rental income for different scenarios
results = {}

for scenario in ['conservative', 'base', 'optimistic']:
    occ = occupancy_scenarios[scenario]
    rates = nightly_rate_scenarios[scenario]
    
    high_season_income = high_season_months * 30 * occ['high'] * rates['high']
    shoulder_season_income = shoulder_season_months * 30 * occ['shoulder'] * rates['shoulder']
    low_season_income = low_season_months * 30 * occ['low'] * rates['low']
    
    annual_gross_income = high_season_income + shoulder_season_income + low_season_income
    
    # Property management fee
    mgmt_fee = annual_gross_income * property_mgmt_pct
    
    # Annual fixed costs
    annual_fixed_costs = monthly_fixed_costs * 12
    
    # Net income
    annual_net_income = annual_gross_income - mgmt_fee - annual_fixed_costs
    
    # ROI calculations
    cash_on_cash_roi = (annual_net_income / total_investment) * 100
    
    # Appreciation scenarios (annual)
    appreciation_rates = {'low': 0.03, 'mid': 0.05, 'high': 0.08}
    
    # 5-year projections
    five_year_results = {}
    for app_scenario, app_rate in appreciation_rates.items():
        property_value_5yr = purchase_price * ((1 + app_rate) ** 5)
        equity_5yr = property_value_5yr - purchase_price
        total_rental_income_5yr = annual_net_income * 5
        total_return_5yr = equity_5yr + total_rental_income_5yr
        roi_5yr = (total_return_5yr / total_investment) * 100
        annualized_roi_5yr = ((1 + roi_5yr/100) ** (1/5) - 1) * 100
        
        five_year_results[app_scenario] = {
            'property_value': property_value_5yr,
            'equity_gain': equity_5yr,
            'rental_income': total_rental_income_5yr,
            'total_return': total_return_5yr,
            'total_roi_pct': roi_5yr,
            'annualized_roi': annualized_roi_5yr
        }
    
    results[scenario] = {
        'annual_gross_income': annual_gross_income,
        'mgmt_fee': mgmt_fee,
        'annual_fixed_costs': annual_fixed_costs,
        'annual_net_income': annual_net_income,
        'cash_on_cash_roi': cash_on_cash_roi,
        'five_year_results': five_year_results
    }

# Print summary results
print('\n===== TULUM PROPERTY INVESTMENT ANALYSIS =====')
print(f'Property Purchase Price: ${purchase_price:,}')
print(f'Closing Costs (8%): ${closing_costs:,.2f}')
print(f'Total Investment: ${total_investment:,.2f}')
print(f'Monthly Fixed Costs: ${monthly_fixed_costs:,.2f}\n')

print('ANNUAL RENTAL INCOME SCENARIOS:')
for scenario in ['conservative', 'base', 'optimistic']:
    r = results[scenario]
    print(f'\n{scenario.upper()} SCENARIO:')
    print(f'Gross Annual Income: ${r["annual_gross_income"]:,.2f}')
    print(f'Property Management (25%): ${r["mgmt_fee"]:,.2f}')
    print(f'Fixed Costs: ${r["annual_fixed_costs"]:,.2f}')
    print(f'Net Annual Income: ${r["annual_net_income"]:,.2f}')
    print(f'Cash-on-Cash ROI: {r["cash_on_cash_roi"]:.2f}%')
    
    print('\n5-YEAR PROJECTIONS:')
    for app_scenario, values in r['five_year_results'].items():
        app_rate = appreciation_rates[app_scenario] * 100
        print(f'  {app_scenario.upper()} APPRECIATION ({app_rate:.1f}%):')
        print(f'  - Property Value after 5 years: ${values["property_value"]:,.2f}')
        print(f'  - Equity Gain: ${values["equity_gain"]:,.2f}')
        print(f'  - Total Rental Income: ${values["rental_income"]:,.2f}')
        print(f'  - Total Return: ${values["total_return"]:,.2f}')
        print(f'  - Total ROI: {values["total_roi_pct"]:.2f}%')
        print(f'  - Annualized ROI: {values["annualized_roi"]:.2f}%')

print('\nOCCUPANCY ASSUMPTIONS:')
for scenario, values in occupancy_scenarios.items():
    print(f'{scenario.capitalize()}: High Season: {values["high"]*100}%, Shoulder: {values["shoulder"]*100}%, Low: {values["low"]*100}%')

print('\nNIGHTLY RATE ASSUMPTIONS:')
for scenario, values in nightly_rate_scenarios.items():
    print(f'{scenario.capitalize()}: High Season: ${values["high"]}, Shoulder: ${values["shoulder"]}, Low: ${values["low"]}') 