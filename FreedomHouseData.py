import csv
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

def simple_get(url):
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None
def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
    and content_type is not None
    and content_type.find('html') > -1)
def log_error(e):
    print(e)
        
country_dataset = {
    'country' : [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018]
}
csv_files = ['AggregateScores2018.csv', 'AggregateScores2017.csv', 'AggregateScores2016.csv', 'AggregateScores2015.csv',
            'AggregateScores2014.csv', 'AggregateScores2013.csv', 'AggregateScores2012.csv', 'AggregateScores2011.csv', 
            'AggregateScores2010.csv']
for file in csv_files:
    with open(file, 'r') as f:
        next(f)
        for row in f:
            #print(row)
            parts = row.split(',')
            country_name = parts[0]
            if(country_name[-1] == '*'):
                country_name = country_name[:-1]
            score = int(parts[-1])
            country_data = country_dataset.get(country_name)
            if country_data is None:
                country_data = []
            country_data.insert(0, score)
            country_dataset[country_name] = country_data
country_dataset.pop('Puerto Rico')
country_dataset.pop('Israeli Occupied Territories')
country_dataset.pop('Palestinian Authority Administered Territories')
#country_dataset.pop("Cote d'Ivoire")
#country_dataset.pop('Sao Tome and Principe')
country_dataset.pop('Swaziland')
country_dataset.pop('Syria')
country_dataset.pop('The Gambia')
#print(country_dataset)
#data_file = open('PredictedData.txt', 'w')
x = country_dataset['country']
#data_file.write('Freedom House 2019 and 2020 predicted scores')
country_names = []
scores_2019 = []
scores_2029 = []
dict_scores_2019 = dict()
dict_scores_2029 = dict()
print('Freedom House 2019 and 2020 predicted scores')
for country in country_dataset:
    if country != 'country':
        #data_file.write(str(country_dataset[country])+'\\n')
        print(str(country_dataset[country]))
        y = country_dataset[country]
        if len(x) == len(y):
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
            #data_file.write(str(country))
            print(country)
            #data_file.write('Slope: '+str(slope))
            print('Slope: '+str(slope))
            #data_file.write('Intercept: '+str(intercept))
            print('Intercept: '+str(intercept))
            #data_file.write('r-value: '+str(r_value))
            #print('r-value: '+str(r_value))
            #data_file.write('p-value: '+str(p_value))
            #print('p-value: '+str(p_value))
            #data_file.write('Standard Deviation Error: '+str(std_err))
            #print('Standard Deviation Error: '+str(std_err))
            country_names.append(country)
            for i in range(2019, 2030):
                country_score = (slope * i) + intercept
                if country_score < 1:
                    country_score = 1
                elif country_score > 100:
                    country_score = 100
                #data_file.write(country+' '+str(i)+' predicted score: '+str(int(country_score)))
                if i == 2019:
                    scores_2019.append(int(country_score))
                    dict_scores_2019[country] = int(country_score)
                elif i == 2029:
                    scores_2029.append(int(country_score))
                    dict_scores_2029[country] = int(country_score)
            #data_file.write()
            print()
'''
print(country_names)
print(len(country_names))
print(scores_2019)
print(len(scores_2019))
print(scores_2029)
print(len(scores_2029))
print(dict_scores_2019)
print(dict_scores_2029)
'''
    
raw_html = simple_get('https://freedomhouse.org/report/countries-world-freedom-2019')
html = BeautifulSoup(raw_html, 'html.parser')
actual_2019_scores = dict()
country_name_two = ''
score = 0
#country_dataset.pop('Swaziland')
#country_dataset.pop('Syria')
#country_dataset.pop('The Gambia')
for i, td in enumerate(html.select('td')):
    index = i
    if index % 7 == 1:
        #print(i, td.text)
        country_name_two = td.text
        #print(country_name_two)
        country_name_two.strip()
        #print(country_name_two)
        if country_name_two[-2] == '*':
            country_name_two = country_name_two[:-2]
        else:
            country_name_two = country_name_two[:-1]
        country_name_two = country_name_two[1:]
        country_name_two = country_name_two.strip()
        if country_name_two == 'Congo, Democratic Republic of (Kinshasa)':
            country_name_two = 'Congo (Kinshasa)'
        if country_name_two == 'Congo, Republic of (Brazzaville)':
            country_name_two = 'Congo (Brazzaville)'
        if country_name_two == "Côte d'Ivoire":
            country_name_two = "Cote d'Ivoire"
        if country_name_two == 'São Tomé and Príncipe':
            country_name_two = 'Sao Tome and Principe'
        if country_name_two == 'St. Vincent and Grenadines':
            country_name_two = 'St. Vincent and the Grenadines'
        if country_name_two == 'North Macedonia':
            country_name_two = 'Macedonia'
    elif index % 7 == 6:
        #print(i, td.text)
        score = int(td.text)
    if country_name_two != '' and score != 0:
        if country_name_two.find('(Translation)') == -1 and country_name_two.find('(Spanish)') == -1: 
            actual_2019_scores[country_name_two] = score
        country_name_two = ''
        score = 0
percent_diff = dict()
print(dict_scores_2019) 
#print(len(dict_scores_2019))
print(actual_2019_scores)
#print(len(actual_2019_scores))
predicted = []
actual = []
percentages = []
differences = []
sum_percentage = 0.0
for country in dict_scores_2019:
    predicted_score = dict_scores_2019[country]
    if actual_2019_scores[country] is None:
        continue
    if actual_2019_scores[country] is not None: 
        actual_score = float(actual_2019_scores[country])
        predicted.append(predicted_score)
        actual.append(actual_score)
        differences.append(abs(predicted_score - actual_score))
        percent_difference = abs(predicted_score - actual_score) / actual_score
        percent_diff[country] = percent_difference * 100
        percentages.append(percent_diff[country])
        sum_percentage += percent_diff[country]
print(percent_diff)
average_error = sum_percentage/len(percent_diff)
print(str(average_error))
    
plt.plot(predicted, actual, 'bo')
plt.axis([0, 100, 0, 100])
plt.title('Predicted 2019 Values vs Actual 2019 Values')
plt.xlabel('Predicted 2019 Value')
plt.ylabel('Actual 2019 Value')
plt.show()
slope, intercept, r_value, p_value, std_err = stats.linregress(predicted, actual)
print('Average Accuracy: '+str(slope))
print('Average Error Difference: '+str(intercept))
print('r-value: '+str(r_value))
print('p-value: '+str(p_value))
print('Standard Deviation Error: '+str(std_err))
    
plt.plot(actual, percentages, 'bo')
plt.axis([0, 100, 0, 150])
plt.title('Actual 2019 Values vs Percent Error')
plt.xlabel('Actual 2019 Value')
plt.ylabel('Percent Error')
plt.show()
    
plt.plot(actual, differences, 'bo')
plt.axis([0, 100, 0, 30])
plt.title('Actual 2019 Values vs Difference Error')
plt.xlabel('Actual 2019 Value')
plt.ylabel('Difference Error')
plt.show()

n, bins, patches = plt.hist(percentages, [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130], density=False, facecolor='b')
plt.xlabel('Percent Error')
plt.ylabel('Number of Countries')
plt.title('Percentage Error Distribution')
plt.show()
print(n)
print(bins)
print(patches)
    
n, bins, patches = plt.hist(scores_2029, [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110], density = False, facecolor = 'r')
plt.xlabel('Freedom Score')
plt.ylabel('Number of Countires')
plt.title('Predicted Freedom Scores Distribution 2029')
plt.show()
print(n)
print(bins)
print(patches)
    
n, bins, patches = plt.hist(predicted, [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110], density = False, facecolor = 'r')
plt.xlabel('Predicted Freedom Score')
plt.ylabel('Number of Countries')
plt.title('Predicted Freedom Scores Distribution 2019')
plt.show()
print(n)
print(bins)
print(patches)
    
n, bins, patches = plt.hist(actual, [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110], density = False, facecolor = 'g')
plt.xlabel('Freedom Score')
plt.ylabel('Number of Countries')
plt.title('Actual Freedom Scores Distribution 2019')
plt.show()
print(n)
print(bins)
print(patches)