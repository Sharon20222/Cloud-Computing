val lines = sc.textFile("hdfs:///pagerank/links.txt")
val links = lines.map{ s =>
      val parts = s.split("\\s+")
      (parts(0), parts(1))
    }.distinct().groupByKey().cache()
var ranks = links.mapValues(v => 1.0)
for (i <- 1 to 2) {
  val contribs = links.join(ranks).values.flatMap{ case (urls, rank) =>
    val size = urls.size
    urls.map(url => (url, rank / size))
  }
  ranks = contribs.reduceByKey(_ + _).mapValues(0.15 + 0.85 * _)
  println("Iteration --> " + i)
  val output = ranks.collect()
  output.foreach(tup => println(s"${tup._1} has rank:  ${tup._2} ."))
}
