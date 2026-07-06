# Enterprise API Integration Interview Prep

Prepared on: 2026-07-06  
Interview focus: API integration, C#, JSON/XML/XSLT, YAML/RAML/OpenAPI, query/path parameters, HTTP status codes, Azure Kafka/Event Hubs, Azure Service Bus, RabbitMQ, low-code/Power Automate, file schedulers, and enterprise system design.

## Read This First

This guide is rewritten around one enterprise shipment and pickup company system because that is the best way to connect all interview topics into one story.

Assumptions:

- The company handles shipment booking, pickup scheduling, driver assignment, package tracking, partner integrations, invoicing, and customer notifications.
- Some partners call APIs directly with JSON.
- Some partners send XML/CSV/JSON files by SFTP, SharePoint, OneDrive, or blob storage.
- Internal operations teams use low-code tools like Power Automate.
- High-volume GPS/tracking events are streamed.
- Business commands like "create shipment", "schedule pickup", and "send notification" are queued reliably.
- C# is the main coding language for examples.

One strong interview line:

> API integration is not only calling an endpoint. It includes API contract design, authentication, request/response handling, data transformation, asynchronous messaging, retries, idempotency, monitoring, and support operations.

## Complete System Scenario

Build an enterprise shipment and pickup platform.

Business capabilities:

- Customers create shipments.
- Customers schedule pickups.
- Drivers receive route assignments.
- Warehouses scan packages.
- Partners send bulk shipment files.
- Customers track packages.
- Operations teams handle exceptions.
- Finance receives billing events.
- Notifications are sent by email, SMS, or Teams.

Systems involved:

- Public Shipment API
- Partner Integration API
- Internal Operations Portal
- Power Automate flows
- File ingestion scheduler
- Azure Service Bus
- Azure Event Hubs with Kafka endpoint
- RabbitMQ for on-premises or partner messaging
- SQL database or Cosmos DB
- Blob storage or data lake
- API Management gateway
- Identity provider such as Microsoft Entra ID
- Monitoring through Application Insights, Log Analytics, dashboards, and alerts

## High-Level Architecture

```text
Customers / Partners / Mobile App
        |
        v
Azure API Management
        |
        v
Shipment Integration API (.NET/C#)
        |
        +--> SQL/Cosmos DB for operational state
        |
        +--> Azure Service Bus queues/topics for business commands
        |
        +--> Event Hubs/Kafka for high-volume tracking events
        |
        +--> Blob/Data Lake for raw files and audit payloads
        |
        +--> Power Automate for approvals, alerts, and operations workflows
        |
        +--> RabbitMQ bridge for on-prem warehouse/partner systems
```

Main flows:

- API flow: partner sends JSON to `POST /shipments`.
- File flow: partner drops XML/CSV file, scheduler reads it, transforms it, validates it, and creates shipments.
- Message flow: API publishes `ShipmentCreated` to Service Bus so downstream workers can process labels, billing, notifications, and pickup planning.
- Stream flow: driver mobile app publishes location/tracking scans to Event Hubs/Kafka.
- Low-code flow: Power Automate watches exceptions and sends approval/notification workflows.

## End-To-End Shipment Flow

1. Customer calls `POST /shipments` with JSON.
2. API Management validates subscription, OAuth/JWT, rate limits, and forwards request.
3. Shipment API validates payload and creates an idempotency key.
4. API saves shipment state to database.
5. API publishes `ShipmentCreated` to Service Bus topic.
6. Label worker receives message and creates label.
7. Pickup worker schedules pickup window.
8. Notification worker sends confirmation.
9. Driver app publishes scan/location events to Event Hubs/Kafka.
10. Operations team sees exceptions through dashboard and Power Automate alerts.
11. Failed messages go to DLQ.
12. All logs include `Correlation-Id`.

Interview answer:

> I would keep the API synchronous only for request validation and initial creation. Longer work like labels, billing, route planning, and notifications should be asynchronous through Service Bus. High-volume tracking or GPS events should go to Event Hubs/Kafka. File-based partner integration should go through a scheduler that archives raw files, transforms XML/CSV/JSON into a canonical model, validates, and publishes commands into the same pipeline.

## Data Format Basics

### JSON

JSON is a lightweight data interchange format. It is common for REST APIs.

Shipment JSON example:

```json
{
  "shipmentId": "SHP-1001",
  "customerId": "CUST-9",
  "serviceLevel": "EXPRESS",
  "pickup": {
    "date": "2026-07-07",
    "windowStart": "09:00",
    "windowEnd": "12:00"
  },
  "packages": [
    {
      "packageId": "PKG-1",
      "weightKg": 2.5,
      "hazmat": false
    }
  ]
}
```

When to use:

- REST APIs
- Mobile apps
- Web apps
- Event payloads
- Power Automate HTTP actions
- Service Bus message payloads

Strengths:

- Lightweight
- Easy to parse in JavaScript, C#, Python, Power Automate
- Natural fit for APIs

Weaknesses:

- No comments
- Less expressive than XML for mixed content and namespaces
- Schema validation requires JSON Schema or OpenAPI schema

### XML

XML is a markup language with elements, attributes, namespaces, and schemas. It is common in enterprise, legacy, SOAP, EDI-style, and partner integrations.

Shipment XML example:

```xml
<Shipment id="SHP-1001">
  <CustomerId>CUST-9</CustomerId>
  <ServiceLevel>EXPRESS</ServiceLevel>
  <Pickup>
    <Date>2026-07-07</Date>
    <WindowStart>09:00</WindowStart>
    <WindowEnd>12:00</WindowEnd>
  </Pickup>
  <Packages>
    <Package id="PKG-1">
      <WeightKg>2.5</WeightKg>
      <Hazmat>false</Hazmat>
    </Package>
  </Packages>
</Shipment>
```

When to use:

- SOAP services
- Legacy enterprise systems
- Partner files
- Systems requiring XSD validation
- Documents with namespaces

Strengths:

- Strong schema validation with XSD
- Supports namespaces
- Good for document-style payloads
- Mature transformation tooling through XPath/XSLT

Weaknesses:

- Verbose
- More complex parsing
- Namespace handling can confuse developers

### XSLT

XSLT is not a data format like JSON or XML. XSLT is a transformation language for converting XML into another XML shape, HTML, text, or sometimes JSON-like output.

Use XSLT when:

- A partner sends XML in one shape and your system needs a different XML shape.
- You need repeatable XML mapping rules.
- You need to convert legacy XML into canonical XML before converting to JSON.

Example: partner XML to canonical shipment XML.

Input:

```xml
<PartnerShipment>
  <Ref>SHP-1001</Ref>
  <Cust>CUST-9</Cust>
  <Svc>EXPRESS</Svc>
</PartnerShipment>
```

XSLT:

```xml
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:template match="/PartnerShipment">
    <Shipment>
      <ShipmentId><xsl:value-of select="Ref"/></ShipmentId>
      <CustomerId><xsl:value-of select="Cust"/></CustomerId>
      <ServiceLevel><xsl:value-of select="Svc"/></ServiceLevel>
    </Shipment>
  </xsl:template>
</xsl:stylesheet>
```

Output:

```xml
<Shipment>
  <ShipmentId>SHP-1001</ShipmentId>
  <CustomerId>CUST-9</CustomerId>
  <ServiceLevel>EXPRESS</ServiceLevel>
</Shipment>
```

## JSON vs XML vs XSLT

| Topic | JSON | XML | XSLT |
|---|---|---|---|
| What it is | Data format | Markup/data format | XML transformation language |
| Common use | REST APIs, events | SOAP, legacy, partner files | Transform XML |
| Shape | Objects and arrays | Elements and attributes | Rules/templates |
| Validation | JSON Schema, OpenAPI schema | XSD | XSLT processor validates transform syntax |
| Verbosity | Low | High | High |
| Namespaces | No native namespace system | Strong namespace support | Works with XML namespaces |
| Interview trap | JSON is not JavaScript object in memory; it is text | XML is not HTML | XSLT is not a payload format |

Strong answer:

> JSON and XML are data formats. XSLT is a transformation language used mainly for XML. In modern REST APIs I usually use JSON. In legacy or partner integrations I may receive XML, validate it with XSD, transform it with XSLT, and then map it into the canonical JSON model used internally.

## YAML, RAML, OpenAPI, And Related Formats

### YAML

YAML is a human-readable data serialization format. It is often used for configuration and API definitions.

Example:

```yaml
shipment:
  shipmentId: SHP-1001
  serviceLevel: EXPRESS
  packages:
    - packageId: PKG-1
      weightKg: 2.5
      hazmat: false
```

Common YAML mistakes:

- Bad indentation
- Mixing tabs and spaces
- Duplicate keys
- Unquoted values that accidentally become booleans/dates
- Thinking YAML is an API spec by itself

### RAML

RAML means RESTful API Modeling Language. It is YAML-based and describes REST APIs.

RAML shipment API example:

```yaml
#%RAML 1.0
title: Shipment API
version: v1
baseUri: https://api.shipping.example.com/{version}
mediaType: application/json

types:
  Shipment:
    type: object
    properties:
      shipmentId: string
      customerId: string
      serviceLevel: string

/shipments:
  get:
    queryParameters:
      status?:
        type: string
      fromDate?:
        type: date-only
    responses:
      200:
        body:
          application/json:
            type: Shipment[]
  post:
    body:
      application/json:
        type: Shipment
    responses:
      201:
        body:
          application/json:
            type: Shipment

/shipments/{shipmentId}:
  uriParameters:
    shipmentId:
      type: string
  get:
    responses:
      200:
        body:
          application/json:
            type: Shipment
```

### OpenAPI

OpenAPI is the most common standard for HTTP API contracts. It can be written in YAML or JSON.

OpenAPI path/query example:

```yaml
openapi: 3.0.3
info:
  title: Shipment API
  version: 1.0.0
paths:
  /shipments/{shipmentId}:
    get:
      parameters:
        - name: shipmentId
          in: path
          required: true
          schema:
            type: string
        - name: includeEvents
          in: query
          required: false
          schema:
            type: boolean
      responses:
        "200":
          description: Shipment found
        "404":
          description: Shipment not found
```

## YAML vs RAML vs OpenAPI

| Topic | YAML | RAML | OpenAPI |
|---|---|---|---|
| What it is | Data serialization format | API modeling language | HTTP API description standard |
| Based on | Its own syntax | YAML | YAML or JSON |
| Purpose | Config/data | Define REST APIs | Define HTTP APIs |
| Used by | CI/CD, Kubernetes, config, specs | API design, often MuleSoft ecosystems | API docs, SDK generation, validation, gateways, custom connectors |
| Example file | `config.yml` | `api.raml` | `openapi.yml` |
| Interview trap | YAML is not automatically RAML/OpenAPI | RAML is not just random YAML | OpenAPI can be YAML or JSON |

Related things to know:

- JSON Schema: describes and validates JSON structure.
- WSDL: describes SOAP services.
- AsyncAPI: describes event-driven APIs and messaging contracts.
- Postman collection: API testing/execution collection, not the same as a formal contract.
- Swagger: older/common name often used for OpenAPI tooling.

Strong answer:

> YAML is a syntax format. RAML and OpenAPI are API specification languages that can use YAML. OpenAPI is more widely used for REST/HTTP APIs, API gateways, documentation, client generation, and Power Automate custom connectors.

## Query Parameter vs Path Parameter

Path parameter:

- Identifies a specific resource.
- Usually required.
- Part of the URL path.

Query parameter:

- Filters, sorts, searches, paginates, or controls behavior.
- Often optional.
- Appears after `?`.

Examples:

```http
GET /shipments/SHP-1001
```

`SHP-1001` is a path parameter.

```http
GET /shipments?status=IN_TRANSIT&fromDate=2026-07-01&page=2&pageSize=50
```

`status`, `fromDate`, `page`, and `pageSize` are query parameters.

Comparison:

| Question | Path parameter | Query parameter |
|---|---|---|
| Identifies resource? | Yes | Usually no |
| Used for filter? | No | Yes |
| Example | `/shipments/{shipmentId}` | `/shipments?status=DELIVERED` |
| Required? | Usually required | Often optional |
| OpenAPI location | `in: path` | `in: query` |
| RAML location | `uriParameters` | `queryParameters` |

Interview answer:

> If removing the value changes which resource I am addressing, it is probably a path parameter. If it filters or modifies a collection request, it is probably a query parameter.

## HTTP Methods

| Method | Use | Shipment example | Idempotent? |
|---|---|---|---|
| GET | Read | `GET /shipments/SHP-1001` | Yes |
| POST | Create or command | `POST /shipments` | Usually no |
| PUT | Replace full resource | `PUT /shipments/SHP-1001` | Yes |
| PATCH | Partial update | `PATCH /shipments/SHP-1001/status` | Usually yes if designed carefully |
| DELETE | Delete/cancel | `DELETE /shipments/SHP-1001` | Yes |

Idempotency:

> Idempotent means repeating the same request leads to the same final result. It matters because retries can happen after timeouts or network failures.

## HTTP Status Codes

Status code families:

| Family | Meaning |
|---|---|
| 1xx | Informational |
| 2xx | Success |
| 3xx | Redirection |
| 4xx | Client/request problem |
| 5xx | Server/downstream problem |

Common codes:

| Code | Meaning | Shipment/API action |
|---|---|---|
| 200 | OK | Return shipment |
| 201 | Created | Shipment created |
| 202 | Accepted | Pickup accepted for async processing |
| 204 | No Content | Cancel succeeded, no body |
| 301/308 | Permanent redirect | Client should use new URL |
| 304 | Not Modified | Cached copy still valid |
| 400 | Bad Request | Invalid JSON or missing required field |
| 401 | Unauthorized | Missing/expired token |
| 403 | Forbidden | Authenticated but not allowed |
| 404 | Not Found | Shipment not found |
| 405 | Method Not Allowed | Used POST on GET-only endpoint |
| 409 | Conflict | Duplicate shipment or invalid state transition |
| 412 | Precondition Failed | ETag/version mismatch |
| 415 | Unsupported Media Type | Sent XML to JSON-only endpoint |
| 422 | Unprocessable Content | Business validation failed |
| 429 | Too Many Requests | Rate limit hit |
| 500 | Internal Server Error | Unexpected server error |
| 502 | Bad Gateway | API gateway/downstream error |
| 503 | Service Unavailable | Service temporarily unavailable |
| 504 | Gateway Timeout | Downstream timed out |

Retry rule:

- Retry: 408, 429, 500, 502, 503, 504.
- Do not blindly retry: 400, 401, 403, 404, 409, 422.
- For 429, respect `Retry-After`.
- For POST retries, use an idempotency key.

Example error response:

```json
{
  "errorCode": "SHIPMENT_VALIDATION_FAILED",
  "message": "Pickup date cannot be in the past.",
  "correlationId": "corr-82b4",
  "details": [
    {
      "field": "pickup.date",
      "reason": "Date must be today or later."
    }
  ]
}
```

## C# Coding Task: Count Unique Tokens By Split And Group

Your corrected requirement:

> There is a paragraph. Count each unique item by how many times it appears. The item can be anything. This can be done by splitting based on spaces, converting to an array, and grouping.

Important: If we split by spaces, punctuation stays attached to the token.

Input:

```text
words, words ==> words frequency
```

Space-split tokens:

```text
words,
words
==>
words
frequency
```

Expected output:

```text
words,: 1
words: 2
==>: 1
frequency: 1
```

C# LINQ solution:

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

        Dictionary<string, int> counts = CountBySpaceSeparatedToken(paragraph);

        foreach (KeyValuePair<string, int> pair in counts)
        {
            Console.WriteLine($"{pair.Key}: {pair.Value}");
        }
    }

    public static Dictionary<string, int> CountBySpaceSeparatedToken(string paragraph)
    {
        return Regex.Split(paragraph.Trim(), @"\s+")
            .Where(token => token.Length > 0)
            .GroupBy(token => token)
            .ToDictionary(group => group.Key, group => group.Count());
    }
}
```

Case-insensitive version:

```csharp
public static Dictionary<string, int> CountBySpaceSeparatedTokenIgnoreCase(string paragraph)
{
    return Regex.Split(paragraph.Trim(), @"\s+")
        .Where(token => token.Length > 0)
        .GroupBy(token => token, StringComparer.OrdinalIgnoreCase)
        .ToDictionary(group => group.Key, group => group.Count(), StringComparer.OrdinalIgnoreCase);
}
```

If the interviewer wants punctuation removed:

```csharp
public static Dictionary<string, int> CountNormalizedWords(string paragraph)
{
    return Regex.Matches(paragraph.ToLowerInvariant(), @"[a-z0-9]+")
        .Cast<Match>()
        .Select(match => match.Value)
        .GroupBy(word => word)
        .ToDictionary(group => group.Key, group => group.Count());
}
```

For the same input, normalized output is:

```text
words: 3
frequency: 1
```

What to say:

> I will clarify whether punctuation should be part of the token. If the instruction says split by space and group, I keep punctuation as part of the token. If the requirement says count normalized words, I remove punctuation or tokenize with a regex.

## C# JSON Extraction Without A Provided Class

Your corrected requirement:

> JSON is provided, but the actual C# class/model is not provided. I need to write a query in C# to extract data from that JSON.

In this case, do not deserialize into a strongly typed input class. Use one of these:

- `JsonDocument` / `JsonElement` from `System.Text.Json`
- `JsonNode` / `JsonObject` from `System.Text.Json.Nodes`
- `JObject` from Newtonsoft.Json if the project already uses Newtonsoft

For interviews, `JsonDocument` is good because it is built into modern .NET.

### Complex Shipment JSON

This example covers nested objects, arrays, missing fields, nulls, numbers, booleans, dates, grouping, filtering, flattening, and projection.

```json
{
  "batchId": "BATCH-20260707-001",
  "receivedAt": "2026-07-07T08:30:00Z",
  "source": {
    "partnerId": "PARTNER-77",
    "channel": "API"
  },
  "shipments": [
    {
      "shipmentId": "SHP-1001",
      "customer": {
        "id": "CUST-9",
        "name": "Northwind Traders",
        "tier": "GOLD"
      },
      "serviceLevel": "EXPRESS",
      "status": "IN_TRANSIT",
      "pickup": {
        "stopId": "STOP-P1",
        "scheduledStart": "2026-07-07T09:00:00Z",
        "scheduledEnd": "2026-07-07T12:00:00Z",
        "address": {
          "city": "Lahore",
          "country": "PK"
        }
      },
      "delivery": {
        "stopId": "STOP-D1",
        "eta": "2026-07-08T16:00:00Z",
        "address": {
          "city": "Karachi",
          "country": "PK"
        }
      },
      "packages": [
        {
          "packageId": "PKG-1",
          "weightKg": 2.5,
          "hazmat": false
        },
        {
          "packageId": "PKG-2",
          "weightKg": 7.1,
          "hazmat": true
        }
      ],
      "events": [
        {
          "type": "PICKED_UP",
          "time": "2026-07-07T10:15:00Z"
        },
        {
          "type": "SCAN",
          "time": "2026-07-07T13:45:00Z",
          "location": "LHE-HUB"
        }
      ],
      "charges": {
        "currency": "USD",
        "base": 20.00,
        "fuelSurcharge": 3.50,
        "discount": null
      }
    },
    {
      "shipmentId": "SHP-1002",
      "customer": {
        "id": "CUST-10",
        "name": "Contoso Retail",
        "tier": "STANDARD"
      },
      "serviceLevel": "STANDARD",
      "status": "EXCEPTION",
      "pickup": {
        "stopId": "STOP-P2",
        "scheduledStart": "2026-07-07T11:00:00Z",
        "scheduledEnd": "2026-07-07T15:00:00Z",
        "address": {
          "city": "Lahore",
          "country": "PK"
        }
      },
      "delivery": {
        "stopId": "STOP-D2",
        "eta": null,
        "address": {
          "city": "Islamabad",
          "country": "PK"
        }
      },
      "packages": [
        {
          "packageId": "PKG-3",
          "weightKg": 1.2,
          "hazmat": false
        }
      ],
      "events": [
        {
          "type": "ADDRESS_EXCEPTION",
          "time": "2026-07-07T12:30:00Z",
          "reason": "Invalid postal code"
        }
      ],
      "charges": {
        "currency": "USD",
        "base": 12.00,
        "fuelSurcharge": 2.00,
        "discount": 1.00
      }
    }
  ]
}
```

### Complex LINQ Extraction Code

Goal:

- Read JSON without a C# input class.
- Extract shipment ID, customer, city, package count, total weight, hazmat flag, latest event, total charge, and exception reason.
- Filter Lahore pickups.
- Group by customer tier.
- Handle missing/null fields safely.

```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.Json;

public sealed record ShipmentSummary(
    string ShipmentId,
    string CustomerId,
    string CustomerName,
    string CustomerTier,
    string ServiceLevel,
    string Status,
    string PickupCity,
    string DeliveryCity,
    int PackageCount,
    decimal TotalWeightKg,
    bool HasHazmat,
    string LatestEventType,
    DateTimeOffset? LatestEventTime,
    decimal TotalCharge,
    string Currency,
    string? ExceptionReason);

public sealed record TierSummary(
    string CustomerTier,
    int ShipmentCount,
    int PackageCount,
    decimal TotalWeightKg,
    decimal TotalCharges,
    int ExceptionCount,
    int HazmatShipmentCount);

public static class Program
{
    public static void Main()
    {
        string json = GetSampleJson();

        List<ShipmentSummary> shipments = ExtractShipmentSummaries(json, pickupCity: "Lahore");
        List<TierSummary> tierReport = BuildTierReport(shipments);

        Console.WriteLine("Shipment summaries:");
        foreach (ShipmentSummary shipment in shipments)
        {
            Console.WriteLine(
                $"{shipment.ShipmentId} | {shipment.CustomerName} | {shipment.PickupCity} -> {shipment.DeliveryCity} | " +
                $"Packages={shipment.PackageCount} | Weight={shipment.TotalWeightKg} | Hazmat={shipment.HasHazmat} | " +
                $"Latest={shipment.LatestEventType} | Charge={shipment.Currency} {shipment.TotalCharge} | " +
                $"Exception={shipment.ExceptionReason ?? "None"}");
        }

        Console.WriteLine();
        Console.WriteLine("Tier report:");
        foreach (TierSummary tier in tierReport)
        {
            Console.WriteLine(
                $"{tier.CustomerTier} | Shipments={tier.ShipmentCount} | Packages={tier.PackageCount} | " +
                $"Weight={tier.TotalWeightKg} | Charges={tier.TotalCharges} | Exceptions={tier.ExceptionCount} | " +
                $"HazmatShipments={tier.HazmatShipmentCount}");
        }
    }

    public static List<ShipmentSummary> ExtractShipmentSummaries(string json, string pickupCity)
    {
        using JsonDocument document = JsonDocument.Parse(json);

        JsonElement root = document.RootElement;
        JsonElement shipmentsArray = GetProperty(root, "shipments");

        List<ShipmentSummary> query =
            (from shipment in EnumerateArrayOrEmpty(shipmentsArray)
             let pickup = GetProperty(shipment, "pickup")
             let delivery = GetProperty(shipment, "delivery")
             let customer = GetProperty(shipment, "customer")
             let packages = EnumerateArrayOrEmpty(GetProperty(shipment, "packages")).ToList()
             let events = EnumerateArrayOrEmpty(GetProperty(shipment, "events")).ToList()
             let charges = GetProperty(shipment, "charges")
             let latestEvent = events
                .OrderByDescending(e => GetNullableDateTimeOffset(e, "time") ?? DateTimeOffset.MinValue)
                .FirstOrDefault()
             let city = GetString(GetProperty(GetProperty(pickup, "address"), "city"))
             where string.Equals(city, pickupCity, StringComparison.OrdinalIgnoreCase)
             select new ShipmentSummary(
                 ShipmentId: GetString(GetProperty(shipment, "shipmentId")),
                 CustomerId: GetString(GetProperty(customer, "id")),
                 CustomerName: GetString(GetProperty(customer, "name")),
                 CustomerTier: GetString(GetProperty(customer, "tier")),
                 ServiceLevel: GetString(GetProperty(shipment, "serviceLevel")),
                 Status: GetString(GetProperty(shipment, "status")),
                 PickupCity: city,
                 DeliveryCity: GetString(GetProperty(GetProperty(delivery, "address"), "city")),
                 PackageCount: packages.Count,
                 TotalWeightKg: packages.Sum(package => GetDecimal(package, "weightKg")),
                 HasHazmat: packages.Any(package => GetBoolean(package, "hazmat")),
                 LatestEventType: latestEvent.ValueKind == JsonValueKind.Undefined
                    ? "NONE"
                    : GetString(GetProperty(latestEvent, "type")),
                 LatestEventTime: latestEvent.ValueKind == JsonValueKind.Undefined
                    ? null
                    : GetNullableDateTimeOffset(latestEvent, "time"),
                 TotalCharge:
                    GetDecimal(charges, "base") +
                    GetDecimal(charges, "fuelSurcharge") -
                    GetDecimal(charges, "discount"),
                 Currency: GetString(GetProperty(charges, "currency"), "USD"),
                 ExceptionReason: events
                    .Where(e => GetString(GetProperty(e, "type")).Contains("EXCEPTION", StringComparison.OrdinalIgnoreCase))
                    .Select(e => GetStringOrNull(GetProperty(e, "reason")))
                    .FirstOrDefault(reason => !string.IsNullOrWhiteSpace(reason))))
            .OrderBy(summary => summary.PickupCity)
            .ThenBy(summary => summary.ShipmentId)
            .ToList();

        return query;
    }

    public static List<TierSummary> BuildTierReport(List<ShipmentSummary> shipments)
    {
        return shipments
            .GroupBy(shipment => shipment.CustomerTier)
            .Select(group => new TierSummary(
                CustomerTier: group.Key,
                ShipmentCount: group.Count(),
                PackageCount: group.Sum(shipment => shipment.PackageCount),
                TotalWeightKg: group.Sum(shipment => shipment.TotalWeightKg),
                TotalCharges: group.Sum(shipment => shipment.TotalCharge),
                ExceptionCount: group.Count(shipment => shipment.Status == "EXCEPTION"),
                HazmatShipmentCount: group.Count(shipment => shipment.HasHazmat)))
            .OrderByDescending(summary => summary.ShipmentCount)
            .ToList();
    }

    private static JsonElement GetProperty(JsonElement element, string propertyName)
    {
        if (element.ValueKind == JsonValueKind.Object &&
            element.TryGetProperty(propertyName, out JsonElement value))
        {
            return value;
        }

        return default;
    }

    private static IEnumerable<JsonElement> EnumerateArrayOrEmpty(JsonElement element)
    {
        return element.ValueKind == JsonValueKind.Array
            ? element.EnumerateArray()
            : Enumerable.Empty<JsonElement>();
    }

    private static string GetString(JsonElement element, string defaultValue = "")
    {
        return element.ValueKind == JsonValueKind.String
            ? element.GetString() ?? defaultValue
            : defaultValue;
    }

    private static string? GetStringOrNull(JsonElement element)
    {
        return element.ValueKind == JsonValueKind.String
            ? element.GetString()
            : null;
    }

    private static bool GetBoolean(JsonElement element, string propertyName)
    {
        JsonElement value = GetProperty(element, propertyName);

        return value.ValueKind == JsonValueKind.True ||
               (value.ValueKind == JsonValueKind.String &&
                bool.TryParse(value.GetString(), out bool parsed) &&
                parsed);
    }

    private static decimal GetDecimal(JsonElement element, string propertyName)
    {
        JsonElement value = GetProperty(element, propertyName);

        if (value.ValueKind == JsonValueKind.Number && value.TryGetDecimal(out decimal number))
        {
            return number;
        }

        if (value.ValueKind == JsonValueKind.String &&
            decimal.TryParse(value.GetString(), out decimal parsed))
        {
            return parsed;
        }

        return 0m;
    }

    private static DateTimeOffset? GetNullableDateTimeOffset(JsonElement element, string propertyName)
    {
        JsonElement value = GetProperty(element, propertyName);

        if (value.ValueKind == JsonValueKind.String &&
            DateTimeOffset.TryParse(value.GetString(), out DateTimeOffset parsed))
        {
            return parsed;
        }

        return null;
    }

    private static string GetSampleJson()
    {
        return """
        {
          "batchId": "BATCH-20260707-001",
          "receivedAt": "2026-07-07T08:30:00Z",
          "source": {
            "partnerId": "PARTNER-77",
            "channel": "API"
          },
          "shipments": [
            {
              "shipmentId": "SHP-1001",
              "customer": {
                "id": "CUST-9",
                "name": "Northwind Traders",
                "tier": "GOLD"
              },
              "serviceLevel": "EXPRESS",
              "status": "IN_TRANSIT",
              "pickup": {
                "stopId": "STOP-P1",
                "scheduledStart": "2026-07-07T09:00:00Z",
                "scheduledEnd": "2026-07-07T12:00:00Z",
                "address": {
                  "city": "Lahore",
                  "country": "PK"
                }
              },
              "delivery": {
                "stopId": "STOP-D1",
                "eta": "2026-07-08T16:00:00Z",
                "address": {
                  "city": "Karachi",
                  "country": "PK"
                }
              },
              "packages": [
                {
                  "packageId": "PKG-1",
                  "weightKg": 2.5,
                  "hazmat": false
                },
                {
                  "packageId": "PKG-2",
                  "weightKg": 7.1,
                  "hazmat": true
                }
              ],
              "events": [
                {
                  "type": "PICKED_UP",
                  "time": "2026-07-07T10:15:00Z"
                },
                {
                  "type": "SCAN",
                  "time": "2026-07-07T13:45:00Z",
                  "location": "LHE-HUB"
                }
              ],
              "charges": {
                "currency": "USD",
                "base": 20.00,
                "fuelSurcharge": 3.50,
                "discount": null
              }
            },
            {
              "shipmentId": "SHP-1002",
              "customer": {
                "id": "CUST-10",
                "name": "Contoso Retail",
                "tier": "STANDARD"
              },
              "serviceLevel": "STANDARD",
              "status": "EXCEPTION",
              "pickup": {
                "stopId": "STOP-P2",
                "scheduledStart": "2026-07-07T11:00:00Z",
                "scheduledEnd": "2026-07-07T15:00:00Z",
                "address": {
                  "city": "Lahore",
                  "country": "PK"
                }
              },
              "delivery": {
                "stopId": "STOP-D2",
                "eta": null,
                "address": {
                  "city": "Islamabad",
                  "country": "PK"
                }
              },
              "packages": [
                {
                  "packageId": "PKG-3",
                  "weightKg": 1.2,
                  "hazmat": false
                }
              ],
              "events": [
                {
                  "type": "ADDRESS_EXCEPTION",
                  "time": "2026-07-07T12:30:00Z",
                  "reason": "Invalid postal code"
                }
              ],
              "charges": {
                "currency": "USD",
                "base": 12.00,
                "fuelSurcharge": 2.00,
                "discount": 1.00
              }
            }
          ]
        }
        """;
    }
}
```

What this covers:

- `JsonDocument.Parse(json)` when no input class exists.
- `EnumerateArray()` for arrays.
- `TryGetProperty()` to avoid crashes on missing fields.
- Null-safe string/number/date extraction.
- LINQ `from`, `let`, `where`, `select`.
- `Sum`, `Any`, `Count`, `OrderByDescending`, `GroupBy`.
- Projection into a custom output record.

Strong interview answer:

> If the class is not provided, I do not guess a model first. I parse the JSON as a document, navigate properties safely, enumerate arrays, and project only the fields I need into an output DTO or anonymous type. For production, if the JSON contract becomes stable, I prefer generated or strongly typed models.

## Friends API Practice

Use the Friends API as a small version of the same ideas.

Friend resource:

```json
{
  "friendId": "FR-100",
  "firstName": "Sara",
  "lastName": "Ahmed",
  "email": "sara@example.com",
  "city": "Lahore",
  "active": true
}
```

Endpoints:

| Endpoint | Method | Purpose |
|---|---|---|
| `/friends` | GET | List friends |
| `/friends?city=Lahore&active=true` | GET | Filter friends |
| `/friends/{friendId}` | GET | Get one friend |
| `/friends` | POST | Create friend |
| `/friends/{friendId}` | PUT | Replace friend |
| `/friends/{friendId}` | PATCH | Partial update |
| `/friends/{friendId}` | DELETE | Delete friend |

C# API call:

```csharp
using System;
using System.Net;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Net.Http.Json;
using System.Threading.Tasks;

public sealed record CreateFriendRequest(string FirstName, string LastName, string Email, string City);
public sealed record Friend(string FriendId, string FirstName, string LastName, string Email, string City, bool Active);

public static class Program
{
    public static async Task Main()
    {
        using var http = new HttpClient();
        http.BaseAddress = new Uri("https://api.example.com/");
        http.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", "replace-token");

        string city = Uri.EscapeDataString("Lahore");
        Friend[] friends = await http.GetFromJsonAsync<Friend[]>($"friends?city={city}&active=true")
            ?? Array.Empty<Friend>();

        using HttpResponseMessage response = await http.PostAsJsonAsync(
            "friends",
            new CreateFriendRequest("Sara", "Ahmed", "sara@example.com", "Lahore"));

        if (response.StatusCode == HttpStatusCode.Created)
        {
            Friend? created = await response.Content.ReadFromJsonAsync<Friend>();
            Console.WriteLine($"Created: {created?.FriendId}");
        }
        else
        {
            string error = await response.Content.ReadAsStringAsync();
            Console.WriteLine($"Failed: {(int)response.StatusCode} {error}");
        }
    }
}
```

## Azure Event Hubs Kafka, Azure Service Bus, RabbitMQ

### Azure Event Hubs With Kafka Endpoint

Azure Event Hubs is a managed event streaming platform. It can expose a Kafka endpoint so Kafka clients can publish/consume events using Kafka protocol without operating a Kafka cluster.

Use it for:

- GPS tracking events
- Driver mobile telemetry
- Package scan streams
- Clickstream/log ingestion
- High-throughput event pipelines
- Analytics consumers reading from offsets

Key concepts:

| Kafka concept | Event Hubs concept |
|---|---|
| Cluster | Namespace |
| Topic | Event hub |
| Partition | Partition |
| Consumer group | Consumer group |
| Offset | Offset |

Shipment example:

```json
{
  "eventType": "PACKAGE_SCANNED",
  "shipmentId": "SHP-1001",
  "packageId": "PKG-1",
  "scanLocation": "LHE-HUB",
  "eventTime": "2026-07-07T13:45:00Z"
}
```

Interview answer:

> I use Event Hubs/Kafka for high-volume append-only event streams where consumers process independently from partitions and offsets.

### Azure Service Bus

Azure Service Bus is an enterprise message broker with queues and pub/sub topics.

Use it for:

- Business commands
- Reliable workflows
- Pickup scheduling jobs
- Label generation jobs
- Billing events
- Notifications
- Dead-letter handling
- Duplicate detection
- Sessions/order per shipment

Shipment queues/topics:

```text
Topic: shipment-events
  Subscription: billing
  Subscription: notification
  Subscription: route-planning

Queue: pickup-scheduling
Queue: label-generation
Queue: customer-notifications
DLQ: built into queues/subscriptions
```

Message example:

```json
{
  "messageId": "SHP-1001:ShipmentCreated",
  "correlationId": "corr-82b4",
  "eventType": "ShipmentCreated",
  "shipmentId": "SHP-1001",
  "createdAt": "2026-07-07T08:31:00Z"
}
```

Interview answer:

> I use Service Bus for reliable business messaging when I need queues, topics, subscriptions, DLQ, duplicate detection, message settlement, scheduled delivery, or ordered processing with sessions.

### RabbitMQ

RabbitMQ is a message broker commonly used with AMQP 0-9-1. It has exchanges, queues, bindings, routing keys, acknowledgements, and dead-letter patterns.

Use it for:

- On-premises systems
- Existing enterprise systems already using RabbitMQ
- Low-latency task queues
- Routing with direct, fanout, topic, and headers exchanges
- Internal microservice messaging when the team operates RabbitMQ

RabbitMQ concepts:

- Producer publishes to exchange.
- Exchange routes to queues using bindings.
- Consumer reads from queue.
- Ack means message processed.
- Nack/reject can requeue or dead-letter.
- Durable queues and persistent messages are needed for reliability.

Shipment routing example:

```text
Exchange: shipment.topic
Routing key: shipment.created.express
Queue: express-label-worker
Binding: shipment.created.*
```

Interview answer:

> I use RabbitMQ when the platform already has RabbitMQ, when I need exchange-based routing, or when working in on-prem/hybrid environments. In Azure-native enterprise workflows, I usually choose Service Bus unless RabbitMQ is already a standard.

## When To Use Kafka/Event Hubs vs Service Bus vs RabbitMQ

| Requirement | Best fit |
|---|---|
| High-volume telemetry/events | Event Hubs/Kafka |
| GPS tracking stream | Event Hubs/Kafka |
| Replay event stream from offset | Event Hubs/Kafka |
| Business command/job | Service Bus or RabbitMQ |
| Enterprise cloud-native queue | Azure Service Bus |
| DLQ and duplicate detection managed by Azure | Azure Service Bus |
| Ordered workflow per shipment | Service Bus sessions |
| Existing on-prem broker | RabbitMQ |
| Exchange/routing-key patterns | RabbitMQ |
| Pub/sub for business events | Service Bus topics or RabbitMQ topic exchange |
| Analytics stream | Event Hubs/Kafka |

Short answer:

> Kafka/Event Hubs is stream-oriented. Service Bus is enterprise workflow/message-oriented. RabbitMQ is broker/routing-oriented and often strong for on-prem or existing AMQP-style systems.

## Synchronous API vs Asynchronous Messaging

Use synchronous HTTP API when:

- The client needs an immediate answer.
- The operation is short.
- The user is waiting.
- Example: `GET /shipments/SHP-1001`.

Use asynchronous messaging when:

- Work is long-running.
- Systems should be decoupled.
- Traffic spikes need buffering.
- Retries should happen without blocking the client.
- Example: label generation, notifications, billing.

Common pattern:

```http
POST /pickup-requests
```

Response:

```http
202 Accepted
Location: /pickup-requests/REQ-1001
```

Meaning:

> The API accepted the request, but actual scheduling will happen asynchronously.

## Reliability Patterns

### Idempotency

Problem: retries can create duplicate shipments.

Solution:

```http
POST /shipments
Idempotency-Key: partner-77-order-90001
```

Store the key with the result. If the same key is received again, return the original result.

### Outbox Pattern

Problem: database save succeeds but message publish fails.

Solution:

- Save business record and outgoing message in the same database transaction.
- Background publisher reads outbox table and publishes to Service Bus.
- Mark outbox message as published.

### Inbox Pattern

Problem: same message is delivered twice.

Solution:

- Store processed message IDs.
- If message ID already processed, skip side effects.

### Dead-Letter Queue

Use DLQ when:

- Message fails after max retries.
- Payload is invalid.
- Downstream system rejects permanently.

DLQ record should include:

- Original payload
- Message ID
- Correlation ID
- Error reason
- Attempt count
- Timestamp

### Retry Strategy

Retry transient errors:

- Timeout
- 408
- 429
- 500
- 502
- 503
- 504

Do not blindly retry:

- 400 bad request
- 401 unauthorized
- 403 forbidden
- 404 not found
- 422 validation error

### Circuit Breaker

If carrier API fails repeatedly:

- Stop calling it for a short time.
- Fail fast or queue requests.
- Resume after cooldown.

### Correlation ID

Every request/message/event should carry:

```text
Correlation-Id: corr-82b4
```

Use it across API logs, Service Bus messages, Event Hubs events, Power Automate runs, and database audit rows.

## Power Automate And Low-Code Flows

Power Automate cloud flow types:

- Automated flow: starts from an event.
- Instant flow: starts from a button/manual action.
- Scheduled flow: starts on recurrence.

Common actions:

- HTTP
- Parse JSON
- Condition
- Apply to each
- Filter array
- Select
- Compose
- Scope
- Terminate
- Send email/Teams message
- Create item/update item

### Shipment Exception Alert Flow

Trigger:

- Service Bus message arrives, or HTTP webhook from API, or scheduled query.

Actions:

1. Parse JSON.
2. If `status == EXCEPTION`.
3. Create Dataverse/SharePoint operations task.
4. Send Teams alert.
5. Wait for approval.
6. If approved, call Shipment API to update address or reschedule pickup.
7. Log result.

Power Automate expression examples:

```text
triggerBody()?['shipmentId']
body('Parse_JSON')?['customer']?['name']
items('Apply_to_each')?['packageId']
coalesce(body('Parse_JSON')?['delivery']?['eta'], 'No ETA')
concat('Shipment ', body('Parse_JSON')?['shipmentId'], ' has an exception')
```

### Power Automate Error Handling

Use scopes:

```text
Scope - Try
Scope - Catch
Scope - Finally
```

Configure run after:

- Catch runs when Try fails/times out.
- Finally logs regardless of success/failure.

Best practices:

- Name actions clearly.
- Use environment variables for URLs.
- Use custom connectors instead of repeated raw HTTP.
- Use retry policies carefully.
- Turn on concurrency only when target API can handle it.
- Never log secrets.
- Use DLP policies.
- Use solutions for ALM.

## Power Automate Custom Connector

Use a custom connector when Power Automate needs to call your Shipment API repeatedly.

Benefits:

- Reusable actions like `Create shipment`, `Get shipment`, `Reschedule pickup`.
- Central auth configuration.
- Better maker experience.
- Less repeated HTTP setup.
- Can be generated from OpenAPI.

Custom connector actions:

```text
CreateShipment
GetShipmentById
SearchShipments
CreatePickupRequest
UpdateShipmentException
```

Authentication:

- OAuth 2.0 / Microsoft Entra ID preferred.
- API key if simpler and acceptable.
- Basic auth only if required by legacy system and always over HTTPS.

## File Reader And Scheduler Pattern

Scenario:

Partners drop shipment files every hour.

Possible file locations:

- SFTP
- SharePoint folder
- OneDrive
- Azure Blob Storage
- Network folder through gateway

File types:

- `.json`
- `.xml`
- `.csv`
- `.yml`
- `.yaml`
- `.raml` for API specs, usually not shipment transactions

Flow:

1. Scheduled trigger runs every 15 minutes or hourly.
2. List files in inbound folder.
3. Filter files by extension and naming convention.
4. Acquire lock or move file to processing folder.
5. Read file content.
6. Validate file format.
7. Transform to canonical shipment model.
8. Publish each shipment to Service Bus or call Shipment API.
9. Move successful file to archive.
10. Move failed file to error folder.
11. Log counts and errors.

Pseudo-logic:

```text
for each file in inbound:
  if extension not in allowed list:
    move to rejected
  else:
    move to processing
    parse based on extension
    validate records
    publish commands
    move to archive or error
```

C# file scheduler sketch:

```csharp
using System;
using System.IO;
using System.Linq;

public static class FileScheduler
{
    private static readonly string[] AllowedExtensions = [".json", ".xml", ".csv"];

    public static void ProcessInboundFolder(string inboundFolder)
    {
        string[] files = Directory.GetFiles(inboundFolder);

        foreach (string file in files)
        {
            string extension = Path.GetExtension(file).ToLowerInvariant();

            if (!AllowedExtensions.Contains(extension))
            {
                MoveTo(file, "rejected");
                continue;
            }

            try
            {
                string content = File.ReadAllText(file);

                if (extension == ".xml")
                {
                    ProcessXmlShipmentFile(content);
                }
                else if (extension == ".json")
                {
                    ProcessJsonShipmentFile(content);
                }
                else if (extension == ".csv")
                {
                    ProcessCsvShipmentFile(content);
                }

                MoveTo(file, "archive");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Failed file {file}: {ex.Message}");
                MoveTo(file, "error");
            }
        }
    }

    private static void ProcessXmlShipmentFile(string content)
    {
        Console.WriteLine("Validate XML, optionally run XSLT, map to canonical model.");
    }

    private static void ProcessJsonShipmentFile(string content)
    {
        Console.WriteLine("Parse JSON, validate schema, publish shipment commands.");
    }

    private static void ProcessCsvShipmentFile(string content)
    {
        Console.WriteLine("Parse CSV rows, validate, publish shipment commands.");
    }

    private static void MoveTo(string file, string folderName)
    {
        string directory = Path.GetDirectoryName(file) ?? ".";
        string targetDirectory = Path.Combine(directory, folderName);
        Directory.CreateDirectory(targetDirectory);

        string target = Path.Combine(targetDirectory, Path.GetFileName(file));
        File.Move(file, target, overwrite: true);
    }
}
```

Interview concerns:

- Avoid processing same file twice.
- Use archive/error folders.
- Use file hash or file name as idempotency key.
- Handle partial uploads by requiring `.ready` marker files.
- Track batch ID and record counts.
- Do not update high-water mark until full success.

## API Integration Design Details

### API Gateway

Use Azure API Management or similar gateway for:

- OAuth/JWT validation
- Subscription keys
- Rate limiting
- Quotas
- Request/response transformation
- API versioning
- IP filtering
- Developer portal
- Logging

### API Versioning

Options:

```text
/v1/shipments
/v2/shipments
Accept: application/vnd.company.shipment.v2+json
```

Avoid breaking old clients without notice.

### Pagination

Examples:

```http
GET /shipments?page=2&pageSize=100
GET /shipments?limit=100&offset=200
GET /shipments?continuationToken=abc123
```

Best answer:

> For large APIs, I prefer continuation tokens because they are safer when data changes during paging.

### Filtering

```http
GET /shipments?status=IN_TRANSIT&fromDate=2026-07-01&toDate=2026-07-07
```

### Sorting

```http
GET /shipments?sort=createdAt&order=desc
```

### ETag / Optimistic Concurrency

Client reads:

```http
ETag: "v7"
```

Client updates:

```http
If-Match: "v7"
```

If another user updated first:

```http
412 Precondition Failed
```

## Security

Authentication:

- OAuth 2.0 client credentials for system-to-system.
- Authorization code flow for user delegated apps.
- Managed identity for Azure service-to-service.
- API key only for simple partner integrations.
- mTLS for high-security partner APIs.

Authorization:

- RBAC by role.
- Scopes/claims in token.
- Partner can access only its own shipments.

Secrets:

- Store in Key Vault or managed connector secrets.
- Rotate secrets.
- Never log tokens.

Network:

- HTTPS/TLS everywhere.
- Private endpoints where possible.
- IP allowlist for partner integrations.

Webhook security:

- HMAC signature header.
- Timestamp to prevent replay.
- Idempotency key.

## Monitoring And Operations

Track:

- API request count
- Latency percentiles
- 4xx/5xx rate
- Service Bus queue length
- DLQ count
- Event Hubs incoming events
- Consumer lag
- File processing success/failure count
- Power Automate failed runs
- Retry count
- Partner-specific error rate

Log fields:

```json
{
  "timestamp": "2026-07-07T08:31:00Z",
  "correlationId": "corr-82b4",
  "partnerId": "PARTNER-77",
  "shipmentId": "SHP-1001",
  "operation": "CreateShipment",
  "statusCode": 201,
  "durationMs": 142
}
```

Alerts:

- DLQ count > threshold
- 5xx rate > threshold
- Queue age > threshold
- File error folder has new file
- Partner API repeatedly returns 401/403/429/5xx

## Complete Enterprise System Design Answer

Question:

> Design an enterprise integration system for a shipment and pickup company.

Answer:

> I would expose public and partner APIs through API Management with OAuth/JWT validation, rate limiting, versioning, and logging. The .NET Shipment Integration API would handle synchronous validation, idempotency, and initial persistence. Long-running work like label generation, pickup scheduling, billing, and notifications would be decoupled through Azure Service Bus queues/topics. High-volume tracking, GPS, and scan events would go to Event Hubs with Kafka support so analytics consumers can process events independently. Partner file integration would use a scheduled ingestion flow or worker that reads files from SFTP/blob/SharePoint, archives raw input, validates JSON/XML/CSV, uses XSLT for XML transformation when needed, maps to a canonical shipment model, and publishes commands into the same Service Bus pipeline. Operations workflows and exception approvals can be handled with Power Automate using custom connectors over the Shipment API. Existing on-prem systems using RabbitMQ can be integrated through a bridge that consumes RabbitMQ messages and republishes canonical events to Azure. I would add correlation IDs, structured logs, DLQs, retries with backoff, idempotency keys, outbox/inbox patterns, dashboards, alerts, and secure secret handling through managed identity or Key Vault.

Follow-up details:

- API contract: OpenAPI for HTTP APIs, RAML if the organization uses RAML, AsyncAPI for events.
- Data formats: JSON for modern APIs, XML/XSLT for legacy partner transforms, CSV for bulk files.
- Reliability: Service Bus DLQ, duplicate detection, outbox, retry, circuit breaker.
- Security: OAuth 2.0, Entra ID, managed identity, API Management policies.
- Monitoring: Application Insights, Log Analytics, queue metrics, DLQ alerts, file processing audit.
- Deployment: CI/CD, infrastructure as code, environment-specific config.

## Other Interview Topics They May Ask

### REST vs SOAP

REST:

- Resource-based
- Commonly JSON
- Uses HTTP methods
- Simpler for web/mobile

SOAP:

- XML envelope
- WSDL contract
- Common in enterprise/legacy
- Strong formal contract

### Webhook vs Polling

Webhook:

- Source pushes event to your HTTP endpoint.
- Faster and efficient.
- Requires public/secure endpoint.

Polling:

- Your system checks source repeatedly.
- Simpler when source cannot push.
- Can waste requests and introduce delay.

### API Contract Testing

Test that provider and consumer agree on:

- Required fields
- Types
- Status codes
- Error body
- Auth requirements
- Backward compatibility

### Schema Evolution

Safe changes:

- Add optional field.
- Add new enum only if clients tolerate it.
- Add new endpoint.

Breaking changes:

- Remove field.
- Rename field.
- Change type.
- Make optional field required.

### Batching

Use batching when:

- Partner sends many shipments.
- API call overhead is high.

Watch out for:

- Partial failures.
- Per-record validation.
- Idempotency per record.

### Rate Limiting

When API returns 429:

- Respect `Retry-After`.
- Use exponential backoff.
- Reduce concurrency.
- Queue work if possible.

### CORS

CORS matters for browser apps calling APIs from another domain. It is not usually a server-to-server integration issue.

### Content-Type vs Accept

`Content-Type`:

> What I am sending.

`Accept`:

> What I want back.

Example:

```http
Content-Type: application/json
Accept: application/json
```

## Fast Mock Questions

### Explain XML, JSON, and XSLT.

JSON and XML are payload/data formats. JSON is common in REST APIs and lightweight. XML is common in legacy/enterprise integrations and supports namespaces and XSD validation. XSLT is not a data format; it transforms XML from one structure into another.

### Explain YAML and RAML.

YAML is a human-readable data serialization format. RAML is an API modeling language based on YAML. OpenAPI is another widely used API specification format and is often preferred for tooling, gateways, and custom connectors.

### Path parameter vs query parameter?

Path parameter identifies the resource: `/shipments/{shipmentId}`. Query parameter filters or modifies the request: `/shipments?status=DELIVERED&page=2`.

### How do you count unique words/tokens in C#?

Split by whitespace, group the tokens, and count each group. Clarify whether punctuation should remain part of the token.

### JSON is provided but no C# class exists. How do you extract data?

Use `JsonDocument` or `JsonNode`, navigate properties safely, enumerate arrays, and project required fields with LINQ. If the contract becomes stable, move to typed DTOs.

### When use Service Bus?

Reliable business messaging, workflow decoupling, queues/topics, DLQ, duplicate detection, and ordered processing with sessions.

### When use Kafka/Event Hubs?

High-volume event streaming like GPS, scans, telemetry, logs, and analytics pipelines where consumers read by partition and offset.

### When use RabbitMQ?

Existing RabbitMQ/on-prem systems, exchange/routing-key patterns, AMQP-style task queues, and teams already operating RabbitMQ.

### How do you design file ingestion?

Schedule or trigger on file arrival, move to processing, read content, validate, transform, publish canonical messages, archive success, move failures to error, and log batch results.

### How does Power Automate fit?

Use it for low-code workflows: approvals, alerts, exception handling, scheduled file processing, and calling APIs through HTTP actions or custom connectors.

### What makes an integration production-ready?

Authentication, authorization, validation, idempotency, retries, DLQ, monitoring, correlation IDs, versioning, contract testing, secret management, and support runbooks.

## Final One-Day Study Plan

### Hour 1

Study HTTP methods, path/query parameters, status codes, and error handling.

### Hour 2

Study JSON/XML/XSLT and YAML/RAML/OpenAPI comparisons.

### Hour 3

Practice C# token frequency and C# JSON extraction without classes.

### Hour 4

Study Service Bus vs Event Hubs/Kafka vs RabbitMQ.

### Hour 5

Study Power Automate flows, Parse JSON, HTTP action, custom connectors, and error scopes.

### Hour 6

Practice the full shipment system design answer out loud.

### Final 30 Minutes

Memorize these lines:

- "Path identifies; query filters."
- "JSON/XML are formats; XSLT transforms XML."
- "YAML is syntax; RAML/OpenAPI are API contracts."
- "Retries require idempotency."
- "Service Bus is for reliable business messaging."
- "Event Hubs/Kafka is for high-volume event streams."
- "RabbitMQ is strong for exchange-based routing and existing broker environments."
- "Power Automate is useful for low-code operational workflows, but production flows still need error handling, logging, and secure connections."
- "For JSON without a class, I use JsonDocument/JsonElement and LINQ projection."

## Sources For Review

- Azure Service Bus overview: https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-messaging-overview
- Azure Event Hubs for Apache Kafka overview: https://learn.microsoft.com/en-us/azure/event-hubs/azure-event-hubs-apache-kafka-overview
- Power Automate cloud flows overview: https://learn.microsoft.com/en-us/power-automate/overview-cloud
- Power Automate custom connectors: https://learn.microsoft.com/en-us/connectors/custom-connectors/
- RabbitMQ AMQP concepts: https://www.rabbitmq.com/tutorials/amqp-concepts
- HTTP status code registry: https://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml
- OpenAPI Specification: https://spec.openapis.org/oas/latest.html
- YAML specification: https://yaml.org/spec/1.2.2/
- RAML 1.0 specification: https://github.com/raml-org/raml-spec/blob/master/versions/raml-10/raml-10.md
- JSON RFC 8259: https://www.rfc-editor.org/rfc/rfc8259
- XML 1.0 specification: https://www.w3.org/TR/xml/
- XSLT 3.0 specification: https://www.w3.org/TR/xslt-30/
