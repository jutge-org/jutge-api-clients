package com.jutge.api;

// PREAMBLE_HERE

/*
 * GSON library is used to convert JSON strings into Java objects and vice versa.
 * Get the .jar file at htmv tps://mvnrepository.com/artifact/com.google.code.gson/gson/2.12.1
 *
 * Compile and execute with the following commands:
 *
 * javac -cp gson-2.12.1.jar:. YourProgram.java
 * java -cp gson-2.12.1.jar:. YourProgram
 *
 * If you want to use Maven, go ahead, it's your life.
 *
 * In VSCode, you can add the .jar file to your project modifying settings.json with:
 *
 * vscode sttings.json: "java.project.referencedLibraries": ["gson-2.12.1.jar"]
 *
 * Warnings:
 * - The use of nulls is not taken into account.
 * - Testing of this Java client is sparse.
 */

import java.io.*;
import java.util.*;
import java.net.URI;
import java.net.URL;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.net.HttpURLConnection;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.reflect.TypeToken;

@SuppressWarnings("unused")

/**
 *
 * JutgeApiClient
 *
 */

public class JutgeApiClient {

    public String JUTGE_API_URL = "https://api.jutge.org/api";

    // Models for Jutge API

    // MODELS_HERE

    // Client types

    private static class Error {
        public String name;
        public String message;
        public String operation_id;
    }

    private static class OutputMessage {
        public String operation_id;
        public String time;
        public String duration;
        public Error error;

        public String toString() {
            return "OutputMessage(" + operation_id + ")";
        }
    }

    public static class Tuple<X, Y> {
        public final X x;
        public final Y y;

        public Tuple(X x, Y y) {
            this.x = x;
            this.y = y;
        }
    }

    public static class Download {
        public byte[] data;
        public String name;
        public String type;

        public void write(String path) throws IOException {
            FileOutputStream fos = new FileOutputStream(path);
            fos.write(data);
            fos.close();
        }
    }

    private static class Execution {
        public JsonElement output;
        public Download[] ofiles;
    }

    public static class Meta {
        public String token;

        public Meta(String token) {
            this.token = token;
        }
    }

    public Meta meta = null;

    /**
     * A client for executing multipart/form-data HTTP requests with binary file
     * handling
     */
    private static class MultipartClient {

        // Most of this class written by claude.ai, under the direction of jpetit.

        public Execution execute(String url, String func, JsonElement ijson, byte[][] ifiles, Meta meta)
                throws Exception {
            String boundary = UUID.randomUUID().toString();
            HttpURLConnection connection = setupConnection(url, boundary);

            try (OutputStream outputStream = connection.getOutputStream()) {
                // Write the data part
                JsonObject inputObject = new JsonObject();
                inputObject.addProperty("func", func);
                if (meta != null) {
                    inputObject.add("meta", new Gson().toJsonTree(meta).getAsJsonObject());
                }
                inputObject.add("input", ijson);
                String data = inputObject.toString();
                writeDataPart(outputStream, boundary, "data", data);

                // Write all input file parts
                for (int i = 0; i < ifiles.length; i++) {
                    writeFilePart(outputStream, boundary, "file_" + i, ifiles[i]);
                }

                // Write the final boundary
                writeFinalBoundary(outputStream, boundary);

                // Check response code
                int responseCode = connection.getResponseCode();
                if (responseCode != HttpURLConnection.HTTP_OK) {
                    throw new Exception("HTTP error code: " + responseCode);
                }

                // Parse the multipart response
                return parseMultipartResponse(connection);
            }
        }

        private HttpURLConnection setupConnection(String url, String boundary) throws Exception {
            URI uri = new URI(url);
            URL urlObj = uri.toURL();
            HttpURLConnection connection = (HttpURLConnection) urlObj.openConnection();
            connection.setDoOutput(true);
            connection.setRequestMethod("POST");
            connection.setRequestProperty("Content-Type", "multipart/form-data; boundary=" + boundary);
            connection.setRequestProperty("Connection", "Keep-Alive");
            return connection;
        }

        private void writeDataPart(OutputStream outputStream, String boundary, String name, String value)
                throws Exception {
            String header = "--" + boundary + "\r\n" +
                    "Content-Disposition: form-data; name=\"" + name + "\"\r\n\r\n";
            outputStream.write(header.getBytes());
            outputStream.write(value.getBytes());
            outputStream.write("\r\n".getBytes());
        }

        private void writeFilePart(OutputStream outputStream, String boundary, String name, byte[] fileData)
                throws Exception {
            String header = "--" + boundary + "\r\n" +
                    "Content-Disposition: form-data; name=\"" + name + "\"; filename=\"" + name + "\"\r\n" +
                    "Content-Type: application/octet-stream\r\n\r\n";
            outputStream.write(header.getBytes());
            outputStream.write(fileData);
            outputStream.write("\r\n".getBytes());
        }

        private void writeFinalBoundary(OutputStream outputStream, String boundary) throws Exception {
            outputStream.write(("--" + boundary + "--\r\n").getBytes());
        }

        private Execution parseMultipartResponse(HttpURLConnection connection) throws Exception {
            String contentType = connection.getContentType();
            if (contentType == null || !contentType.startsWith("multipart/form-data")) {
                throw new Exception("Response is not multipart/form-data: " + contentType);
            }

            // Extract boundary from content type
            String boundary = extractBoundary(contentType);
            InputStream inputStream = connection.getInputStream();
            byte[] responseBytes = readAllBytes(inputStream);

            Execution result = new Execution();
            ArrayList<Download> downloads = new ArrayList<>();

            // Convert boundary to bytes for binary searching
            byte[] boundaryBytes = ("--" + boundary).getBytes();
            byte[] finalBoundaryBytes = ("--" + boundary + "--").getBytes();

            // Find all boundary positions
            ArrayList<Integer> boundaryPositions = findAllBoundaries(responseBytes, boundaryBytes, finalBoundaryBytes);

            if (boundaryPositions.size() < 2) {
                throw new Exception("Could not find enough boundaries in response");
            }

            // Process each part
            for (int i = 0; i < boundaryPositions.size() - 1; i++) {
                int start = boundaryPositions.get(i);
                int end = boundaryPositions.get(i + 1);

                // Extract part content between boundaries
                byte[] partBytes = new byte[end - start];
                System.arraycopy(responseBytes, start, partBytes, 0, partBytes.length);

                // Find the end of headers (double CRLF)
                int headerEnd = findHeaderEnd(partBytes);
                if (headerEnd == -1) {
                    continue; // Skip malformed part
                }

                // Extract headers as string
                String headers = new String(partBytes, 0, headerEnd);

                // Extract content after headers
                byte[] contentBytes = new byte[partBytes.length - headerEnd];
                System.arraycopy(partBytes, headerEnd, contentBytes, 0, contentBytes.length);

                // Strip final CRLF that precedes the next boundary
                contentBytes = stripTrailingCRLF(contentBytes);

                if (i == 0) {
                    // First part is the output string
                    String data = new String(contentBytes);
                    JsonObject object = new Gson().fromJson(data, JsonObject.class);
                    result.output = object.get("output");
                } else {
                    // Subsequent parts are binary files
                    Download download = new Download();
                    download.data = contentBytes;

                    // Extract name and type from headers
                    String contentDisposition = extractHeader(headers, "Content-Disposition");
                    String contentTypeHeader = extractHeader(headers, "Content-Type");

                    if (contentDisposition != null) {
                        String filename = extractFilenameFromContentDisposition(contentDisposition);
                        download.name = filename != null ? filename : "file_" + (i - 1);
                    } else {
                        download.name = "file_" + (i - 1);
                    }

                    download.type = contentTypeHeader != null ? contentTypeHeader : "application/octet-stream";

                    downloads.add(download);
                }
            }

            result.ofiles = downloads.toArray(new Download[0]);
            return result;
        }

        private String extractHeader(String headers, String headerName) {
            for (String line : headers.split("\r\n")) {
                if (line.startsWith(headerName + ":")) {
                    return line.substring(headerName.length() + 1).trim();
                }
            }
            return null;
        }

        private String extractFilenameFromContentDisposition(String contentDisposition) {
            String[] parts = contentDisposition.split(";");
            for (String part : parts) {
                part = part.trim();
                if (part.startsWith("filename=")) {
                    String filename = part.substring("filename=".length());
                    // Remove quotes if present
                    if (filename.startsWith("\"") && filename.endsWith("\"")) {
                        filename = filename.substring(1, filename.length() - 1);
                    }
                    return filename;
                }
            }
            return null;
        }

        private byte[] stripTrailingCRLF(byte[] data) {
            if (data.length >= 2 && data[data.length - 2] == '\r' && data[data.length - 1] == '\n') {
                byte[] result = new byte[data.length - 2];
                System.arraycopy(data, 0, result, 0, data.length - 2);
                return result;
            }
            return data;
        }

        private int findHeaderEnd(byte[] partBytes) {
            // Look for double CRLF which separates headers from content
            for (int i = 0; i < partBytes.length - 3; i++) {
                if (partBytes[i] == '\r' && partBytes[i + 1] == '\n' &&
                        partBytes[i + 2] == '\r' && partBytes[i + 3] == '\n') {
                    return i + 4;
                }
            }
            return -1;
        }

        private ArrayList<Integer> findAllBoundaries(byte[] data, byte[] boundaryBytes, byte[] finalBoundaryBytes) {
            ArrayList<Integer> positions = new ArrayList<>();

            // Find all regular boundaries
            int pos = indexOf(data, boundaryBytes, 0);
            while (pos != -1) {
                positions.add(pos);
                pos = indexOf(data, boundaryBytes, pos + boundaryBytes.length);
            }

            // Find final boundary if it exists
            pos = indexOf(data, finalBoundaryBytes, 0);
            if (pos != -1) {
                positions.add(pos);
            }

            return positions;
        }

        private int indexOf(byte[] data, byte[] pattern, int start) {
            for (int i = start; i <= data.length - pattern.length; i++) {
                boolean found = true;
                for (int j = 0; j < pattern.length; j++) {
                    if (data[i + j] != pattern[j]) {
                        found = false;
                        break;
                    }
                }
                if (found) {
                    return i;
                }
            }
            return -1;
        }

        private byte[] readAllBytes(InputStream inputStream) throws Exception {
            ByteArrayOutputStream buffer = new ByteArrayOutputStream();
            int bytesRead;
            byte[] data = new byte[4096];

            while ((bytesRead = inputStream.read(data, 0, data.length)) != -1) {
                buffer.write(data, 0, bytesRead);
            }

            return buffer.toByteArray();
        }

        private String extractBoundary(String contentType) {
            String[] parts = contentType.split(";");
            for (String part : parts) {
                part = part.trim();
                if (part.startsWith("boundary=")) {
                    String boundary = part.substring("boundary=".length()).trim();
                    // Remove quotes if present
                    if (boundary.startsWith("\"") && boundary.endsWith("\"")) {
                        boundary = boundary.substring(1, boundary.length() - 1);
                    }
                    return boundary;
                }
            }
            throw new IllegalArgumentException("Boundary not found in Content-Type: " + contentType);
        }
    }

    public Execution execute(String func, JsonElement ijson, byte[][] ifiles) throws Exception {
        var client = new MultipartClient();
        return client.execute(JUTGE_API_URL, func, ijson, ifiles, meta);
    }

    public void login(String email, String password) throws Exception {
        var credentialsIn = new CredentialsIn();
        credentialsIn.email = email;
        credentialsIn.password = password;
        var credentialsOut = auth.login(credentialsIn);
        if (credentialsOut.token.equals("")) {
            System.err.println(credentialsOut.error);
            System.exit(1);
        }
        meta = new Meta(credentialsOut.token);
    }

    public void logout() throws Exception {
        auth.logout();
        meta = null;
    }

    // MAIN_MODULE_HERE

    // MODULES_HERE
}
