<?php

// Include the client
require_once "jutge_api_client.php";

// Get a fortune cookie
$fortune = jutge\misc\get_fortune();
print($fortune);
print(PHP_EOL);

// Get the server time and print it
$time = jutge\misc\get_time();
print_r($time);
print(PHP_EOL);
