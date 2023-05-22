<!DOCTYPE html>
<html>
<?php include $_SERVER['DOCUMENT_ROOT'] . '/head.html';?>
<body>
<div style="float: right;"><a href="/" class="bannerBox3">Go Home</a></div>
<h1><i>Survey Results</i></h1>
<p>Enjoy the pretty visuals!</p>
<hr><br>
<h2>Color Chart</h2>
<div id="colorsChart" class="graphBox"></div>
<h2>Sports Chart</h2>
<div id="sportsChart" class="graphBox"></div>
<h2>Fruits Chart</h2>
<div id="fruitsChart" class="graphBox"></div>
<script src="https://cdn.plot.ly/plotly-2.20.0.min.js"></script>
<script>
  const colorsChart = document.getElementById("colorsChart");
  const sportsChart = document.getElementById("sportsChart");
  const fruitsChart = document.getElementById("fruitsChart");

  <?php
    // Connection parameters
    $servername = 'localhost';
    $username = 'root';
    $password = 'testpass100';
    $dbname = 'captchaDemo';
    
    // Create connection
    $conn = new mysqli($servername, $username, $password, $dbname);
    
    // Check connection
    if ($conn->connect_error) {
      die("Connection failed: " . $conn->connect_error);
    }
    
    $sql = "SELECT favoriteColor, COUNT(*) as count FROM surveyResults GROUP BY favoriteColor";
    $result = $conn->query($sql);

    $colors = array();
    if ($result->num_rows > 0) {
      while($row = $result->fetch_assoc()) {
        array_push($colors, ["name" => $row["favoriteColor"], "count" => $row["count"]]);
      }
    } 

    echo 'const colors = ' . json_encode($colors) . ';' . "\n  ";
    
    $sql = "SELECT favoriteSport, COUNT(*) as count FROM surveyResults GROUP BY favoriteSport";
    $result = $conn->query($sql);

    $sports = array();
    if ($result->num_rows > 0) {
      while($row = $result->fetch_assoc()) {
        array_push($sports, ["name" => $row["favoriteSport"], "count" => $row["count"]]);
      }
    } 

    echo 'const sports = ' . json_encode($sports) . ';' . "\n  ";
    
    $sql = "SELECT favoriteFruit, COUNT(*) as count FROM surveyResults GROUP BY favoriteFruit";
    $result = $conn->query($sql);

    $fruits = array();
    if ($result->num_rows > 0) {
      while($row = $result->fetch_assoc()) {
        array_push($fruits, ["name" => $row["favoriteFruit"], "count" => $row["count"]]);
      }
    } 

    echo 'const fruits = ' . json_encode($fruits) . ';' . "\n";
    
    // Close connection
    $conn->close();
  ?>

  function buildGraph() {
    var opts = {displayModeBar: false, responsive: true, staticPlot: true};
    var layout = {
      font: {
        family: 'sans-serif',
        size: 18,
        color: '#000'
      }
    };
    var colorData = [{
      x: colors.map(function(color) {
        return color.name;
      }),
      y: colors.map(function(color) {
        return color.count;
      }),
      name: "Colors",
      type: 'bar',
      marker: {
        color: 'navy',
      }
    }];
    Plotly.newPlot('colorsChart', colorData, layout, opts);
    
    var sportData = [{
      x: sports.map(function(sport) {
        return sport.name;
      }),
      y: sports.map(function(sport) {
        return sport.count;
      }),
      name: "Sports",
      type: 'bar',
      marker: {
        color: 'navy',
      }
    }]
    Plotly.newPlot("sportsChart", sportData, layout, opts);
    
    var fruitData = [{
      x: fruits.map(function(fruit) {
        return fruit.name;
      }),
      y: fruits.map(function(fruit) {
        return fruit.count;
      }),
      name: "Fruits",
      type: 'bar',
      marker: {
        color: 'navy',
      }
    }]
    Plotly.newPlot("fruitsChart", fruitData, layout, opts);
  }
  
  buildGraph();
  // https://plotly.com/javascript/font/
</script>
<br><hr>
</body>
</html>
