// We use Catch2 (https://github.com/catchorg/Catch2) for C++ unit tests.

#include "catch_amalgamated.hpp"
#include "jutge_api_client.cpp"
#include <iostream>

using namespace jutge_api_client;
using namespace std;

TEST_CASE("misc.get_time", "[misc]")
{
    Time time = misc::get_time();
    REQUIRE(time.int_timestamp >= 1740000000);
    REQUIRE(time.int_timestamp <= 2000000000);
}

TEST_CASE("misc.get_fortune", "[misc]")
{
    string fortune = misc::get_fortune();
    REQUIRE(fortune.size() > 0);
}