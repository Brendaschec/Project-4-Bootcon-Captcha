<div id="output"></div>
<div id="colorsChart"></div>
<div id="sportsChart"></div>
<script src='https://cdn.plot.ly/plotly-2.20.0.min.js'></script>
<script>
  const favoriteForm = document.getElementById("favoriteForm");
  const favoriteColor = document.getElementById("favoriteColor");
  const favoriteSport = document.getElementById("favoriteSport");
  const capchaSolution = document.getElementById("capchaSolution");
  const output = document.getElementById("output");
  const colorsChart = document.getElementById("colorsChart");
  const sportsChart = document.getElementById("sportsChart");
  
  favoriteForm.addEventListener("submit", handleSubmit);
  async function handleSubmit(e) {
    e.preventDefault();
    const favoriteColorValue = favoriteColor.value;
    const favoriteSportValue = favoriteSport.value;
    const capchaSolutionValue = capchaSolution.value;
    const data = await sendRequest(favoriteColorValue, favoriteSportValue, capchaSolutionValue)
    if (!data.success) {
      output.textContent = "Wrong capcha!";
      return;
    }
    buildGraph(data);
  }
  async function sendRequest(favoriteColorValue, favoriteSportValue, capchaSolutionValue) {
    // const response = await fetch("/apps/captcha/favorites", {
    //   method: "POST",
    //   body: `captchaAnswer=${capchaSolutionValue}&color=${favoriteColorValue}&sport=${favoriteSportValue}`,
    //   headers: {
    //     "Content-Type": "application/x-www-form-urlencoded"
    //   }
    // })
    // const responseData = await response.json();
    // return responseData;
    // return {
    //   success: false,
    // }
    return {
      success: true,
      colors: [{
          name: "Blue",
          count: 4
        },
        {
          name: "Red",
          count: 1
        },
        {
          name: "Yellow",
          count: 7
        },
        {
          name: "Green",
          count: 5
        },
        {
          name: "Orange",
          count: 4
        },
        {
          name: "Purple",
          count: 2
        },
      ],
      sports: [{
          name: "Soccer",
          count: 2
        },
        {
          name: "Basketball",
          count: 3
        },
        {
          name: "Football",
          count: 4
        },
        {
          name: "Badminton",
          count: 1
        },
        {
          name: "Swimming",
          count: 6
        },
        {
          name: "Pickleball",
          count: 3
        },
      ]
    }
  }

  function buildGraph(data) {
    const colors = data.colors;
    const sports = data.sports;
    
    var colorData = [{
      x: colors.map(function(color) {
        return color.name;
      }),
      y: colors.map(function(color) {
        return color.count;
      }),
      name: "Colors",
      type: 'bar'
    }];
    Plotly.newPlot('colorsChart', colorData);
    
    var sportData = [{
      x: sports.map(function(sport) {
        return sport.name;
      }),
      y: sports.map(function(sport) {
        return sport.count;
      }),
      name: "Sports",
      type: 'bar'
    }]
    Plotly.newPlot("sportsChart", sportData);
  }
</script>
