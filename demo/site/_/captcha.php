<!DOCTYPE html>
<html>
<?php include $_SERVER['DOCUMENT_ROOT'] . '/head.html';?>
<body>
<h1><i>Are you a robot?</i></h1>
<p>Complete the verification challenge!</p>
<p>
  &nbsp;- Your session is valid for one minute at a time.
  <br>
  &nbsp;- Input only capital letters and digits.
</p>
<hr>
<form method="post" action="<?php echo htmlspecialchars($_SERVER['PHP_SELF'] . '?' . $_SERVER['QUERY_STRING']);?>">
<br><br>
<?php
  // URL of the backend server
  $url = 'http://127.0.0.1:8080/new_image';
  
  // Initialize cURL
  $curlHandle = curl_init();
  
  // Set the cURL options
  curl_setopt($curlHandle, CURLOPT_URL, $url);
  curl_setopt($curlHandle, CURLOPT_RETURNTRANSFER, 1);
  curl_setopt($curlHandle, CURLOPT_HEADER, 1);
  
  // Execute the cURL request to fetch the challenge image
  $response = curl_exec($curlHandle);
  
  // Get the header size
  $headerSize = curl_getinfo($curlHandle, CURLINFO_HEADER_SIZE);
  
  // Separate the response header and body
  $header = substr($response, 0, $headerSize);
  $body = substr($response, $headerSize);
  
  // Close the cURL handle
  curl_close($curlHandle);
  
  // Process the headers
  $headers = explode("\r\n", $header);
  foreach ($headers as $hdr) {
    // Find curl header with set-cookie + cookie value
    if (stripos($hdr, 'Set-Cookie:') !== false) {
      // Forward the cookie to the end user
      header($hdr, false);
    }
  }
  
  // Convert the PNG image to base64
  $base64Image = base64_encode($body);
  
  // Echo the base64 encoded image as an inline data blob
  echo '<img src="data:image/png;base64,' . $base64Image . '" />' . "\n";
  
  // Resources and References
  // https://www.geeksforgeeks.org/php-curl/
  // https://stackoverflow.com/questions/47854286/showing-an-image-with-curl
  // https://www.w3schools.com/php/php_form_validation.asp
?>
<br><br>
<label>Type the text you recognize:</label>
<br><br>
<input autocomplete="false" type="text" style="text-transform: uppercase;" name="captchaAnswer">
<input type="submit" value="Submit">
</form>
<br>
<div id="audioDiv">
  <a href="javascript:void(0);" onclick="playAudio();" id="requestAudio">Request Audio-Based Challenge</a>
</div>
<script>
  // Different server-side design compared to basic.html
  const audioDiv = document.getElementById("audioDiv");
  
  // Firefox agressively caches the audio even when the document reloads
  // We load a random URL suffix to trick it into not caching
  const randCacheWorkaround = Math.floor(Math.random() * 100);

  function playAudio() {
    audioDiv.innerHTML = `<audio controls="controls" ><source src="/apps/captcha/audio.php?nocache=${randCacheWorkaround}"></audio>`
  }
</script>
<br><hr>
</body>
</html>
