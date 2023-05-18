<?php
  //// Show errors
  ini_set('display_errors', 1);
  ini_set('display_startup_errors', 1);
  error_reporting(E_ALL);
  
  //// Generic Input Sanitization (W3Schools)
  function sanitizeInput($data) {
    $data = trim($data);
    $data = stripslashes($data);
    $data = htmlspecialchars($data);
    return $data;
  }
  
  //// Sanitize Query Strings into new Array
  $validQuery = array();
  foreach ($_GET as $key => $value) {
    $saniKey = sanitizeInput($key);
    $saniValue = sanitizeInput($value);
    $validQuery[$saniKey] = $saniValue;
  }
  
  //// Validate the rest of the query keys based on Form ID
  if (isset($validQuery['formid'])) {
    switch ($validQuery['formid']) {
      // Validation for survey
      case 'survey':
        $allowedValues = array(
          'favoriteColor' => array('Red','Orange','Yellow','Green','Blue','Purple','Black'),
          'favoriteFruit' => array('Apple','Orange','Banana','Pear','Blueberry','Grape','Blackberry'),
          'favoriteSport' => array('Soccer','Basketball','Football','Badminton','Swimming','Pickleball')
        );
        foreach ($allowedValues as $key => $value) {
          // check if the key exists in the validQuery array
          if (isset($validQuery[$key])) {
            // check if the value from validQuery is in the nested array
            if (!in_array($validQuery[$key], $value)) {
              // if not, exit with an error message
              exit("Invalid value for $key!");
            }
          } else {
            // if the key is not found, exit with an error message
            exit("Missing required key: $key!");
          }
        }
        //echo "Keys and Values are valid!";
        break;
      case 'contact':
        exit("Under Contruction");
        break;
      default:
        exit("Invalid Form ID!");
    }
  }

  //// Update DB with Form Data
  function finishAction() {
    global $validQuery;
    
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
    
    // Do different things depending on the form ID
    switch ($validQuery['formid']) {
      // survey
      case 'survey':
        $sql = "INSERT INTO surveyResults VALUES ('{$validQuery['favoriteColor']}', '{$validQuery['favoriteSport']}', '{$validQuery['favoriteFruit']}', NOW())";
        if ($conn->query($sql) === TRUE) {
          echo "Thank you for participating in our survey!\n<br>\n";
          echo "Your response has been recorded.\n<br>\n";
          echo "View the results <a href=\"/results.php\">here</a>";
        } else {
          echo "Error: " . $sql . "<br>" . $conn->error;
        }
        break;
      case 'contact':
        exit("Under Contruction");
        break;
      default:
        exit("Invalid Form ID!");
    }

    // Close the connection
    $conn->close();
  }

  //// Show the captcha if its just a plain GET request.
  if ($_SERVER['REQUEST_METHOD'] == 'GET') {
    include $_SERVER['DOCUMENT_ROOT'] . '/_/captcha.php';
  }

  //// For POST requests: more validation and possibly update the db.
  if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    //echo "I have your survey inputs: " . sanitizeInput($_SERVER['QUERY_STRING']);
    //echo "<br>";
    //echo "I have your captcha inputs: " . sanitizeInput($_POST["captchaAnswer"]);
    //echo "<br>";

    $url = 'http://127.0.0.1:8080/validate';
 
    // Prepare the POST data
    $postData = array(
      'captchaAnswer' => sanitizeInput($_POST['captchaAnswer'])
    );
    
    // Retrieve the cookies from the user's browser ($_COOKIE)
    $cookies = array();
    foreach ($_COOKIE as $key => $value) {
      $cookies[] = $key . '=' . urlencode($value);
    }
    $cookieString = implode('; ', $cookies);
    
    // Initialize cURL
    $curlHandle = curl_init();
    
    // Set the cURL options
    curl_setopt($curlHandle, CURLOPT_URL, $url);
    curl_setopt($curlHandle, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($curlHandle, CURLOPT_FOLLOWLOCATION, 1);
    curl_setopt($curlHandle, CURLOPT_COOKIE, $cookieString);
    curl_setopt($curlHandle, CURLOPT_POST, 1);
    curl_setopt($curlHandle, CURLOPT_POSTFIELDS, http_build_query($postData));
    
    // Execute the cURL request
    $response = curl_exec($curlHandle);
    
    // Close the cURL handle
    curl_close($curlHandle);
    
    // Process the response as needed
    if ($response == "Correct!\n") {
      finishAction();
    } elseif ($response == "Wrong!\n")  {
      echo "Wrong. Try again!\n<br>";
      include $_SERVER['DOCUMENT_ROOT'] . '/_/captcha.php';
    } else {
      echo "Session/Body Error:\n<br>";
      echo "Your session is invalid.\n<br>";
      echo "Make sure you complete the CAPTCHA in time.\n<br>";
      echo "Try Again.\n<br>";
      include $_SERVER['DOCUMENT_ROOT'] . '/_/captcha.php';
    }
  }

  //// Resources and References
  // https://www.w3schools.com/php/php_superglobals_get.asp
  // https://www.w3schools.com/php/php_looping_for.asp
  // https://www.w3schools.com/php/php_switch.asp
  // https://www.w3schools.com/php/php_form_validation.asp
  // https://www.geeksforgeeks.org/php-curl/
?>
