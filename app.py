from flask import Flask, request, render_template
from flask_cors import CORS
from json import loads
from github import Github
import os
from pprint import pprint

gitObject = Github(os.environ['USER'], os.environ['PASS'])

app = Flask(__name__)
CORS(app=app)

data = []

# ? Reference model
# {
#     "Name":"CircuitVerse",
#     "Repo":"https://github.com/CircuitVerse/CircuitVerse",
#     "Owner":"Shivansh Srivastava",
#     "profiles":[
#       {
#         "github":"https://github.com/Shivansh2407",
#         "linkedin":"https://www.linkedin.com/in/shivansh-srivastava24/"
#       }
#     ],
#     "Description":"CircuitVerse is a free, open-source platform which allows users to construct digital logic circuits online. We also offer the Interactive Book which teaches users on the fundamentals of modern, digital circuits.",
#     "TechStack":["Flutter","Firebase","SQlite"]
#   },


# ? Tech Stack options
# ['JS',
#  'StreamLit',
#  'django',
#  'Deep Learning',
#  'C++',
#  'Html',
#  'Markdown',
#  'NODE JS',
#  'GANs',
#  'Mongodb',
#  'Angular8',
#  'UI/UX',
#  'Dart',
#  'MERN',
#  'js',
#  'css',
#  'Pytorch',
#  'Tensorflow',
#  'ReactJS',
#  'Image Processing',
#  'Web Application',
#  'React',
#  'GraphQL',
#  'Monstack',
#  'JavaScript',
#  'Golang',
#  'ReactJs',
#  'BASH',
#  'Data Science',
#  'python',
#  'PHP',
#  'Docker',
#  'NextJS',
#  'CSS',
#  'Reactjs',
#  'Kotlin',
#  'Computer Vision',
#  'TensorFlow.JS',
#  'Django',
#  'Reinforcement Learning',
#  'bootstrap5',
#  'bootstrap',
#  'Machine Learning',
#  'Compiler Design',
#  'ANN',
#  'CSS3',
#  'flask',
#  'Bootstrap',
#  'Firebase',
#  'Flask',
#  'OpenCV',
#  'Algorithms',
#  'Data Analysis',
#  'TensorFlow',
#  'VanillaJS',
#  'Git',
#  'Data Mocking',
#  'Nodejs',
#  'API',
#  'Mangodb',
#  'Expressjs',
#  'GitHub Actions',
#  'Flutter',
#  'Express',
#  'Javascript',
#  'Python',
#  'C',
#  'MySql Database',
#  'ML',
#  'HTML',
#  'Web Dev',
#  'MaterialUI',
#  'MySQL Database',
#  'Python 3.x',
#  'MongoDB',
#  'Bootstrap4',
#  'Java',
#  'Vanilla JS',
#  'ExpressJS',
#  'Deep learning',
#  'html',
#  'NodeJS',
#  'Node.js',
#  'CNN',
#  'GOFAI',
#  'Bulma CSS',
#  'HTML5']

with open('./data.json', 'r') as projects:
    data = loads(projects.read())

temp = []
mainCount = 0
for i in data:
    count = 0
    # repo = gitObject.get_repo(i['Repo'].split('/')[len(i['Repo'].split('/')) - 2] + '/' + i['Repo'].split('/')[len(i['Repo'].split('/')) - 1])
    tempdir = {
        'gitUser': i['profiles'][0]['github'].split('/')[-1::][0],
        'gitStats': {
            # 'stars': repo.stargazers_count,
            # 'openIssues': len(list(repo.get_issues(state='open'))),

            'stars': 400,
            'openIssues': 26
        }
    }
    data[mainCount].update(tempdir)
    data[mainCount]['Description'] = data[mainCount]['Description'][0:400] + '...'
    for j in i['TechStack']:
        temp.append(j)
        if 'sql' in j.lower():
            data[mainCount]['TechStack'][count] = {
                'text': j,
                'color': 'is-info'
            }
        elif 'firebase' in j.lower():
            data[mainCount]['TechStack'][count] = {
                'text': j,
                'color': 'is-warning'
            }
        elif 'hmtl' in j.lower():
            data[mainCount]['TechStack'][count] = {
                'text': j,
                'color': 'is-danger'
            }
        elif 'react' in j.lower():
            data[mainCount]['TechStack'][count] = {
                'text': j,
                'color': 'is-link'
            }
        elif 'flutter' in j.lower():
            data[mainCount]['TechStack'][count] = {
                'text': j,
                'color': 'is-info'
            }
        elif 'js' in j.lower():
            data[mainCount]['TechStack'][count] = {
                'text': j,
                'color': 'is-warning'
            }
        elif j == 'Deep Learning':
            data[mainCount]['TechStack'][count] = {
                'text': j,
                'color': 'is-dark'
            }
        elif 'py' in j.lower():
            data[mainCount]['TechStack'][count] = {
                'text': j,
                'color': 'is-info'
            }
        elif 'django' in j.lower():
            data[mainCount]['TechStack'][count] = {
                'text': j,
                'color': 'is-primary'
            }
        elif j == 'Computer Vision':
            data[mainCount]['TechStack'][count] = {
                'text': j,
                'color': 'is-black'
            }
        elif 'css' in j.lower() or 'docker' in j.lower():
            data[mainCount]['TechStack'][count] = {
                'text': j,
                'color': 'is-link'
            }
        else:
            data[mainCount]['TechStack'][count] = {
                'text': j,
                'color': 'is-success'
            }
        count += 1
    mainCount += 1

pprint(data)

techStack = list(set(temp))
pprint(techStack)

@app.route('/')
def homeRoute():
    return render_template('home.html', data=data, Stack=techStack, filter=None)

@app.route('/filter', methods=['POST'])
def filteredData():
    techfilter = request.form.get('tech')
    retdata = []
    for project in data:
        for tech in project['TechStack']:
            if(tech['text'] == str(techfilter)):
                retdata.append(project)
                break
    return render_template('home.html', data=retdata, Stack=techStack, filter=techfilter)

if __name__ == "__main__":
    app.run(debug=True)