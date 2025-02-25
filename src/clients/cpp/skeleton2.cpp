
void login(string email, string password)
{
    const CredentialsIn credentials_in = { email, password };
    try {
        const CredentialsOut credentials_out = auth::login(credentials_in);
        meta = Meta { credentials_out.token };
    } catch (const exception& e) {
        cout << "login failed" << endl;
        exit(1);
    }
}

void logout()
{
    auth::logout();
    meta = nullopt;
}
