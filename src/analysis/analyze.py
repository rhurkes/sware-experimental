from shapely.geometry import Point, Polygon
from datetime import datetime, timedelta
import pickle, statistics

# TODO just ignore Florida tornadoes and polys with 2 points
# TODO allow analysis by radius around point, or polygon (dixie alley, chase alley, upslope, etc.)

START_YEAR = 2014
END_YEAR = 2020
YEARS_ANALYZED = 7
TESTING_UPSLOPE = False
N_CHASE_ALLEY = Polygon([(-107, 50), (-107, 43), (-100, 42), (-93, 42), (-93, 45.5), (-95.66, 50)])
UPSLOPE = Polygon([(-107, 43), (-107, 43), (-100, 34), (-100, 42)])
C_CHASE_ALLEY = Polygon([(-100, 42), (-100, 34), (-93, 34), (-93, 42)])
S_CHASE_ALLEY = Polygon([(-107, 34), (-107, 25), (-93, 25), (-93, 34)])
MIDWEST = Polygon([(-93, 45.5), (-93, 36), (-84, 36), (-84, 43.5), (-95.66, 50)])
DIXIE_ALLEY = Polygon([(-93, 36), (-93, 25), (-84, 25), (-84, 36)])
CHASE_ZONES = [N_CHASE_ALLEY, UPSLOPE, C_CHASE_ALLEY, S_CHASE_ALLEY, MIDWEST, DIXIE_ALLEY]

# Dict of all outlooks, keyed by date (eg. 20170516)
with open('outlooks.pkl', 'rb') as file:
    outlooks = pickle.load(file)

# List of all reports in format: dt, state, rating, start, end, length, width
with open('tornado_reports.pkl', 'rb') as file:
    reports = pickle.load(file)
# Limit analysis of reports potentially impact by the "Florida problem"
reports = [x for x in reports if x['state'] != 'FL']

agg_risk_count = {None: 0, '0.02': 0, '0.05': 0, '0.10': 0, '0.15': 0, '0.30': 0, 'SIGN': 0}
agg_reports_per_risk = {None: 0, '0.02': 0, '0.05': 0, '0.10': 0, '0.15': 0, '0.30': 0, 'SIGN': 0}
agg_sign_count = {'0.02': 0, '0.05': 0, '0.10': 0, '0.15': 0, '0.30': 0}
agg_report_count = 0
agg_days_count = 0
agg_days_with_report = 0
agg_report_in_10 = 0
agg_report_in_10_sign = 0
agg_10_no_sign_day_count = 0
agg_10_sign_day_count = 0
agg_10_no_sign_ef = 0
agg_10_sign_ef = 0
agg_risk_ef = {None: 0, '0.02': 0, '0.05': 0, '0.10': 0, '0.15': 0, '0.30': 0, 'SIGN': 0}

def get_highest_risk(outlook):
    keys = [x for x in outlook.keys() if x != 'SIGN']
    keys = sorted(keys, reverse=True)
    return None if len(keys) == 0 else keys[0]

# date format: 20170518
def analyze_date(date):
    highest_risk = get_highest_risk(outlooks[date])
    date_reports = [x for x in reports if x['date'] == date]
    reports_count = len(date_reports)
    
    # Update aggregate stats
    global agg_days_count
    global agg_report_count
    global agg_days_with_report
    global agg_risk_count
    global agg_sign_count
    global agg_reports_per_risk

    agg_days_count += 1
    agg_report_count += reports_count
    if reports_count > 0:
        agg_days_with_report += 1
    agg_risk_count[highest_risk] += 1
    agg_reports_per_risk[highest_risk] += reports_count
    if 'SIGN' in outlooks[date]:
        if highest_risk == None:
            return
        agg_sign_count[highest_risk] += 1
        agg_risk_count['SIGN'] += 1
        agg_reports_per_risk['SIGN'] += reports_count

def analyze_dates():
    dt = datetime(START_YEAR, 1, 1)
    while dt.year <= END_YEAR:
        date = dt.strftime('%Y%m%d')
        analyze_date(date)
        dt = dt + timedelta(days=1)

def analyze_reports():
    global agg_report_in_10
    global agg_report_in_10_sign
    global agg_10_no_sign_day_count
    global agg_10_sign_day_count
    global agg_10_no_sign_ef
    global agg_10_sign_ef
    global agg_risk_ef

    for report in reports:
        point = Point(report['start'])
        date = report['date']
        outlook = outlooks[date]
        highest_risk = get_highest_risk(outlook)
        agg_risk_ef[highest_risk] += report['length']
        
        # Decorate each report with risk
        risk_found = False
        reversed_risks = sorted(outlook.keys(), reverse=True)
        reversed_risks = [x for x in reversed_risks if x != 'SIGN']
        for risk in reversed_risks:
            if risk_found:
                continue
            for poly in outlook[risk]:
                if risk_found:
                    continue
                if len(poly) < 3:
                    continue
                if Polygon(poly).contains(point):
                    report['risk'] = risk
                    risk_found = True
        if not risk_found:
            report['risk'] = None

        # 10% SIGN Analysis
        if '0.10' in outlook:
            for poly in outlook['0.10']:
                if Polygon(poly).contains(point):
                    agg_report_in_10 += 1
            if 'SIGN' in outlook:
                agg_10_sign_day_count += 1
                agg_10_sign_ef += report['length']
                for poly in outlook['SIGN']:
                    if Polygon(poly).contains(point):
                        agg_report_in_10_sign += 1
            else:
                agg_10_no_sign_day_count += 1
                agg_10_no_sign_ef += report['length']

def percent(a, b):
    if b == 0:
        return '0%'
    else:
        return f'{int((a / b) * 100)}%'

def analyze(zone):
    global outlooks
    global reports

    # Zone filtering
    if zone:
        original_count = len(reports)
        reports = [x for x in reports if zone.contains(Point(x['start']))]
        filtered_count = len(reports)
        print(f'Filtered down to {filtered_count} reports ({percent(filtered_count, original_count)})')
        new_outlooks = {}
        for date in outlooks:
            new_outlook = {}
            outlook = outlooks[date]
            for risk in outlook:
                for poly in outlook[risk]:
                    # The Florida problem
                    if len(poly) < 3:
                        continue
                    center = Polygon(poly).centroid
                    if zone.contains(center):
                        if risk not in new_outlook:
                            new_outlook[risk] = []
                        new_outlook[risk].append(poly)
            new_outlooks[date] = new_outlook
        outlooks = new_outlooks

    # Build analysis aggregates
    analyze_dates()
    analyze_reports()

    # How many days are tornado days
    print(f'\nTornado days: {agg_days_with_report}/{agg_days_count} ({percent(agg_days_with_report, agg_days_count)})')
    # How many tornadoes mean on a tornado day
    print(f'\nTornadoes/day: {int(len(reports) / agg_days_with_report)}')
    # How many tornadoes mean on each risk day
    print('\nHow many tornadoes mean on each risk day:')
    for key in agg_reports_per_risk:
        if agg_risk_count[key] == 0:
            print(f'{key}: 0')
        else:
            print(f'{key}: {int(agg_reports_per_risk[key] / agg_risk_count[key])}')
    # TODO tornado/day percentiles
    # How many days of each risk
    print('\nHow many days had each risk as the highest risk:')
    for key in agg_risk_count:
        if key != 'SIGN':
            pct = percent(agg_risk_count[key], agg_days_count)
            per_year = int(agg_risk_count[key] / YEARS_ANALYZED)
            print(f'{key}: {agg_risk_count[key]} ({pct}) ({per_year}/year)')
    # How many days of each risk have SIGN
    print('\nHow many days of each risk have SIGN:')
    for key in agg_sign_count:
        pct = percent(agg_sign_count[key], agg_risk_count[key])
        print(f'{key}: {agg_sign_count[key]} ({pct})')
    # Breakdown of sign on mean for 10%
    print('\nHow does SIGN impact mean tornadoes within the highest risk on 10% days')
    print(f'10%: {agg_10_no_sign_day_count / agg_report_in_10}')
    print(f'10% w/SIGN: {agg_10_sign_day_count / agg_report_in_10_sign}')
    print('\nHow does SIGN impact mean EF rating:')
    print(f'10% no SIGN: {agg_10_no_sign_ef / agg_report_in_10}')
    print(f'10% SIGN: {agg_10_sign_ef / agg_report_in_10_sign}')
    for key in agg_risk_ef:
        if agg_reports_per_risk[key] == 0:
            print(f'{key}: 0')
        else:
            print(f'{key}: {agg_risk_ef[key] / agg_reports_per_risk[key]}')
    # TODO where is the highest concentration of 5s? 10s? 15s? 30s? SIGNS?
    # TODO how does this vary in regions?
    # TODO how often this upgrade and/or change nature significantly?

# analyze_date('20170518')
analyze(DIXIE_ALLEY)
