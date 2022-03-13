from outlook_client import get_tornado_risks

# Day 1 outlooks are available at 0600z, 1300z, 1630z, 2000z
hour = '1300'
date = '2021-03-13'
risks = get_tornado_risks(date, hour)
print(risks)
