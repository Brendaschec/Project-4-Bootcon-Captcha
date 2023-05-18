<?php
  // idea: Sanitize browser cookies and user agent
  $userAgent = $_SERVER['HTTP_USER_AGENT'];
  $isIOS = (preg_match('/iPad|iPhone|iPod/', $userAgent));

  // URL of the backend server
  if($isIOS) {
    $url = 'http://127.0.0.1:8080/new_audio/1.mp3';
  } else {
    $url = 'http://127.0.0.1:8080/new_audio/1.wav';
  }

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
  curl_setopt($curlHandle, CURLOPT_COOKIE, $cookieString);
  curl_setopt($curlHandle, CURLOPT_HEADER, 1);
  
  // Execute the cURL request to fetch the challenge image
  $response = curl_exec($curlHandle);
  
  // Get the header size
  $headerSize = curl_getinfo($curlHandle, CURLINFO_HEADER_SIZE);
  
  // Separate the response header and body
  $header = substr($response, 0, $headerSize);
  $body = substr($response, $headerSize);
  $headers = explode("\r\n", $header);
  foreach ($headers as $hdr) {
    // Forward curl headers
    header($hdr);
  }

  // Close the cURL handle
  curl_close($curlHandle);
  
  // Echo the response
  echo $body;
?>
