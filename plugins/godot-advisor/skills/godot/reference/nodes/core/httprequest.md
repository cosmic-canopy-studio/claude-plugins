---
class: HTTPRequest
inherits: Node > Object
brief: A node with the ability to send HTTP(S) requests.
---

# HTTPRequest

A node with the ability to send HTTP(S) requests.

## Description

A node with the ability to send HTTP requests. Uses HTTPClient internally.

Can be used to make HTTP requests, i.e. download or upload files or web content via HTTP.

**Warning:** See the notes and warnings on HTTPClient for limitations, especially regarding TLS security.

**Note:** When exporting to Android, make sure to enable the INTERNET permission in the Android export preset before exporting the project or using one-click deploy. Otherwise, network communication of any kind will be blocked by Android.

**Note:** HTTPRequest nodes will automatically handle decompression of response bodies. An Accept-Encoding header will be automatically added to each of your requests, unless one is already specified. Any response with a Content-Encoding: gzip header will automatically be decompressed and delivered to you as uncompressed bytes.

## Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| accept_gzip | bool | true | If true, this header will be added to each request: Accept-Encoding: gzip, deflate. Response bodies will be automatically decompressed. |
| body_size_limit | int | -1 | Maximum allowed size for response bodies. If the response body is compressed, this will be used as the maximum allowed size for the decompressed body. |
| download_chunk_size | int | 65536 | The size of the buffer used and maximum bytes to read per iteration. Set this to a lower value (e.g. 4096) when downloading small files to decrease memory usage at the cost of download speeds. |
| download_file | String | "" | The file to download into. Will output any received file into it. |
| max_redirects | int | 8 | Maximum number of allowed redirects. |
| timeout | float | 0.0 | The duration to wait in seconds before a request times out. If timeout is set to 0.0 then the request will never time out. |
| use_threads | bool | false | If true, multithreading is used to improve performance. |

## Methods

| Returns | Method |
|---------|--------|
| void | cancel_request() |
| int | get_body_size() const |
| int | get_downloaded_bytes() const |
| Status | get_http_client_status() const |
| Error | request(url: String, custom_headers: PackedStringArray = [], method: Method = 0, request_data: String = "") |
| Error | request_raw(url: String, custom_headers: PackedStringArray = [], method: Method = 0, request_data_raw: PackedByteArray = []) |
| void | set_http_proxy(host: String, port: int) |
| void | set_https_proxy(host: String, port: int) |
| void | set_tls_options(client_options: TLSOptions) |

## Signals

**request_completed**(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray)

Emitted when a request is completed.

## Enumerations

**enum Result:**

- **RESULT_SUCCESS** = 0 - Request successful
- **RESULT_CHUNKED_BODY_SIZE_MISMATCH** = 1 - Request failed due to a mismatch between expected and actual chunked body size
- **RESULT_CANT_CONNECT** = 2 - Request failed while connecting
- **RESULT_CANT_RESOLVE** = 3 - Request failed while resolving
- **RESULT_CONNECTION_ERROR** = 4 - Request failed due to connection (read/write) error
- **RESULT_TLS_HANDSHAKE_ERROR** = 5 - Request failed on TLS handshake
- **RESULT_NO_RESPONSE** = 6 - Request does not have a response (yet)
- **RESULT_BODY_SIZE_LIMIT_EXCEEDED** = 7 - Request exceeded its maximum size limit
- **RESULT_BODY_DECOMPRESS_FAILED** = 8 - Request failed due to an error while decompressing the response body
- **RESULT_REQUEST_FAILED** = 9 - Request failed (currently unused)
- **RESULT_DOWNLOAD_FILE_CANT_OPEN** = 10 - HTTPRequest couldn't open the download file
- **RESULT_DOWNLOAD_FILE_WRITE_ERROR** = 11 - HTTPRequest couldn't write to the download file
- **RESULT_REDIRECT_LIMIT_REACHED** = 12 - Request reached its maximum redirect limit
- **RESULT_TIMEOUT** = 13 - Request failed due to a timeout

## Usage Examples

**Basic GET Request:**
```gdscript
func _ready() -> void:
    var http_request: HTTPRequest = HTTPRequest.new()
    add_child(http_request)
    http_request.request_completed.connect(_on_request_completed)

    var error: Error = http_request.request("https://httpbin.org/get")
    if error != OK:
        push_error("An error occurred in the HTTP request.")

func _on_request_completed(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray) -> void:
    var json: JSON = JSON.new()
    json.parse(body.get_string_from_utf8())
    var response: Variant = json.get_data()
    print(response)
```

**POST Request with JSON:**
```gdscript
func post_json(url: String, data: Dictionary) -> void:
    var http_request: HTTPRequest = HTTPRequest.new()
    add_child(http_request)
    http_request.request_completed.connect(_on_request_completed)

    var body: String = JSON.new().stringify(data)
    var headers: PackedStringArray = ["Content-Type: application/json"]

    var error: Error = http_request.request(url, headers, HTTPClient.METHOD_POST, body)
    if error != OK:
        push_error("An error occurred in the HTTP request.")
```

**Download Image:**
```gdscript
func _ready() -> void:
    var http_request: HTTPRequest = HTTPRequest.new()
    add_child(http_request)
    http_request.request_completed.connect(_on_image_downloaded)

    var error: Error = http_request.request("https://placehold.co/512.png")
    if error != OK:
        push_error("An error occurred in the HTTP request.")

func _on_image_downloaded(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray) -> void:
    if result != HTTPRequest.RESULT_SUCCESS:
        push_error("Image couldn't be downloaded.")
        return

    var image: Image = Image.new()
    var error: Error = image.load_png_from_buffer(body)
    if error != OK:
        push_error("Couldn't load the image.")
        return

    var texture: ImageTexture = ImageTexture.create_from_image(image)
    # Use texture...
```

**Download to File:**
```gdscript
func download_file(url: String, file_path: String) -> void:
    var http_request: HTTPRequest = HTTPRequest.new()
    add_child(http_request)
    http_request.download_file = file_path
    http_request.request_completed.connect(_on_download_completed)

    var error: Error = http_request.request(url)
    if error != OK:
        push_error("An error occurred in the HTTP request.")

func _on_download_completed(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray) -> void:
    if result == HTTPRequest.RESULT_SUCCESS:
        print("File downloaded successfully!")
    else:
        push_error("Download failed with result: ", result)
```

**Custom Headers and Authentication:**
```gdscript
func authenticated_request(url: String, token: String) -> void:
    var http_request: HTTPRequest = HTTPRequest.new()
    add_child(http_request)
    http_request.request_completed.connect(_on_request_completed)

    var headers: PackedStringArray = [
        "Authorization: Bearer " + token,
        "Accept: application/json"
    ]

    var error: Error = http_request.request(url, headers)
    if error != OK:
        push_error("An error occurred in the HTTP request.")
```

**Timeout Configuration:**
```gdscript
func _ready() -> void:
    var http_request: HTTPRequest = HTTPRequest.new()
    add_child(http_request)

    # Set timeout to 10 seconds
    http_request.timeout = 10.0

    # For large downloads, disable timeout
    http_request.timeout = 0.0

    http_request.request_completed.connect(_on_request_completed)
    http_request.request("https://example.com/api/endpoint")
```

## Important Notes

**GET Request Data:**
- When method is HTTPClient.METHOD_GET, the payload sent via request_data might be ignored by the server or even cause the server to reject the request (check RFC 7231 section 4.3.1). As a workaround, you can send data as a query string in the URL (see String.uri_encode() for an example).

**Security:**
- It's recommended to use transport encryption (TLS) and to avoid sending sensitive information (such as login credentials) in HTTP GET URL parameters. Consider using HTTP POST requests or HTTP headers for such information instead.

**Body Size:**
- Some Web servers may not send a body length. In this case, get_body_size() will return -1. If using chunked transfer encoding, the body length will also be -1.

**Threading:**
- Use use_threads = true for better performance, especially for large downloads or uploads.

## Tutorials

- [Making HTTP requests](https://docs.godotengine.org/en/stable/tutorials/networking/http_request_class.html)
- [TLS certificates](https://docs.godotengine.org/en/stable/tutorials/networking/ssl_certificates.html)
