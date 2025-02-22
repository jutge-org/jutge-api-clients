// Quick login function that reads the credentials from ~/.jutge-client.json
// and stores the token in the global variable meta.
// TODO: We could improve this function to mimin the Python one.

void login()
{
    string home = getenv("HOME");
    const string path = home + "/.jutge-client.json";
    ifstream ifs(path);
    json j;
    ifs >> j;
    ifs.close();

    const CredentialsIn credentials_in = j;
    try {
        const CredentialsOut credentials_out = auth::login(credentials_in);
        meta = Meta { credentials_out.token };
    } catch (const exception& e) {
        cout << "login failed" << endl;
        exit(1);
    }
}
