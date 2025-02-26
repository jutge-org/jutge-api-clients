<?php

declare(strict_types=1);

use PHPUnit\Framework\TestCase;

require_once "jutge_api_client.php";

final class MiscTest extends TestCase
{
    public function test_get_time(): void
    {
        $time = jutge\misc\get_time();

        $this->assertTrue($time['int_timestamp'] >= 1740000000);
        $this->assertTrue($time['int_timestamp'] <= 2000000000);
    }

    public function test_fortune(): void
    {
        $fortune = jutge\misc\get_fortune();

        $this->assertTrue(strlen($fortune) > 0);
    }
}
