import requests
import re
import matplotlib.pyplot as plt
import numpy as np


response=requests.get("http://www.georgetown.edu/")
txt = response.text

pattern1 = re.compile('[Rr]esearch')
research = re.findall(pattern1, txt)
print('Research and research wordcount: ' + str(len(research)))

pattern2 = re.compile('[Tt]echnology')
tech = re.findall(pattern2, txt)
print('Technology and technology wordcount: ' + str(len(tech)))

pattern3 = re.compile('[Ss]tudent')
student = re.findall(pattern3, txt)
print('Student and student wordcount: ' + str(len(student)))

count_list = [len(research),len(tech),len(student)]
y_axis = np.arange(len(count_list))
Labels = ['R|research','T|technology','S|student']
#print(count_list)

plt.bar(y_axis, count_list, align='center', alpha = 0.5)
plt.xticks(y_axis,Labels)
plt.ylabel('Count')
plt.title("Word Count")
plt.savefig('WordCount.png')