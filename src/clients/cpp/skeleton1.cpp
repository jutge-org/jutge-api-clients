// ensure https is available
#define CPPHTTPLIB_OPENSSL_SUPPORT

// includes
#include "httplib.h"
#include <fstream>
#include <map>
#include <nlohmann/json.hpp>
#include <optional>
#include <sstream>
#include <stdexcept>
#include <string>
#include <tuple>
#include <variant>
#include <vector>

// extend JSON library to support std::variant and std::optional
// see https://github.com/nlohmann/json?tab=readme-ov-file#how-do-i-convert-third-party-types
// and https://www.kdab.com/jsonify-with-nlohmann-json/

namespace nlohmann {
template <typename T, typename... Ts>
void variant_from_json(const nlohmann::json& j, std::variant<Ts...>& data)
{
    try {
        data = j.get<T>();
    } catch (...) {
    }
}

template <typename... Ts>
struct adl_serializer<std::variant<Ts...>> {
    static void to_json(nlohmann::json& j, const std::variant<Ts...>& data)
    {
        std::visit([&j](const auto& v) { j = v; }, data);
    }

    static void from_json(const nlohmann::json& j, std::variant<Ts...>& data)
    {
        (variant_from_json<Ts>(j, data), ...);
    }
};

template <typename T>
struct adl_serializer<std::optional<T>> {
    static void to_json(json& j, const std::optional<T>& opt)
    {
        if (opt == std::nullopt) {
            j = nullptr;
        } else {
            j = *opt;
        }
    }

    static void from_json(const json& j, std::optional<T>& opt)
    {
        if (j.is_null()) {
            opt = std::nullopt;
        } else {
            opt = j.template get<T>();
        }
    }
};
}

namespace jutge_api_client {

using namespace std;
using json = nlohmann::json;

string JUTGE_API_SERVER = "https://api.jutge.org";

struct Meta {
    string token;
};

NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(Meta, token)

optional<Meta> meta = nullopt;

class UnauthorizedError : public runtime_error {
public:
    UnauthorizedError(const string& msg)
        : runtime_error(msg)
    {
    }
};

class InfoError : public runtime_error {
public:
    InfoError(const string& msg)
        : runtime_error(msg)
    {
    }
};

class NotFoundError : public runtime_error {
public:
    NotFoundError(const string& msg)
        : runtime_error(msg)
    {
    }
};

class InputError : public runtime_error {
public:
    InputError(const string& msg)
        : runtime_error(msg)
    {
    }
};

class ProcessingError : public runtime_error {
public:
    ProcessingError(const string& msg)
        : runtime_error(msg)
    {
    }
};

void throwError(const map<string, string>& error, const string& operation_id)
{
    // TODO: do something with operation_id
    string message = "Unknown error";
    auto it = error.find("message");
    if (it != error.end())
        message = it->second;

    if (error.at("name") == "UnauthorizedError") {
        throw UnauthorizedError(message);
    }
    if (error.at("name") == "InfoError") {
        throw InfoError(message);
    }
    if (error.at("name") == "NotFoundError") {
        throw NotFoundError(message);
    }
    if (error.at("name") == "InputError") {
        throw InputError(message);
    }
    throw std::runtime_error("Unknown error");
}

using Headers = map<string, string>;

struct Range {
    size_t start;
    size_t end;
};

struct Part {
    int id;
    Headers headers;
    string content;

    bool is_file()
    {
        const auto it = headers.find("Content-Disposition");
        return it != headers.end() && it->second.find(" filename=") != string::npos;
    }

    string get_filename()
    {
        const string& content_disposition = headers["Content-Disposition"];
        size_t pos1 = content_disposition.find(" filename");
        size_t pos2 = content_disposition.find("\"", pos1 + 1);
        size_t pos3 = content_disposition.find("\"", pos2 + 1);
        return content_disposition.substr(pos2 + 1, pos3 - pos2 - 1);
    }

    string get_name()
    {
        const string& content_disposition = headers["Content-Disposition"];
        size_t pos1 = content_disposition.find(" name");
        size_t pos2 = content_disposition.find("\"", pos1 + 1);
        size_t pos3 = content_disposition.find("\"", pos2 + 1);
        return content_disposition.substr(pos2 + 1, pos3 - pos2 - 1);
    }

    string get_content_type()
    {
        return headers["Content-Type"];
    }

    json get_json()
    {
        return json::parse(content);
    }
};

Headers get_headers(const string& body)
{
    Headers headers;
    size_t pos1 = 0;
    while (true) {
        size_t pos2 = body.find("\r\n", pos1);
        if (pos2 - pos1 == 0)
            break;
        string line = body.substr(pos1, pos2 - pos1);
        size_t pos = line.find(":");
        string key = line.substr(0, pos);
        string value = line.substr(pos + 2);
        headers[key] = value;
        pos1 = pos2 + 2;
    }
    return headers;
}

string get_boundary(const string& contentType)
{
    size_t pos1 = contentType.find("boundary=\"");
    size_t pos2 = contentType.find("\"", pos1 + 1);
    size_t pos3 = contentType.find("\"", pos2 + 1);
    return "--" + contentType.substr(pos2 + 1, pos3 - pos2 - 1);
}

vector<Part> get_parts(const httplib::Result& result)
{
    vector<Range> ranges;

    const auto it = result->headers.find("Content-Type");
    if (it == result->headers.end())
        return {};
    const string& boundary = get_boundary(it->second);

    const string& content = result->body;
    size_t pos = 0;
    while (true) {
        pos = content.find(boundary, pos);
        if (pos == string::npos)
            break;
        pos += boundary.size() + 2;
        size_t pos2 = content.find(boundary, pos);
        if (pos2 == string::npos)
            break;
        ranges.push_back({ pos, pos2 });
        pos = pos2;
    }

    vector<Part> parts;
    for (Range range : ranges) {
        Part part;
        part.id = parts.size() + 1;
        const string body = content.substr(range.start, range.end - range.start);
        part.headers = get_headers(body);
        size_t pos = body.find("\r\n\r\n");
        part.content = body.substr(pos + 4, body.size() - pos - 4 - 2);
        parts.push_back(part);
    }
    return parts;
}

using Blob = string;

using Files = vector<Blob>;

struct Download {
    Blob content;
    string name;
    string type;
};

using Downloads = vector<Download>;

tuple<json, Downloads> execute(const string& func, const json& ijson, const Files& ifiles)
{
    using namespace std;
    httplib::Client client(JUTGE_API_SERVER);

    json idata = {
        { "func", func },
        { "input", ijson },
    };
    if (meta)
        idata["meta"] = *meta;

    httplib::MultipartFormDataItems datas = {
        { "data", idata.dump(), "", "" },
        //{"file2", "{\n  \"world\", true\n}\n", "world.json", "application/json"},
    };
    for (int i = 0; i < ifiles.size(); ++i) {
        const string name = "file_" + to_string(i);
        datas.push_back({ name, ifiles[i], name, "" });
    }

    const auto result = client.Post("/api", datas);

    vector<Download> ofiles;
    json answer;

    vector<Part> parts = get_parts(result);
    for (Part part : parts) {
        if (part.is_file()) {
            const Download download = {
                part.content,
                part.get_filename(),
                part.get_content_type(),
            };
            ofiles.push_back(download);
        } else {
            answer = part.get_json();
        }
    }

    if (answer.contains("error")) {
        throwError(answer["error"], answer["operation_id"]);
    }
    return { answer["output"], ofiles };
}
}
