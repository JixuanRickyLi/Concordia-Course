# SOEN 387 - FALL 2019 - Assignment 1

## Team Member Contribution:

We did this assignment together.

## WAR file:

We generate a WAR file using the IDE IntellijIDEA. Create a new Artifact in the project settings, then select the
type as `Web Application: Archive`, then create a manifest.mf file. Then build this artifact, we can see a new
SOEN_387_A1_war.war file is created in the /out/artifacts/SOEN_387_A1_war folder.

## Run the HttpServer in Task 3

We run the class using IntellijIDEA. It require Java 1.8 (or above) installed on the machine.

## What happens when you submit the html forms in Task 3?

The page crash because in the simple http server, we did not handle the previous path `/display` used in task 1 and 2.

## Task 1

In task 1 and task 2, we use tomcat 9.0.26 as the server. The server must be started first.

The servlet file is /web/src/Servlet/DisplayHttpRequest.java

The StringUtils.java file is used to encode the Strings and display display them in a html page properly.

If the "format" parameter has a invalid value, we throw a ServletException with a message, and a default server error
 page will be displayed.
 
Our URL pattern is "/display". 

For instance, opening the URL "http://localhost:8080/display?format=html&param1=val1&param2=val2" will sent a GET
 request and get a response as a html page, which displays the request method, the request headers, and the request
  parameters.
  
## Task 2

We use bootstrap 4 as a basic css library, and differentiate the html pages with css-file1.css and css-file2.css

## Task 3

The http server file is /web/src/SimpleHttpServer.java

## Task 4

### curl -v -H user-agent:SOEN387 http://localhost:8080/display?format=html

```
$ curl -v -H user-agent:SOEN387 http://localhost:8080/display?format=html
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0*   Trying ::1:8080...
* TCP_NODELAY set
* Connected to localhost (::1) port 8080 (#0)
> GET /display?format=html HTTP/1.1
> Host: localhost:8080
> Accept: */*
> user-agent:SOEN387
>
* Mark bundle as not supporting multiuse
< HTTP/1.1 200
< Content-Type: text/html;charset=ISO-8859-1
< Transfer-Encoding: chunked
< Date: Sun, 06 Oct 2019 18:51:01 GMT
<
{ [714 bytes data]
100   707    0   707    0     0   172k      0 --:--:-- --:--:-- --:--:--  172k<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Basic Servlet</title>
<style>
table, th, td {
border: 1px solid black; border-collapse: collapse; padding: 5px; text-align:left;}
</style>
</head>
<body>


<table style="width:50%;">
<tr>
<th style="width:25%;">Request Method: </th>
<td>GET</td>
</tr>
</table>

</br>
<table style="width:50%;">
<tr><th colspan="2">Request Headers: </th></tr>

<tr><th>host</th><td>localhost:8080</td></tr>
<tr><th>accept</th><td>*/*</td></tr>
<tr><th>user-agent</th><td>SOEN387</td></tr>
</table>
</br>
<table style="width:50%;">
<tr><th colspan="2">Query String: </th></tr>
<tr><th>format</th><td>html</td></tr>
</table>

</body>
</html>

```

### curl -v -X POST -H user-agent:SOEN387 http://localhost:8080/display?format=html

```
$ curl -v -X POST -H user-agent:SOEN387 http://localhost:8080/display?format=html
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0*   Trying ::1:8080...
* TCP_NODELAY set
* Connected to localhost (::1) port 8080 (#0)
> POST /display?format=html HTTP/1.1
> Host: localhost:8080
> Accept: */*
> user-agent:SOEN387
>
* Mark bundle as not supporting multiuse
< HTTP/1.1 200
< Content-Type: text/html;charset=ISO-8859-1
< Transfer-Encoding: chunked
< Date: Sun, 06 Oct 2019 18:52:49 GMT
<
{ [715 bytes data]
100   708    0   708    0     0   230k      0 --:--:-- --:--:-- --:--:--  230k<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Basic Servlet</title>
<style>
table, th, td {
border: 1px solid black; border-collapse: collapse; padding: 5px; text-align:left;}
</style>
</head>
<body>


<table style="width:50%;">
<tr>
<th style="width:25%;">Request Method: </th>
<td>POST</td>
</tr>
</table>

</br>
<table style="width:50%;">
<tr><th colspan="2">Request Headers: </th></tr>

<tr><th>host</th><td>localhost:8080</td></tr>
<tr><th>accept</th><td>*/*</td></tr>
<tr><th>user-agent</th><td>SOEN387</td></tr>
</table>
</br>
<table style="width:50%;">
<tr><th colspan="2">Query String: </th></tr>
<tr><th>format</th><td>html</td></tr>
</table>

</body>
</html>
```

### curl -v -H user-agent:SOEN387 http://localhost:8080/index.html

```
$ curl -v -H user-agent:SOEN387 http://localhost:8080/index.html
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0*   Trying ::1:8080...
* TCP_NODELAY set
* Connected to localhost (::1) port 8080 (#0)
> GET /index.html HTTP/1.1
> Host: localhost:8080
> Accept: */*
> user-agent:SOEN387
>
* Mark bundle as not supporting multiuse
< HTTP/1.1 200
< Accept-Ranges: bytes
< ETag: W/"1978-1569789536417"
< Last-Modified: Sun, 29 Sep 2019 20:38:56 GMT
< Content-Type: text/html
< Content-Length: 1978
< Date: Sun, 06 Oct 2019 18:54:46 GMT
<
{ [1978 bytes data]
100  1978  100  1978    0     0   482k      0 --:--:-- --:--:-- --:--:--  482k<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html
        PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
    <title>Title</title>
    <link rel="stylesheet" type="text/css" href="bootstrap.min.css">
    <link rel="stylesheet" type="text/css" href="css/css-file1.css">
    <script type="application/javascript" src="bootstrap.min.js"></script>
</head>
<body>
<div class="container">
    <div class="row m-5">
        <div class="col-12">
            <h2>Send a GET Request</h2>
            <form action="/display" method="get">
                <div class="form-group">
                    <label for="name">Name</label>
                    <input name="name" type="text" class="form-control" id="name" placeholder="Enter name">
                </div>
                <div class="form-group">
                    <label for="email">Email address</label>
                    <input name="email" type="email" class="form-control" id="email" aria-describedby="emailHelp"
                            placeholder="Enter email">
                </div>
                <div class="form-group">
                    <label for="format">format:</label>
                    <select name="format" class="form-control" id="format">
                        <option></option>
                        <option value="html">html</option>
                        <option value="text">plain text</option>
                        <option value="xml">xml</option>
                    </select>
                </div>
                <button type="submit" class="btn btn-primary">Submit</button>
                <a href="index2.html" class="btn btn-success active" role="button" aria-pressed="true">Switch to
                    POST method</a>
            </form>
        </div>
    </div>
</div>
</body>
</html>

```

### curl -v -X POST -H user-agent:SOEN387 http://localhost:8080?format=text

```
$ curl -v -X POST -H user-agent:SOEN387 http://localhost:8080?format=text
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0*   Trying ::1:8080...
* TCP_NODELAY set
* Connected to localhost (::1) port 8080 (#0)
> POST /?format=text HTTP/1.1
> Host: localhost:8080
> Accept: */*
> user-agent:SOEN387
>
* Empty reply from server
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
* Connection #0 to host localhost left intact
curl: (52) Empty reply from server
```

The last one has empty reply because in the requirement, we only need to implement a http-server which returns a
static file like index.html. If we send a POST request and set the format to text, there will be no content displayed.
 
