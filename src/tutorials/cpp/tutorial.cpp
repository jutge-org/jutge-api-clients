/**
 * This is a tutorial script that shows how to use the Jutge API client in C++.
 *
 * Full reference documentation is available at https://api.org
 */

// Include the Jutge API client header file
#include "jutge_api_client.cpp"

using namespace jutge_api_client;
using namespace std;

int main()
{
    // Get a fortune cookie
    cout << misc::get_fortune() << endl;

    // Get the current time in the server and print one of its attributes
    Time time = misc::get_time();
    cout << time.full_time << endl;
    cout << endl;

    // Get the homepage stats and print them
    auto stats = misc::get_homepage_stats();
    cout << "users: " << stats.users
         << ", problems: " << stats.problems
         << ", submissions: " << stats.submissions << endl;
    cout << endl;

    // Download the Jutge logo and save it to a file
    auto download = misc::get_logo();
    download.write("logo.png");

    // Get all compilers and print them if they are for C++
    auto compilers = tables::get_compilers();
    for (const auto& [compiler_id, compiler] : compilers) {
        if (compiler.language == "C++") {
            cout << compiler_id << ": '" << compiler.name << endl;
        }
    }
    cout << endl;

    // Get P68688 (Hello, world!) problem and print its title, author and English statement.
    auto problem = problems::get_problem("P68688_en");
    cout << problem.title << endl;
    cout << *(problem.abstract_problem.author) << endl;
    auto statement = problems::get_text_statement("P68688_en");
    cout << statement << endl;
    cout << endl;

    // All previous functions where public, but in order to access
    // other functions, we need to login using Jutge.org's credentials.

    string email = "...";
    string password = "...";
    login(email, password);
    cout << endl;

    // Get user's name and uid in the profile.
    auto profile = student::profile::get();
    cout << profile.name << endl;
    cout << profile.user_uid << endl;
    cout << endl;

    // All authenticated users are students and can use the student module.
    // There are other modules for different roles, such as admin, instructor, etc.

    // Get all problem statuses, filter those that are accepted and print the first 8 in alphabetical order.
    auto statuses = student::statuses::get_all();
    vector<string> accepteds;
    for (const auto& [problemNm, status] : statuses) {
        if (status.status == "accepted") {
            accepteds.push_back(problemNm);
        }
    }
    sort(accepteds.begin(), accepteds.end());
    for (int i = 0; i < min(size_t(8), accepteds.size()); i++) {
        cout << accepteds[i] << " ";
    }
    cout << endl
         << endl;

    // Get the status of problem P68688
    auto status = student::statuses::get_for_abstract_problem("P68688");
    cout << status.status << endl;
    cout << endl;

    // Logging out is not necessary, but it is advisable.
    logout();
    cout << endl;
}