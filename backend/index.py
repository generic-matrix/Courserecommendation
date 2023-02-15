import pandas as pd
import neattext.functions as nfx
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity,linear_kernel
from pathlib import Path
from flask import Flask, request, jsonify
import json
from flask_cors import CORS


class RecommendCourses:
  def __init__(self):
    #create a dataframe 
    dirname = Path.cwd().as_posix()
    business_df = pd.read_csv(dirname+'/dataset/3.1-data-sheet-udemy-courses-business-courses.csv')
    design_df = pd.read_csv(dirname+'/dataset/3.1-data-sheet-udemy-courses-design-courses.csv')
    music_df = pd.read_csv(dirname+'/dataset/3.1-data-sheet-udemy-courses-music-courses.csv')
    web_df = pd.read_csv(dirname+'/dataset/3.1-data-sheet-udemy-courses-web-development.csv')
    entry_df = pd.read_csv(dirname+'/dataset/Entry Level Project Sheet - 3.1-data-sheet-udemy-courses-web-development.csv')
    df = pd.concat([business_df, design_df,music_df,web_df,entry_df])

    #drop duplicates from the course_title column
    df = df.drop_duplicates(subset=['course_title'])
    # clean_title column to string from course_title
    df['clean_title'] = df['course_title'].astype(str)
    # clean_title remove stopwords
    df['clean_title'] = df['clean_title'].apply(nfx.remove_stopwords)
    # clean_title remove special characters
    df['clean_title'] = df['clean_title'].apply(nfx.remove_special_characters)

    # create CountVectorizer
    countvect = CountVectorizer()
    cv_mat = countvect.fit_transform(df['clean_title'])

    # create CV words
    df_cv_words = pd.DataFrame(cv_mat.todense(),columns=countvect.get_feature_names())
    self.df = df
    self.cosine_sim_mat = cosine_similarity(cv_mat)
    print("Data loaded Successfully")

  def autocomplete(self,query):
    result = self.df.loc[self.df['clean_title'].str.contains(query, case=False)]
    print(result)
    data = []
    index = 0
    for obj in result["course_title"][0:5]:
      data.append({
          "key":index,
          "value":obj
      })
      index = index + 1
    return data
  
  def recommend_course(self,title,numrec = 10):
    course_index = pd.Series( self.df.index, index=self.df['course_title']).drop_duplicates()
    if title in course_index:
      index = course_index[title]
      scores = list(enumerate(self.cosine_sim_mat [index]))
      sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
      selected_course_index = [i[0] for i in sorted_scores[1:]]
      selected_course_score = [i[1] for i in sorted_scores[1:]]
      rec_df = self.df.iloc[selected_course_index]
      rec_df['Similarity_Score'] = selected_course_score
      final_recommended_courses = rec_df[['course_title', 'Similarity_Score', 'url', 'price', 'num_subscribers']]
      result = final_recommended_courses.head(numrec).to_json(orient ='index')
      parsed = json.loads(result)
      return {"error":None,"data":parsed}
    else:
      return {"error": "course with title name "+title+" not found"}


app = Flask(__name__)
CORS(app)
recommendation = RecommendCourses()



@app.route("/recommend", methods=["GET"])
def recommend():
    query = request.args.get("query")
    if query is None:
        return jsonify({'error' : 'Malformed Request'})
    else:
        #Introduction Financial Modeling
        return recommendation.recommend_course(query,20)

@app.route("/autocomplete", methods=["GET"])
def autocomplete():
    query = request.args.get("query")
    if query is None:
        return jsonify({'error' : 'Malformed Request'})
    else:
        return jsonify(recommendation.autocomplete(query))
    


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5001,debug=True)

