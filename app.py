from flask import Flask,render_template,request
import pickle
import numpy as np

popular_df=pickle.load(open('populardf.pkl','rb'))
pt=pickle.load(open('pt.pkl','rb'))
course=pickle.load(open('course.pkl','rb'))
similarity_score=pickle.load(open('similarity_score.pkl','rb'))
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           pic=list(popular_df['image'].values),
                           course_name=list(popular_df['course name'].values),
                           instr=list(popular_df['instructor'].values),
                           platf=list(popular_df['platform'].values),
                           rate=list(popular_df['rating'].values),
                           sub=list(popular_df['subject'].values),
                           lk=list(popular_df['link'].values),
                           cont=list(popular_df['description'].values))


@app.route('/recommend')
def recommend_ui():
    return render_template('first.html')

@app.route('/recommend_course',methods=['post'])
def recommend2():
    user_in = request.form.get('user_in')
    data_list = []
    v=0
    sub_name = user_in.lower()
    for i, row in course.iterrows():
        if row['subject'] == sub_name:
            itm = []
            tem_df = course[course['subject'] == sub_name][0:10]
            itm.extend(list(tem_df['course name'].values))
            itm.extend(list(tem_df['description'].values))
            itm.extend(list(tem_df['image'].values))
            itm.extend(list(tem_df['rating'].values))
            itm.extend(list(tem_df['platform'].values))
            itm.extend(list(tem_df['subject'].values))
            itm.extend(list(tem_df['link'].values))
            v = v + 1

    data_ = itm
    for i in range(10):
        it = []
        it.append(data_[i])
        it.append(data_[i + 10])
        it.append(data_[i + 20])
        it.append(data_[i + 30])
        it.append(data_[i + 40])
        it.append(data_[i + 50])
        it.append(data_[i + 60])
        data_list.append(it)
    if v != 0:
        print(data_list)
    else:
        print("SORRY FOR THE INCONVENIENCE WE WILL UPDATE SOON , UNTIL THEN YOU CAN REFER ARE TOP 50 COURSES")
    return render_template('first.html', data_list=data_list)

@app.route('/recommended')
def recommend_uix():
    return render_template('recommend.html')

@app.route('/recommend_course_',methods=['post'])
def recommend():
    user_input=request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:6]
    data = []
    for i in similar_items:
        item = []
        temp_df = course[course['course name'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('course name')['image'].values))
        item.extend(list(temp_df.drop_duplicates('course name')['course name'].values))
        item.extend(list(temp_df.drop_duplicates('course name')['description'].values))
        item.extend(list(temp_df.drop_duplicates('course name')['platform'].values))
        item.extend(list(temp_df.drop_duplicates('course name')['subject'].values))
        item.extend(list(temp_df.drop_duplicates('course name')['rating'].values))
        item.extend(list(temp_df.drop_duplicates('course name')['link'].values))
        data.append(item)
    print(data)
    return render_template('recommend.html', data=data)

if __name__=='__main__':
    app.run(debug=True)