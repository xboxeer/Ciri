import re
sample="sample:sample2:elendil zheng"
result=re.findall('[^:]*$',sample)
result2=re.findall('[^.]*(?=:[^:]*$)',sample)
pass