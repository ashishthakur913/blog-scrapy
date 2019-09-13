<?php

$strJsonFileContents = file_get_contents("quotes.json");
$array = json_decode($strJsonFileContents, true);

$decoded_json = json_encode($array, JSON_UNESCAPED_UNICODE);
$fp = fopen('final_translated.json', 'w');
fwrite($fp, $decoded_json);
fclose($fp);