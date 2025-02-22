<?php

namespace client;


$meta = null;


function execute($func, $input)
{
    global $meta;

    $info = array(
        'func' => $func,
        'input' => $input,
        'meta' => $meta,
    );

    $data = array(
        'data' => json_encode($info),
    );

    $url = 'https://api.jutge.org/api';

    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

    $response = curl_exec($ch);

    $lines = explode("\n", $response);
    $intersting = $lines[3];
    $answer = json_decode($intersting, true);

    curl_close($ch);

    if (array_key_exists('output', $answer)) {
        return $answer["output"];
    } else {
        throw new \Exception($answer["error"]["name"]);
    }
}



function login()
{
    $path = getenv('HOME') . '/.jutge-client.yml';
    if (!file_exists($path)) {
        echo 'The file ~/.jutge-client.yml does not exist';
        exit();
    }
    $file = file_get_contents($path);
    list($line1, $line2) = explode("\n", $file, 2);
    list($email_text, $email) = explode(': ', trim($line1), 2);
    list($password_text, $password) = explode(': ', trim($line2), 2);
    $credentials = execute('auth.login', array('email' => $email, 'password' => $password));
    global $meta;
    $meta = array(
        'token' => $credentials['token'],
        'exam' => null,
    );
}

function logout()
{
    global $meta;
    $meta = array('token' => null, 'exam' => null);
}
