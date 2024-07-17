import pandas as pd
from pyspark.sql.functions import col, explode
from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.ml.evaluation import RegressionEvaluator

from pyspark.ml.recommendation import ALS
from pyspark.ml.tuning import ParamGridBuilder, CrossValidator

# Initiate Spark session
spark = SparkSession.builder.appName('Recommendations').getOrCreate()

# Load data
movies = spark.read.csv("gs://movie_bucket11/movies.csv", header=True)
ratings = spark.read.csv("gs://movie_bucket11/ratings.csv", header=True)

# Data preprocessing
ratings = ratings.withColumn('userId', col('userId').cast('integer')) \
    .withColumn('movieId', col('movieId').cast('integer')) \
    .withColumn('rating', col('rating').cast('float')).drop('timestamp')

# Split data into training and test sets
(train, test) = ratings.randomSplit([0.8, 0.2], seed=1234)

# Create ALS model
als = ALS(userCol="userId", itemCol="movieId", ratingCol="rating", nonnegative=True, implicitPrefs=False, coldStartStrategy="drop")

# Hyperparameter tuning
param_grid = ParamGridBuilder() \
            .addGrid(als.rank, [10, 50, 100, 150]) \
            .addGrid(als.regParam, [.01, .05, .1, .15]) \
            .build()

evaluator = RegressionEvaluator(metricName="rmse", labelCol="rating", predictionCol="prediction")

cv = CrossValidator(estimator=als, estimatorParamMaps=param_grid, evaluator=evaluator, numFolds=5)

# Train model
model = cv.fit(train)
best_model = model.bestModel

# Print best model parameters
print("**Best Model**")
print("  Rank:", best_model._java_obj.parent().getRank())
print("  MaxIter:", best_model._java_obj.parent().getMaxIter())
print("  RegParam:", best_model._java_obj.parent().getRegParam())

# Evaluate model
test_predictions = best_model.transform(test)
RMSE = evaluator.evaluate(test_predictions)
print("RMSE:", RMSE)

# Generate recommendations
nrecommendations = best_model.recommendForAllUsers(10)
nrecommendations = nrecommendations.withColumn("rec_exp", explode("recommendations")) \
    .select('userId', col("rec_exp.movieId"), col("rec_exp.rating"))

# Show sample recommendations
nrecommendations.limit(10).show()
