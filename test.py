# # # # import json
# # # # import pprint
# # # # #
# # # # # data = {}
# # # # # data['people'] = []
# # # # # data['people'].append({
# # # # #     'name': 'Scott',
# # # # #     'website': 'stackabuse.com',
# # # # #     'from': 'Nebraska'
# # # # # })
# # # # # data['people'].append({
# # # # #     'name': 'Larry',
# # # # #     'website': 'google.com',
# # # # #     'from': 'Michigan'
# # # # # })
# # # # # data['people'].append({
# # # # #     'name': 'Tim',
# # # # #     'website': 'apple.com',
# # # # #     'from': 'Alabama'
# # # # # })
# # # # #
# # # # # with open('data.txt', 'w') as outfile:
# # # # #     json.dump(data, outfile)
# # # #
# # # # with open('data.txt','r') as f:
# # # #     # pprint.pprint(json.load(f))
# # #
# # import datetime
# # import pytz
# #
# # print(datetime.datetime.utcnow().strftime('%b | %d | %Y  %H:%M:%S  %Z'))
# # print(pytz.utc.localize(datetime.datetime.now()))
# #
# # b= pytz.utc.localize(datetime.datetime.utcnow())
# # print(b)
# # tz=pytz.timezone('EET')
# # print(tz)
# # print(tz.localize(datetime.datetime.now()))
#
# from itertools import accumulate
#
# lst = [[5,6,8],[8,5,3],[9,10,3]]
# print(list(accumulate(lst, lambda x,y : list(set(y)-set(x)))))

# for i in range(1,10,2):
#     print(f'{"^"*i:^12}')
import time
import sys

