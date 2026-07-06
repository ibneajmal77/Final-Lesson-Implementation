# API Integration System Interview Prep

Prepared on: 2026-07-06  
Interview target: 2026-07-07  
Focus: API integration, data formats, HTTP, Power Automate, Azure messaging, low-code flows, file/scheduler patterns, and practical coding tasks.

## How To Use This Guide

Use this as a one-day crash plan and an interview answer bank.

Your goal is not to memorize every tool. Your goal is to explain how integration systems move data safely:

1. Identify the source and target systems.
2. Understand the API contract.
3. Authenticate securely.
4. Send the correct request.
5. Transform JSON, XML, YAML, or file data.
6. Handle status codes, retries, duplicates, and failures.
7. Monitor and support the integration.

Assumption: "friends API" means a sample CRUD API for friend records. If your interviewer means a real internal API with that name, map the same concepts to that API.

## 24-Hour Prep Plan

### Block 1: API Basics, 90 minutes

Know these cold:

- HTTP methods: GET, POST, PUT, PATCH, DELETE.
- Request parts: URL, path parameters, query parameters, headers, body.
- Response parts: status code, headers, body.
- JSON request and response shape.
- Difference between sync API and async messaging.

Practice answer:

> An API integration connects systems through a contract. I check the endpoint, method, parameters, authentication, payload format, response schema, and error behavior. Then I build transformation, retry, logging, and monitoring around it.

### Block 2: Parameters and Status Codes, 60 minutes

Memorize:

- Path parameter identifies a resource: `/friends/{friendId}`.
- Query parameter filters, sorts, searches, or paginates: `/friends?city=Lahore&page=2`.
- 2xx means success.
- 3xx means redirect.
- 4xx means client/request problem.
- 5xx means server/downstream problem.

### Block 3: JSON, XML, XSLT, YAML, RAML, 2 hours

Be able to explain:

- JSON is common for REST API payloads.
- XML is common in enterprise/legacy integrations.
- XSLT transforms XML from one structure to another.
- YAML is human-readable configuration/data.
- RAML is YAML-based API modeling.
- OpenAPI is the most common HTTP API contract/spec format.

### Block 4: Power Automate, 2 hours

Know the flow:

- Trigger: scheduled, manual, automated, or HTTP request.
- Actions: HTTP call, Parse JSON, Condition, Apply to each, Filter array, Compose, Create item, Send email.
- Error handling: Scope, Configure run after, retry policy, terminate, logging.
- Custom connectors: wrap an API so makers can use it like a native connector.

### Block 5: Azure Messaging, 90 minutes

Understand:

- Azure Event Hubs with Kafka endpoint: event streaming, high-throughput logs, Kafka protocol compatibility.
- Azure Service Bus: queues/topics for enterprise messaging, commands, workflows, retries, DLQ.
- Kafka/Event Hubs is usually for event streams.
- Service Bus is usually for reliable business messages and workflow decoupling.

### Block 6: Mock Interview, 2 hours

Answer out loud:

- "Design an integration from a Friends API into our CRM."
- "What happens if the API returns 429?"
- "How do you parse JSON in Power Automate?"
- "Path parameter vs query parameter?"
- "When would you use Service Bus instead of Kafka?"
- "How would you transform XML?"
- "How do you prevent duplicate processing?"

## One-Minute Interview Intro

Use this if they ask, "Tell me about API integration."

> API integration is about connecting systems reliably through a clear contract. I start by understanding the endpoint, method, authentication, request payload, response schema, and expected errors. Then I design how data moves, how it is transformed, how failures are retried or dead-lettered, and how the integration is monitored. For low-code platforms like Power Automate, I would use triggers, HTTP actions, Parse JSON, conditions, loops, and custom connectors. For higher-volume or decoupled systems, I would use Azure Service Bus for reliable business messages or Event Hubs/Kafka for streaming events.

## API Integration Mental Model

Every integration has these parts:

- Source: system that produces data, such as Friends API, file storage, CRM, ERP, database, webhook.
- Trigger: what starts the flow, such as schedule, manual button, HTTP request, file created event, queue message.
- Contract: endpoint, method, parameters, headers, payload schema, response schema.
- Auth: API key, Basic, OAuth 2.0, managed identity, SAS token, client credentials.
- Transform: convert fields, rename properties, flatten arrays, map codes, XML to JSON, JSON to XML.
- Delivery: synchronous HTTP call or asynchronous message/event.
- Reliability: retry, timeout, idempotency, deduplication, DLQ, compensation.
- Observability: logs, correlation ID, metrics, alerts, run history.
- Security: secrets, least privilege, HTTPS/TLS, input validation, DLP policies.

## HTTP Request Anatomy

Example:

```http
POST /api/friends?notify=true HTTP/1.1
Host: example.com
Authorization: Bearer eyJhbGciOi...
Content-Type: application/json
Accept: application/json
Correlation-Id: 8b7f0a1

{
  "name": "Aisha Khan",
  "email": "aisha@example.com",
  "city": "Lahore"
}
```

Parts:

- Method: `POST`
- Path: `/api/friends`
- Query parameter: `notify=true`
- Headers: `Authorization`, `Content-Type`, `Accept`, `Correlation-Id`
- Body: JSON payload

## HTTP Methods

| Method | Use | Example | Idempotent? |
|---|---|---|---|
| GET | Read resource | `GET /friends/123` | Yes |
| POST | Create or submit operation | `POST /friends` | Usually no |
| PUT | Replace full resource | `PUT /friends/123` | Yes |
| PATCH | Partial update | `PATCH /friends/123` | Usually yes if designed well |
| DELETE | Delete resource | `DELETE /friends/123` | Yes |

Interview line:

> Idempotent means repeating the same request should not create a different final result. This matters for retries.

## Path Parameter vs Query Parameter

| Concept | Path Parameter | Query Parameter |
|---|---|---|
| Purpose | Identifies a specific resource or hierarchy | Filters, searches, sorts, paginates, or controls behavior |
| Location | Inside URL path | After `?` in URL |
| Example | `/friends/123` | `/friends?city=Lahore` |
| Required? | Usually required | Often optional |
| OpenAPI location | `in: path` | `in: query` |
| RAML location | `uriParameters` | `queryParameters` |

Examples:

```http
GET /friends/123
```

`123` is a path parameter because it identifies one friend.

```http
GET /friends?city=Lahore&active=true&page=2
```

`city`, `active`, and `page` are query parameters because they filter or control the list.

Strong interview answer:

> I use path parameters when the value is part of the resource identity, and query parameters when the value modifies the request, such as filtering, sorting, paging, or optional flags.

## HTTP Status Codes

### Status Code Families

| Family | Meaning | Interview meaning |
|---|---|---|
| 1xx | Informational | Rare in normal API work |
| 2xx | Success | Request worked |
| 3xx | Redirection | Client may need another URL |
| 4xx | Client error | Caller sent something wrong or is not allowed |
| 5xx | Server error | API or downstream system failed |

### Common Status Codes

| Code | Meaning | What to do |
|---|---|---|
| 200 | OK | Success with response body |
| 201 | Created | Resource created, often with location/id |
| 202 | Accepted | Request accepted for async processing |
| 204 | No Content | Success, no response body |
| 301/308 | Permanent redirect | Update endpoint if appropriate |
| 302/307 | Temporary redirect | Follow only if client supports it safely |
| 400 | Bad Request | Validate payload, schema, required fields |
| 401 | Unauthorized | Check missing/expired token |
| 403 | Forbidden | Token valid but lacks permission |
| 404 | Not Found | Resource or endpoint not found |
| 405 | Method Not Allowed | Wrong HTTP method |
| 409 | Conflict | Duplicate, version conflict, business state conflict |
| 412 | Precondition Failed | ETag/version condition failed |
| 415 | Unsupported Media Type | Check `Content-Type` |
| 422 | Unprocessable Content | Syntax valid, business validation failed |
| 429 | Too Many Requests | Back off, respect `Retry-After`, reduce concurrency |
| 500 | Internal Server Error | Retry with backoff if transient |
| 502 | Bad Gateway | Gateway/downstream issue, retry |
| 503 | Service Unavailable | Retry later, circuit breaker |
| 504 | Gateway Timeout | Retry carefully, check timeout/idempotency |

Good answer for 429:

> I would respect the `Retry-After` header if present, use exponential backoff, reduce concurrency, and make the operation idempotent so retries do not create duplicates.

## JSON Essentials

JSON data types:

- object: `{ "id": 1 }`
- array: `[1, 2, 3]`
- string: `"Ali"`
- number: `25`
- boolean: `true`
- null: `null`

Example response:

```json
{
  "id": "f-100",
  "name": "Ali Naqvi",
  "email": "ali@example.com",
  "tags": ["school", "cricket"],
  "address": {
    "city": "Karachi",
    "country": "PK"
  }
}
```

Common extraction examples:

```text
name -> body('HTTP')?['name']
city -> body('HTTP')?['address']?['city']
first tag -> body('HTTP')?['tags']?[0]
```

In Power Automate, after `Parse JSON`, you can use dynamic fields directly. Without `Parse JSON`, you often use expressions like:

```text
body('HTTP')?['id']
body('HTTP')?['address']?['city']
triggerBody()?['friendId']
items('Apply_to_each')?['email']
```

## Extract JSON From Text

Interview scenario: "Given a string containing JSON, extract the JSON."

Example input:

```text
Status ok. Payload: {"id":123,"name":"Ali","active":true}. Done.
```

Practical approach:

1. Find the first `{` or `[`.
2. Parse until the matching closing `}` or `]`.
3. Validate with a JSON parser.
4. Avoid regex-only parsing for nested JSON because braces can be nested.

Python example:

```python
import json

def extract_first_json(text: str):
    starts = [i for i in (text.find("{"), text.find("[")) if i != -1]
    if not starts:
        raise ValueError("No JSON object or array start found")

    start = min(starts)
    stack = []
    in_string = False
    escape = False

    pairs = {"{": "}", "[": "]"}

    for i in range(start, len(text)):
        ch = text[i]

        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            continue

        if ch == '"':
            in_string = True
        elif ch in pairs:
            stack.append(pairs[ch])
        elif stack and ch == stack[-1]:
            stack.pop()
            if not stack:
                return json.loads(text[start:i + 1])

    raise ValueError("JSON was not complete")

print(extract_first_json('Payload: {"id":123,"name":"Ali"} done'))
```

C# example:

```csharp
using System;
using System.Collections.Generic;
using System.Text.Json;

public static class Program
{
    public static void Main()
    {
        string text = "Status ok. Payload: {\"id\":123,\"name\":\"Ali\",\"active\":true}. Done.";
        JsonElement json = ExtractFirstJson(text);

        Console.WriteLine(JsonSerializer.Serialize(json, new JsonSerializerOptions
        {
            WriteIndented = true
        }));
    }

    public static JsonElement ExtractFirstJson(string text)
    {
        int objectStart = text.IndexOf('{');
        int arrayStart = text.IndexOf('[');

        int start = GetFirstJsonStart(objectStart, arrayStart);
        if (start == -1)
        {
            throw new InvalidOperationException("No JSON object or array start found.");
        }

        var stack = new Stack<char>();
        bool inString = false;
        bool escaping = false;

        for (int i = start; i < text.Length; i++)
        {
            char current = text[i];

            if (inString)
            {
                if (escaping)
                {
                    escaping = false;
                }
                else if (current == '\\')
                {
                    escaping = true;
                }
                else if (current == '"')
                {
                    inString = false;
                }

                continue;
            }

            if (current == '"')
            {
                inString = true;
            }
            else if (current == '{')
            {
                stack.Push('}');
            }
            else if (current == '[')
            {
                stack.Push(']');
            }
            else if (stack.Count > 0 && current == stack.Peek())
            {
                stack.Pop();

                if (stack.Count == 0)
                {
                    string jsonText = text.Substring(start, i - start + 1);
                    using JsonDocument document = JsonDocument.Parse(jsonText);
                    return document.RootElement.Clone();
                }
            }
        }

        throw new InvalidOperationException("JSON was not complete.");
    }

    private static int GetFirstJsonStart(int objectStart, int arrayStart)
    {
        if (objectStart == -1)
        {
            return arrayStart;
        }

        if (arrayStart == -1)
        {
            return objectStart;
        }

        return Math.Min(objectStart, arrayStart);
    }
}
```

### C# JSON Extraction From API Response Using LINQ

Interview scenario: "An API returns JSON. Extract active friends from Lahore and print their names."

Input JSON:

```json
{
  "requestId": "req-100",
  "data": {
    "friends": [
      {
        "id": "f-100",
        "firstName": "Ali",
        "lastName": "Naqvi",
        "email": "ali@example.com",
        "city": "Karachi",
        "active": true
      },
      {
        "id": "f-101",
        "firstName": "Sara",
        "lastName": "Ahmed",
        "email": "sara@example.com",
        "city": "Lahore",
        "active": true
      },
      {
        "id": "f-102",
        "firstName": "Usman",
        "lastName": "Khan",
        "email": "usman@example.com",
        "city": "Lahore",
        "active": false
      }
    ]
  }
}
```

C# LINQ solution:

```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.Json;

public sealed record FriendSummary(string Id, string FullName, string Email);

public static class Program
{
    public static void Main()
    {
        string json = @"
        {
          ""requestId"": ""req-100"",
          ""data"": {
            ""friends"": [
              {
                ""id"": ""f-100"",
                ""firstName"": ""Ali"",
                ""lastName"": ""Naqvi"",
                ""email"": ""ali@example.com"",
                ""city"": ""Karachi"",
                ""active"": true
              },
              {
                ""id"": ""f-101"",
                ""firstName"": ""Sara"",
                ""lastName"": ""Ahmed"",
                ""email"": ""sara@example.com"",
                ""city"": ""Lahore"",
                ""active"": true
              },
              {
                ""id"": ""f-102"",
                ""firstName"": ""Usman"",
                ""lastName"": ""Khan"",
                ""email"": ""usman@example.com"",
                ""city"": ""Lahore"",
                ""active"": false
              }
            ]
          }
        }";

        List<FriendSummary> activeLahoreFriends = ExtractActiveFriendsByCity(json, "Lahore");

        foreach (FriendSummary friend in activeLahoreFriends)
        {
            Console.WriteLine($"{friend.Id}: {friend.FullName} - {friend.Email}");
        }
    }

    public static List<FriendSummary> ExtractActiveFriendsByCity(string json, string city)
    {
        using JsonDocument document = JsonDocument.Parse(json);

        JsonElement friends = document
            .RootElement
            .GetProperty("data")
            .GetProperty("friends");

        List<FriendSummary> result =
            (from friend in friends.EnumerateArray()
             let isActive = friend.GetProperty("active").GetBoolean()
             let friendCity = friend.GetProperty("city").GetString()
             where isActive && string.Equals(friendCity, city, StringComparison.OrdinalIgnoreCase)
             select new FriendSummary(
                 Id: friend.GetProperty("id").GetString() ?? "",
                 FullName: $"{friend.GetProperty("firstName").GetString()} {friend.GetProperty("lastName").GetString()}",
                 Email: friend.GetProperty("email").GetString() ?? ""))
            .ToList();

        return result;
    }
}
```

Output:

```text
f-101: Sara Ahmed - sara@example.com
```

If the JSON comes from an actual API call, the extraction method stays the same:

```csharp
using HttpClient http = new HttpClient();
string json = await http.GetStringAsync("https://api.example.com/friends");

List<FriendSummary> friends = ExtractActiveFriendsByCity(json, "Lahore");
```

What to say:

> I parse the API response into a `JsonDocument`, enumerate the JSON array, and use LINQ to filter and project only the fields I need. I materialize the result with `ToList()` before the `JsonDocument` is disposed.

Interview explanation:

> I would prefer using a real JSON parser once I identify the candidate JSON substring. Regex is fragile for nested objects, arrays, escaped quotes, and strings that contain braces.

## Paragraph Token Frequency Coding Task

Problem: Given a paragraph, count how many times each token appears. A token can be a word, number, punctuation mark, or symbol.

Example:

```text
"words, words ==> words frequency"
```

Expected result:

```json
{
  "words": 3,
  ",": 1,
  "=": 2,
  ">": 1,
  "frequency": 1
}
```

Python solution:

```python
import re
from collections import Counter

def token_frequency(text: str) -> dict[str, int]:
    tokens = re.findall(r"[a-zA-Z0-9]+|[^\sA-Za-z0-9]", text.lower())
    return dict(Counter(tokens))

print(token_frequency("words, words ==> words frequency"))
```

JavaScript solution:

```javascript
function tokenFrequency(text) {
  const tokens = text.toLowerCase().match(/[a-z0-9]+|[^\sA-Za-z0-9]/g) || [];
  const counts = {};

  for (const token of tokens) {
    counts[token] = (counts[token] || 0) + 1;
  }

  return counts;
}

console.log(tokenFrequency("words, words ==> words frequency"));
```

C# solution: count words, numbers, punctuation, and symbols

```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;

public static class Program
{
    public static void Main()
    {
        string paragraph = "words, words ==> words frequency";

        Dictionary<string, int> counts = TokenFrequency(paragraph);

        foreach (KeyValuePair<string, int> pair in counts)
        {
            Console.WriteLine($"{pair.Key}: {pair.Value}");
        }
    }

    public static Dictionary<string, int> TokenFrequency(string text)
    {
        // [a-z0-9]+ counts a full word/number as one token.
        // [^\\sA-Za-z0-9] counts punctuation and symbols as tokens.
        return Regex.Matches(text.ToLowerInvariant(), @"[a-z0-9]+|[^\sA-Za-z0-9]")
            .Cast<Match>()
            .Select(match => match.Value)
            .GroupBy(token => token)
            .ToDictionary(group => group.Key, group => group.Count());
    }
}
```

Output:

```text
words: 3
,: 1
=: 2
>: 1
frequency: 1
```

If the interviewer wants consecutive symbols counted as one token, for example `==>` as one item, use this regex instead:

```csharp
@"[a-z0-9]+|[^\sA-Za-z0-9]+"
```

That would produce:

```text
words: 3
,: 1
==>: 1
frequency: 1
```

If the interviewer literally means every character, including punctuation and spaces, use character frequency:

```csharp
using System;
using System.Collections.Generic;
using System.Linq;

public static class Program
{
    public static void Main()
    {
        string paragraph = "words, words ==> words frequency";
        Dictionary<char, int> counts = CharacterFrequency(paragraph);

        foreach (KeyValuePair<char, int> pair in counts)
        {
            string display = pair.Key == ' ' ? "[space]" : pair.Key.ToString();
            Console.WriteLine($"{display}: {pair.Value}");
        }
    }

    public static Dictionary<char, int> CharacterFrequency(string text)
    {
        return text
            .GroupBy(character => character)
            .ToDictionary(group => group.Key, group => group.Count());
    }
}
```

What to say:

> I first clarify the unit of counting. If the requirement is words plus punctuation, I tokenize the paragraph with a regex and group the tokens. If the requirement is literally every character, I group by character directly. In both cases, time complexity is O(n).

## XML Essentials

XML is markup with elements, attributes, and text.

Example:

```xml
<friend id="f-100">
  <name>Ali Naqvi</name>
  <email>ali@example.com</email>
  <city>Karachi</city>
</friend>
```

Key concepts:

- Element: `<name>Ali</name>`
- Attribute: `id="f-100"`
- Root element: one top-level element
- Namespace: avoids name conflicts
- XSD: XML Schema Definition, validates structure and types
- XPath: selects nodes from XML
- XSLT: transforms XML into another XML, HTML, text, or sometimes JSON-like text

XPath examples:

```xpath
/friend/name
/friend/@id
//email
```

## XSLT Essentials

XSLT transforms one XML shape into another.

Input XML:

```xml
<friend id="f-100">
  <name>Ali Naqvi</name>
  <email>ali@example.com</email>
</friend>
```

Output XML:

```xml
<contact>
  <contactId>f-100</contactId>
  <fullName>Ali Naqvi</fullName>
  <emailAddress>ali@example.com</emailAddress>
</contact>
```

XSLT:

```xml
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:template match="/friend">
    <contact>
      <contactId><xsl:value-of select="@id"/></contactId>
      <fullName><xsl:value-of select="name"/></fullName>
      <emailAddress><xsl:value-of select="email"/></emailAddress>
    </contact>
  </xsl:template>
</xsl:stylesheet>
```

Interview line:

> XPath is for selecting data from XML. XSLT is for transforming XML into a different output structure.

## YAML Essentials

YAML is commonly used for configuration and API specs. It is indentation-sensitive.

Example:

```yaml
friend:
  id: f-100
  name: Ali Naqvi
  tags:
    - school
    - cricket
```

Common mistakes:

- Bad indentation.
- Mixing tabs and spaces.
- Forgetting quotes around values that look like booleans or dates.
- Duplicating keys.

## RAML Essentials

RAML stands for RESTful API Modeling Language. It is YAML-based and used to describe REST APIs.

Minimal RAML example:

```yaml
#%RAML 1.0
title: Friends API
version: v1
baseUri: https://api.example.com/{version}
mediaType: application/json

types:
  Friend:
    type: object
    properties:
      id: string
      name: string
      email: string
      city?: string

/friends:
  get:
    queryParameters:
      city?:
        type: string
      active?:
        type: boolean
    responses:
      200:
        body:
          application/json:
            type: Friend[]
  post:
    body:
      application/json:
        type: Friend
    responses:
      201:
        body:
          application/json:
            type: Friend

/friends/{friendId}:
  uriParameters:
    friendId:
      type: string
  get:
    responses:
      200:
        body:
          application/json:
            type: Friend
```

RAML interview points:

- RAML files usually start with `#%RAML 1.0`.
- It models resources, methods, parameters, request bodies, responses, types, and security.
- Path/template URI parameters are defined as `uriParameters`.
- Query parameters are defined as `queryParameters`.

## OpenAPI Essentials

OpenAPI is a standard way to describe HTTP APIs. It can be written in YAML or JSON.

Minimal OpenAPI example:

```yaml
openapi: 3.0.3
info:
  title: Friends API
  version: 1.0.0
servers:
  - url: https://api.example.com
paths:
  /friends/{friendId}:
    get:
      parameters:
        - name: friendId
          in: path
          required: true
          schema:
            type: string
        - name: includeHistory
          in: query
          required: false
          schema:
            type: boolean
      responses:
        "200":
          description: Friend found
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Friend"
        "404":
          description: Friend not found
components:
  schemas:
    Friend:
      type: object
      required:
        - id
        - name
        - email
      properties:
        id:
          type: string
        name:
          type: string
        email:
          type: string
```

Interview line:

> OpenAPI is useful because it acts as a contract. Developers, testers, API gateways, documentation tools, and low-code custom connectors can use the same definition.

## Friends API Example

Resource: Friend

```json
{
  "id": "f-100",
  "firstName": "Ali",
  "lastName": "Naqvi",
  "email": "ali@example.com",
  "city": "Karachi",
  "active": true,
  "updatedAt": "2026-07-06T13:30:00Z"
}
```

Possible endpoints:

| Endpoint | Method | Purpose |
|---|---|---|
| `/friends` | GET | List friends |
| `/friends?city=Karachi` | GET | Filter friends |
| `/friends/{friendId}` | GET | Get one friend |
| `/friends` | POST | Create friend |
| `/friends/{friendId}` | PUT | Replace friend |
| `/friends/{friendId}` | PATCH | Update some fields |
| `/friends/{friendId}` | DELETE | Delete friend |

Example create request:

```http
POST /friends HTTP/1.1
Content-Type: application/json
Authorization: Bearer <token>

{
  "firstName": "Sara",
  "lastName": "Ahmed",
  "email": "sara@example.com",
  "city": "Lahore"
}
```

Example response:

```http
HTTP/1.1 201 Created
Content-Type: application/json
Location: /friends/f-101

{
  "id": "f-101",
  "firstName": "Sara",
  "lastName": "Ahmed",
  "email": "sara@example.com",
  "city": "Lahore",
  "active": true
}
```

## C# Friends API Integration Example

This example shows path parameters, query parameters, JSON request bodies, bearer token authentication, and status-code handling.

Replace `https://api.example.com/` and `token` with real values before running.

```csharp
using System;
using System.Collections.Generic;
using System.Net;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Net.Http.Json;
using System.Threading.Tasks;

public sealed record Friend(
    string? Id,
    string FirstName,
    string LastName,
    string Email,
    string? City,
    bool Active);

public sealed record CreateFriendRequest(
    string FirstName,
    string LastName,
    string Email,
    string? City);

public sealed class FriendsApiClient
{
    private readonly HttpClient _http;

    public FriendsApiClient(HttpClient http, string token)
    {
        _http = http;
        _http.BaseAddress = new Uri("https://api.example.com/");
        _http.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", token);
        _http.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));
    }

    public async Task<Friend?> GetFriendByIdAsync(string friendId)
    {
        // friendId is a path parameter.
        string path = $"friends/{Uri.EscapeDataString(friendId)}";

        using HttpResponseMessage response = await _http.GetAsync(path);

        if (response.StatusCode == HttpStatusCode.NotFound)
        {
            return null;
        }

        await EnsureSuccessAsync(response);

        return await response.Content.ReadFromJsonAsync<Friend>();
    }

    public async Task<List<Friend>> SearchFriendsByCityAsync(string city)
    {
        // city and active are query parameters.
        string path = $"friends?city={Uri.EscapeDataString(city)}&active=true";

        using HttpResponseMessage response = await _http.GetAsync(path);
        await EnsureSuccessAsync(response);

        return await response.Content.ReadFromJsonAsync<List<Friend>>() ?? new List<Friend>();
    }

    public async Task<Friend> CreateFriendAsync(CreateFriendRequest request)
    {
        using HttpResponseMessage response = await _http.PostAsJsonAsync("friends", request);

        if (response.StatusCode != HttpStatusCode.Created)
        {
            await EnsureSuccessAsync(response);
        }

        Friend? created = await response.Content.ReadFromJsonAsync<Friend>();

        return created ?? throw new InvalidOperationException("API returned an empty response body.");
    }

    private static async Task EnsureSuccessAsync(HttpResponseMessage response)
    {
        if (response.IsSuccessStatusCode)
        {
            return;
        }

        string body = await response.Content.ReadAsStringAsync();

        string message = response.StatusCode switch
        {
            HttpStatusCode.BadRequest => "Bad request. Check payload, required fields, and schema.",
            HttpStatusCode.Unauthorized => "Unauthorized. Token is missing, invalid, or expired.",
            HttpStatusCode.Forbidden => "Forbidden. Token is valid but does not have permission.",
            HttpStatusCode.TooManyRequests => "Rate limited. Back off and respect Retry-After if present.",
            HttpStatusCode.InternalServerError => "Server error. Retry if the operation is idempotent.",
            HttpStatusCode.BadGateway => "Bad gateway. Downstream service may be unavailable.",
            HttpStatusCode.ServiceUnavailable => "Service unavailable. Retry later.",
            HttpStatusCode.GatewayTimeout => "Gateway timeout. Retry carefully with idempotency.",
            _ => $"API call failed with status {(int)response.StatusCode}."
        };

        throw new HttpRequestException($"{message} Response body: {body}");
    }
}

public static class Program
{
    public static async Task Main()
    {
        using var http = new HttpClient();
        var client = new FriendsApiClient(http, token: "replace-with-access-token");

        Friend? existing = await client.GetFriendByIdAsync("f-100");
        Console.WriteLine(existing is null ? "Friend not found." : existing.Email);

        List<Friend> lahoreFriends = await client.SearchFriendsByCityAsync("Lahore");
        Console.WriteLine($"Found {lahoreFriends.Count} active friends in Lahore.");

        Friend created = await client.CreateFriendAsync(new CreateFriendRequest(
            FirstName: "Sara",
            LastName: "Ahmed",
            Email: "sara@example.com",
            City: "Lahore"));

        Console.WriteLine($"Created friend ID: {created.Id}");
    }
}
```

What to say:

> In C#, I use `HttpClient` for API calls, serialize request bodies as JSON, deserialize responses into typed models, URL-encode path and query parameter values, and handle status codes explicitly. For retries, I only retry transient failures and make sure the operation is idempotent.

## Power Automate Essentials

Power Automate is a low-code workflow service.

Flow types:

- Automated cloud flow: starts from an event, such as new email or new SharePoint file.
- Instant cloud flow: starts manually, such as button click.
- Scheduled cloud flow: starts on a recurrence, such as every day at 8 AM.
- Desktop flow: automates UI actions on desktop apps.

Common building blocks:

- Trigger: starts the flow.
- Action: does work.
- Connector: talks to a service.
- Condition: if/else branching.
- Apply to each: loop through array.
- Parse JSON: creates typed dynamic content from JSON.
- Compose: stores an expression result.
- Filter array: filters an array.
- Select: maps an array to a new shape.
- Scope: groups actions, useful for try/catch-style error handling.
- Terminate: ends flow with success, failure, or cancellation.

## Power Automate HTTP Flow Pattern

Scenario: Call Friends API every morning and save active friends into SharePoint or Dataverse.

Steps:

1. Trigger: Recurrence, daily at 8 AM.
2. Action: HTTP GET `https://api.example.com/friends?active=true`.
3. Action: Parse JSON using sample response schema.
4. Action: Apply to each friend.
5. Action: Upsert record into target system.
6. Action: Log success count.
7. Error scope: log error, send Teams/email alert, terminate failed.

HTTP action fields:

- Method: GET/POST/PUT/PATCH/DELETE.
- URI: endpoint URL.
- Headers: auth, content type, accept.
- Body: request payload for POST/PUT/PATCH.

Example headers:

```json
{
  "Authorization": "Bearer <token>",
  "Accept": "application/json",
  "Content-Type": "application/json",
  "Correlation-Id": "@{guid()}"
}
```

## Power Automate Parse JSON

Example JSON:

```json
{
  "id": "f-100",
  "name": "Ali Naqvi",
  "city": "Karachi"
}
```

Example schema:

```json
{
  "type": "object",
  "properties": {
    "id": {
      "type": "string"
    },
    "name": {
      "type": "string"
    },
    "city": {
      "type": "string"
    }
  },
  "required": ["id", "name"]
}
```

Key expressions:

```text
triggerBody()
body('HTTP')
body('Parse_JSON')?['id']
items('Apply_to_each')?['email']
outputs('Compose')
coalesce(body('Parse_JSON')?['city'], 'Unknown')
```

## Power Automate Error Handling

Recommended structure:

- Scope: Try
- Scope: Catch
- Scope: Finally

Use "Configure run after":

- Catch runs after Try has failed, timed out, or been skipped.
- Finally runs after Try/Catch as needed.

Retry strategy:

- Retry only transient errors: 408, 429, 500, 502, 503, 504.
- Do not blindly retry validation errors: 400, 401, 403, 404, 422.
- Use exponential backoff where possible.
- For 429, respect `Retry-After`.

Interview line:

> In Power Automate, I group risky actions in a Scope, configure a Catch scope to run after failure, log the error details, and send an alert. I also tune retry policies and avoid retrying permanent validation errors.

## Power Automate Custom Connectors

Use a custom connector when:

- The API does not have a built-in Power Automate connector.
- You want reusable actions like `Get friend`, `Create friend`, `Update friend`.
- You want makers to avoid manually configuring raw HTTP every time.
- You have an OpenAPI definition that can describe the API.

Custom connector pieces:

- Host/base URL.
- Authentication.
- Actions.
- Request definitions.
- Response definitions.
- Test operation.

Interview line:

> A custom connector packages an API contract into reusable low-code actions. It improves consistency, reuse, security, and maintainability compared with repeated raw HTTP actions.

## File Reader and Scheduler Pattern

Scenario: Every hour, read files from a folder, filter `.raml`, `.yaml`, `.yml`, `.json`, or `.xml`, then process each file.

Power Automate flow:

1. Trigger: Recurrence every hour.
2. Action: List files in folder from SharePoint, OneDrive, SFTP, or Azure Blob.
3. Action: Filter array where file name ends with `.raml`, `.yaml`, `.yml`, `.json`, or `.xml`.
4. Action: Apply to each file.
5. Action: Get file content.
6. Action: Process based on extension.
7. Action: Move file to archive/success or error folder.
8. Action: Log file name, timestamp, status, and error message.

Design tips:

- Use archive folders so files are not processed twice.
- Add a correlation ID per run.
- Validate file type and content before processing.
- Use idempotency keys, such as file name + hash + timestamp.
- Put failed files in an error folder with reason.

Pseudo-condition:

```text
endsWith(fileName, '.raml')
or endsWith(fileName, '.yaml')
or endsWith(fileName, '.yml')
or endsWith(fileName, '.json')
or endsWith(fileName, '.xml')
```

## Azure Event Hubs With Kafka

Azure Event Hubs can expose an Apache Kafka endpoint. This lets Kafka clients send and receive events using Kafka protocol without managing a Kafka cluster.

Concept mapping:

| Kafka concept | Event Hubs concept |
|---|---|
| Cluster | Namespace |
| Topic | Event hub |
| Partition | Partition |
| Consumer group | Consumer group |
| Offset | Offset |

Use Event Hubs/Kafka when:

- You need high-throughput event ingestion.
- You process telemetry, clickstream, logs, IoT, or event streams.
- Consumers read independently from offsets.
- You need partitioned ordered streams.

Important points:

- Event Hubs is fully managed.
- Kafka clients often need configuration changes rather than application rewrite.
- Delivery is commonly at-least-once, so consumers must handle duplicates.
- Partitions affect parallelism and ordering.
- Consumer groups let multiple independent applications read the same event stream.

Interview line:

> I would use Event Hubs/Kafka for event streaming and high-throughput ingestion where consumers read from partitions and offsets. I would make consumers idempotent because duplicate events can happen.

## Azure Service Bus

Azure Service Bus is a fully managed enterprise message broker with queues and publish-subscribe topics.

Use Service Bus when:

- You need reliable business messaging.
- You want to decouple producer and consumer.
- You need competing consumers.
- You need dead-letter queues.
- You need scheduled delivery, sessions, FIFO-like ordering, or transactions.
- You need topic subscriptions with filters.

Core concepts:

- Queue: point-to-point messaging.
- Topic: publish-subscribe messaging.
- Subscription: independent receiver under a topic.
- DLQ: stores messages that cannot be delivered or processed.
- Lock/settlement: receiver completes, abandons, dead-letters, or defers a message.
- Sessions: ordering/grouping for related messages.

Interview line:

> I would use Service Bus for reliable commands and business workflows, especially when I need queues, DLQ, duplicate detection, ordering with sessions, or topic subscriptions with filters.

## Event Hubs/Kafka vs Service Bus

| Requirement | Better fit |
|---|---|
| Telemetry, logs, clickstream | Event Hubs/Kafka |
| High-throughput append-only stream | Event Hubs/Kafka |
| Consumers track offsets | Event Hubs/Kafka |
| Business command, such as create invoice | Service Bus |
| Need DLQ and message settlement | Service Bus |
| Need competing workers for jobs | Service Bus |
| Need topic subscription filters | Service Bus |
| Need replay from stream retention | Event Hubs/Kafka |
| Need workflow reliability | Service Bus |

Short answer:

> Event Hubs/Kafka is stream-oriented. Service Bus is message/workflow-oriented.

## Synchronous API vs Asynchronous Messaging

Use synchronous HTTP API when:

- Caller needs immediate answer.
- Operation is short.
- Failure can be returned directly.
- User is waiting.

Use asynchronous messaging when:

- Work is long-running.
- Systems should be decoupled.
- Traffic spikes need buffering.
- You need retries independent of caller.
- You need eventual consistency.

Example:

- Sync: `GET /friends/f-100` returns the friend immediately.
- Async: `POST /friend-import-jobs` returns `202 Accepted`, then worker processes messages from Service Bus.

## Reliability Patterns

### Retry

Retry transient failures:

- Timeout
- 408
- 429
- 500
- 502
- 503
- 504

Do not blindly retry:

- 400 invalid request
- 401 invalid/missing auth
- 403 no permission
- 404 resource not found, unless eventual consistency is expected
- 422 business validation error

### Idempotency

Problem: Retry can create duplicates.

Solutions:

- Use PUT with stable resource ID.
- Use idempotency key header.
- Store processed message IDs.
- Use unique constraints in target system.
- Upsert instead of insert.

Example:

```http
POST /friends
Idempotency-Key: import-20260706-f-100
```

### Dead-Letter Queue

Use DLQ when a message cannot be processed after retries.

Store:

- Message ID.
- Correlation ID.
- Original payload.
- Error reason.
- Attempt count.
- Timestamp.

### Correlation ID

Add a correlation ID across systems:

```http
Correlation-Id: 8b7f0a1
```

Use it in logs so you can trace one transaction across API gateway, flow, queue, function, and target system.

## Security Essentials

Authentication:

- API key: simple, but less secure if not protected.
- Basic auth: username/password, only over HTTPS.
- OAuth 2.0 client credentials: machine-to-machine integrations.
- OAuth authorization code: user delegated access.
- Managed identity: Azure service identity without storing secrets.
- SAS token: scoped access token used by some Azure services.

Authorization:

- Principle of least privilege.
- Separate read and write permissions.
- Rotate secrets.
- Store secrets in secure vaults or managed connections.
- Do not log tokens or passwords.

Interview line:

> For production integrations, I prefer OAuth 2.0 or managed identity where possible, HTTPS/TLS, least privilege, secret rotation, and no secrets in logs or code.

## Pagination, Filtering, and Sorting

Common query parameters:

```http
GET /friends?page=2&pageSize=100
GET /friends?limit=100&offset=200
GET /friends?updatedAfter=2026-07-06T00:00:00Z
GET /friends?sort=updatedAt&order=desc
```

Integration tips:

- Always handle pagination.
- Use incremental load with `updatedAfter` where possible.
- Store last successful sync timestamp.
- Watch for time zones.
- Avoid missing records updated during the sync by using a high-water mark strategy.

## API Integration System Design Example

Question: "Design an integration that syncs Friends API data into CRM every hour."

Answer structure:

1. Requirements:
   - Source: Friends API.
   - Target: CRM/Dataverse/SQL.
   - Frequency: hourly.
   - Data: active friends updated since last run.
   - SLA: define acceptable delay.

2. Flow:
   - Scheduled trigger.
   - Read last successful sync time.
   - Call `GET /friends?updatedAfter=<timestamp>&page=1`.
   - Parse JSON.
   - Loop pages.
   - Validate records.
   - Upsert into target using friend ID.
   - Log success/failure.
   - Update sync timestamp only after successful completion.

3. Reliability:
   - Retry transient errors.
   - Respect 429 rate limits.
   - Use idempotent upsert.
   - Store failed records separately.
   - Alert on repeated failures.

4. Security:
   - OAuth/client credentials or managed identity.
   - Store secrets securely.
   - Use HTTPS.

5. Observability:
   - Correlation ID.
   - Count records read, inserted, updated, failed.
   - Flow run history.
   - Alert on failure or abnormal volume.

6. Scale:
   - If volume grows, put records onto Service Bus and process with workers.
   - If it becomes event stream data, use Event Hubs/Kafka.

Short interview answer:

> I would build a scheduled integration that reads changed friends from the API using pagination and an `updatedAfter` filter, parses the JSON, validates each record, and upserts into the target using friend ID as the idempotency key. I would add retries for transient errors, handle 429 with backoff, log correlation IDs and counts, and send failed records to an error store or DLQ. If the volume grows, I would decouple with Service Bus.

## Low-Code Interview Points

Low-code does not mean no engineering. You still need:

- Good API contracts.
- Secure connections.
- Environment variables.
- Proper error handling.
- ALM/deployment strategy.
- Monitoring.
- DLP policies.
- Versioning.
- Testing.

Power Automate best practices:

- Keep flows small and readable.
- Use child flows for reuse.
- Name actions clearly.
- Use Scopes for Try/Catch/Finally.
- Avoid hardcoding environment-specific URLs/secrets.
- Avoid unnecessary loops if Filter array or Select can do it.
- Control concurrency when calling rate-limited APIs.
- Log enough detail to troubleshoot, but never log secrets.

## Common Interview Questions And Strong Answers

### 1. What is an API?

An API is a contract that lets one system use functionality or data from another system. In HTTP APIs, the contract includes endpoints, methods, parameters, headers, payload schemas, responses, and errors.

### 2. What is API integration?

API integration connects two or more systems by sending requests, receiving responses, transforming data, and handling reliability, security, and monitoring.

### 3. What is the difference between REST and SOAP?

REST commonly uses HTTP resources, methods, and JSON. SOAP is XML-based, has a formal envelope, often uses WSDL, and is common in enterprise/legacy systems. REST is usually simpler for web APIs, while SOAP has strict standards for contracts and enterprise features.

### 4. What is a path parameter?

A path parameter identifies a resource in the URL path, such as `/friends/{friendId}`.

### 5. What is a query parameter?

A query parameter modifies the request, such as filtering, searching, sorting, or pagination: `/friends?city=Lahore&page=2`.

### 6. Difference between PUT and PATCH?

PUT usually replaces the full resource. PATCH updates specific fields.

### 7. What does 201 mean?

201 Created means the resource was created successfully.

### 8. What does 202 mean?

202 Accepted means the request was accepted, but processing may continue asynchronously.

### 9. What does 401 vs 403 mean?

401 means authentication is missing or invalid. 403 means the caller is authenticated but not allowed.

### 10. What does 409 mean?

409 Conflict means the request conflicts with current state, such as duplicate resource or version conflict.

### 11. What does 429 mean?

429 Too Many Requests means rate limit exceeded. Back off, respect `Retry-After`, and reduce concurrency.

### 12. How do you handle API failures?

Classify errors as transient or permanent, retry transient errors with backoff, do not retry validation errors blindly, log details with correlation ID, alert, and store failed records for replay.

### 13. How do you prevent duplicate records?

Use idempotency keys, upserts, unique constraints, stable external IDs, and processed message tracking.

### 14. What is JSON?

JSON is a lightweight data format using objects, arrays, strings, numbers, booleans, and null. It is widely used for REST API payloads.

### 15. What is XML?

XML is a markup format with elements, attributes, namespaces, and schemas. It is common in enterprise and legacy integrations.

### 16. What is XSLT?

XSLT transforms XML from one structure into another structure. XPath selects nodes inside XML.

### 17. What is YAML?

YAML is a human-readable data format often used for configuration and API specs. It is indentation-sensitive.

### 18. What is RAML?

RAML is a YAML-based language for modeling REST APIs, including resources, methods, parameters, bodies, responses, types, and security.

### 19. What is OpenAPI?

OpenAPI is a standard API description format for HTTP APIs. It helps generate documentation, clients, server stubs, tests, and custom connectors.

### 20. How do you parse JSON in Power Automate?

Use the Parse JSON action with a schema, then use dynamic content or expressions like `body('Parse_JSON')?['id']`.

### 21. How do you call an API in Power Automate?

Use the HTTP action, set method, URI, headers, authentication, and optional body. Then handle the response status code and parse the body.

### 22. What is a custom connector?

A custom connector wraps an external API as reusable Power Automate actions with defined authentication, requests, and responses.

### 23. What is a scheduled flow?

A scheduled flow starts on a recurrence, such as every hour or every day.

### 24. What is an automated flow?

An automated flow starts from an event, such as a file created, item modified, or email received.

### 25. What is an HTTP-triggered flow?

A flow that starts when it receives an HTTP request. It can expose a URL and accept a JSON payload.

### 26. How do you process files on a schedule?

Use a recurrence trigger, list files in a folder, filter files by extension or metadata, get file content, process each file, then archive success and error files separately.

### 27. When would you use Azure Service Bus?

Use Service Bus for reliable enterprise messaging, queues, topics, subscriptions, DLQ, sessions, and decoupled business workflows.

### 28. When would you use Kafka or Event Hubs?

Use Kafka/Event Hubs for high-throughput event streaming, telemetry, logs, clickstream, and consumers reading from partitioned streams.

### 29. What is a dead-letter queue?

A DLQ stores messages that cannot be delivered or processed after retries, so they can be inspected, fixed, or replayed.

### 30. What is a consumer group?

A consumer group lets a group of consumers share reading from a stream. Different consumer groups can independently read the same stream.

### 31. What is at-least-once delivery?

The system tries to deliver messages at least once, but duplicates can happen. Consumers must be idempotent.

### 32. What is exactly-once processing?

It means each business effect happens once. In real integrations, this usually requires idempotency, transactions, deduplication, and careful design rather than only relying on the broker.

### 33. How do you monitor an integration?

Track success/failure counts, latency, retries, dead-letter count, status codes, correlation IDs, and alerts.

### 34. How do you secure API credentials?

Use managed identity or OAuth where possible, store secrets securely, rotate keys, avoid logging secrets, and apply least privilege.

### 35. How do you handle pagination?

Loop through pages using next link, page number, offset, or continuation token until no more records remain.

### 36. How do you handle schema changes?

Version APIs, validate payloads, make parsers tolerant to new optional fields, monitor failures, and coordinate breaking changes.

### 37. What is content negotiation?

The client uses headers like `Accept` and `Content-Type` to tell the server what format it sends and expects back.

### 38. What is a webhook?

A webhook is an HTTP callback where one system sends events to another when something happens.

### 39. Webhook vs polling?

Webhook is event-driven and faster. Polling checks on a schedule and is simpler when the source cannot push events.

### 40. How would you troubleshoot a failing API flow?

Check trigger input, request URL, auth token, headers, payload, status code, response body, retry history, correlation ID, and downstream system logs.

## Mini Hands-On Practice

### Practice 1: Classify Parameters

URL:

```http
GET /customers/42/orders?status=open&page=3
```

Answer:

- `42` is a path parameter.
- `status=open` is a query parameter.
- `page=3` is a query parameter.

### Practice 2: Pick Status Code

Create friend succeeded:

```text
201 Created
```

Delete friend succeeded with no body:

```text
204 No Content
```

Missing token:

```text
401 Unauthorized
```

Valid token but no permission:

```text
403 Forbidden
```

Rate limited:

```text
429 Too Many Requests
```

### Practice 3: Transform JSON

Input:

```json
{
  "firstName": "Ali",
  "lastName": "Naqvi",
  "email": "ali@example.com"
}
```

Output:

```json
{
  "fullName": "Ali Naqvi",
  "emailAddress": "ali@example.com"
}
```

Power Automate expressions:

```text
concat(body('Parse_JSON')?['firstName'], ' ', body('Parse_JSON')?['lastName'])
body('Parse_JSON')?['email']
```

### Practice 4: Design Error Handling

Question: "What if the Friends API is down?"

Answer:

> I would retry transient errors with backoff, fail gracefully after max attempts, log the correlation ID and response details, alert the support channel, and keep the source records available for replay. If processing is asynchronous, I would use a queue and DLQ so messages are not lost.

## Final Cheat Sheet

Say these phrases naturally:

- "I start from the API contract."
- "Path parameters identify resources; query parameters filter or control the request."
- "I treat 4xx as caller/request issues and 5xx as server/downstream issues, with exceptions like 429."
- "Retries require idempotency."
- "For 429, I respect Retry-After and reduce concurrency."
- "For Power Automate, I use Parse JSON, Scopes, Configure run after, and clear logging."
- "For reliable business messages, I use Service Bus."
- "For high-throughput event streams, I use Event Hubs/Kafka."
- "I use correlation IDs to trace one transaction across systems."
- "I avoid logging secrets and prefer managed identity or OAuth where possible."

## Clarifying Questions To Ask The Interviewer

Use these during system design questions:

- What is the source system and target system?
- Is this real-time, scheduled, or event-driven?
- What is the expected volume and peak rate?
- What is the required SLA or acceptable delay?
- What authentication method is required?
- Is the API contract OpenAPI, RAML, WSDL, or informal documentation?
- What errors should be retried?
- Are duplicate records acceptable, or do we need strict idempotency?
- Is there an existing monitoring/logging standard?
- Are there compliance or DLP restrictions?

## Sources For Further Review

- Azure Event Hubs for Apache Kafka overview: https://learn.microsoft.com/en-us/azure/event-hubs/azure-event-hubs-apache-kafka-overview
- Azure Service Bus overview: https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-messaging-overview
- Power Automate cloud flow basics: https://learn.microsoft.com/en-us/power-automate/get-started-logic-flow
- Power Automate custom connectors: https://learn.microsoft.com/en-us/connectors/custom-connectors/
- HTTP status code registry: https://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml
- OpenAPI Specification: https://spec.openapis.org/oas/latest.html
- YAML 1.2.2 specification: https://yaml.org/spec/1.2.2/
- RAML 1.0 specification: https://github.com/raml-org/raml-spec/blob/master/versions/raml-10/raml-10.md
- XML 1.0 specification: https://www.w3.org/TR/xml/
- XSLT specification: https://www.w3.org/TR/xslt20/
