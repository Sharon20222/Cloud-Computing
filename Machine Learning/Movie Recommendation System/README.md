# Movie Recommendation System with MLlib - Collaborative Filtering

## Overview

This project involves building a movie recommendation system using Apache Spark's MLlib library. The system utilizes collaborative filtering to predict user preferences and recommend movies accordingly.

## Steps Involved

### Step 1: Data Conversion

Convert MovieLens data from the format:
```
UserID  MovieID  Rating  Timestamp
196     242      3       881250949
186     302      3       891717742
...
```
to the format:
```
UserID,MovieID,Rating
196,242,3
186,302,3
...
```

Shell Script 1:
```sh
cat u.data | while read userid movieid rating timestamp
do
   echo "${userid},${movieid},${rating}"
done
```

Shell Script 2:
```sh
cat u.data | tr -s ' ' | cut -d' ' -f1-3 | tr ' ' ','
```

### Step 2: Implement MLlib Collaborative Filtering

Using the transformed data, implement the collaborative filtering algorithm provided by MLlib. The complete Python code can be found in `recommendation_example.py`.

## Enhancements and Future Improvements

- **Advanced Preprocessing:**
  - Sophisticated data cleaning
  - Include additional features (genres, demographics, timestamps)
- **Hybrid Recommendation Systems:**
  - Combine collaborative filtering with content-based filtering
  - Use matrix factorization and deep learning models
- **Scalability and Performance:**
  - Optimize for larger datasets
  - Use Apache Spark for faster processing
- **User Interface Improvements:**
  - Develop intuitive user interface
  - Implement personalized dashboards and visualizations

## Conclusion and Project Summary

- **Project Overview:**
  - Implemented movie recommendation system with MLlib collaborative filtering
  - Transformed MovieLens data format, applied ML techniques
- **Key Achievements:**
  - Functional recommendation system
  - Proficiency in data preprocessing, collaborative filtering, Python
- **Learnings:**
  - Hands-on experience with MLlib and collaborative filtering
  - Enhanced skills in data manipulation, ML, system deployment
- **Future Work:**
  - Integrate advanced features, techniques
  - Explore deployment and real-world applications

## Presentation Slides

For a detailed presentation of this project, refer to the [slides](link_to_presentation).

---
