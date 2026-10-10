$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.IO.Compression.FileSystem
Add-Type -AssemblyName System.IO.Compression
$out = 'D:\Final-Lesson-Implementation\R1\Muhammad-Awais-CV-Updated.docx'
$script:body = [Text.StringBuilder]::new()
function Para([string]$text, [string]$style = 'Normal', [bool]$bullet = $false) {
    $escaped = [Security.SecurityElement]::Escape($text)
    $num = if ($bullet) { '<w:numPr><w:ilvl w:val="0"/><w:numId w:val="1"/></w:numPr>' } else { '' }
    [void]$script:body.Append("<w:p><w:pPr><w:pStyle w:val=`"$style`"/>$num</w:pPr><w:r><w:t xml:space=`"preserve`">$escaped</w:t></w:r></w:p>")
}
function Bullet([string]$text) { Para $text 'Bullet' $true }
function Job([string]$title,[string]$org,[string]$dates) {
    Para $title 'Job'
    Para $org 'Company'
    Para $dates 'Dates'
}
Para 'Muhammad Awais' 'Title'
Para 'Full Stack and Infrastructure Engineer' 'Subtitle'
Para 'Dubai, United Arab Emirates  |  +971 52 605 9643  |  ibneajmal77@gmail.com' 'Contact'
Para 'linkedin.com/in/muhammad-awais-ajmal  |  github.com/ibneajmal77' 'Contact'
Para 'Professional Summary' 'Heading1'
Para 'Senior Full Stack Engineer with 8+ years delivering enterprise applications, AI-powered platforms, and cloud infrastructure. Hands-on experience with Microsoft Azure, Python FastAPI, Node.js/TypeScript, and ASP.NET Core; Docker and Kubernetes; infrastructure as code; and automated deployment pipelines. Operates production services with distributed tracing, on-call incident response, rollback and recovery, and root-cause analysis. Delivered systems processing 200K+ daily events with 99.99% message delivery reliability and automated tests maintaining 90%+ code coverage.'
Para 'Technical Skills' 'Heading1'
Para 'Azure: AKS, Container Apps, Functions, App Service, API Management, Front Door, Azure OpenAI Service, AI Search, Machine Learning, Event Hubs, Service Bus, Azure SQL, Cosmos DB, Key Vault, Azure AD, RBAC.'
Para 'Backend and APIs: Python, FastAPI, Django, Node.js, NestJS, Express, TypeScript, C#, ASP.NET Core; REST, OpenAPI, GraphQL, gRPC; microservices, event-driven systems, DDD, CQRS, Clean Architecture.'
Para 'Infrastructure and delivery: Docker, Kubernetes, Helm, Terraform, Azure Bicep, ARM templates, Ansible, Azure DevOps Pipelines, GitHub Actions, Jenkins, ArgoCD, GitOps; dev, QA, and production environments.'
Para 'Observability and security: Azure Monitor, Application Insights, Log Analytics, OpenTelemetry, Prometheus, Grafana, Loki; OAuth 2.0, OIDC, JWT, RBAC, secrets management, automated security scanning, DevSecOps.'
Para 'AI and full stack: Azure OpenAI, LangChain, Semantic Kernel, RAG, vector search, pgvector, PostgreSQL, Redis, Kafka; React, Angular, Vue.js, Next.js; xUnit, NUnit, Jest, Vitest, PyTest, Playwright.'
Para 'Professional Experience' 'Heading1'
Job 'Senior Full Stack Engineer' 'USS IT CONSULTANTS L.L.C. | Contracted to 7X / EPG' 'Aug 2024 - Present | Dubai, UAE'
Bullet 'Built backend services for an AI-enabled platform using .NET 9 ASP.NET Core, Node.js 22 NestJS on Azure Functions, and Python 3.12 FastAPI for ML inference; scaled services on Kubernetes and Azure Container Apps.'
Bullet 'Integrated Azure OpenAI Service, LangChain, Semantic Kernel, Azure AI Search, and PostgreSQL pgvector into a production RAG pipeline with sub-2-second responses for natural-language content search.'
Bullet 'Deployed and operated services on Azure Container Apps and AWS EKS; used ArgoCD GitOps for declarative deployments, reconciliation, and an audit trail of production changes.'
Bullet 'Automated infrastructure provisioning with Terraform and Azure DevOps, creating environments and AI service dependencies in under five minutes.'
Bullet 'Handled production incidents and on-call support using OpenTelemetry, Azure Monitor, Application Insights, Grafana, Loki, and Prometheus; restored services through rollback or traffic mitigation and delivered RCA, alert improvements, and permanent fixes.'
Bullet 'Processed 200K+ daily events through Kafka, Azure Event Hubs, and Redis Streams with 99.99% message delivery reliability. Maintained 90%+ test coverage across .NET, Node.js, Python, and browser workflows.'
Bullet 'Delivered React, Vue.js, and Next.js frontends, a shared TypeScript UI layer, and a federated GraphQL gateway integrating domain APIs and ML endpoints.'
Job 'Senior Full Stack Engineer' 'GAC Group | Global Logistics Platform' 'Oct 2023 - Aug 2024 | Dubai, UAE'
Bullet 'Designed logistics microservices with .NET 6, Node.js NestJS, and Python FastAPI; defined REST/OpenAPI contracts, GraphQL APIs, and gRPC integration between domain services.'
Bullet 'Deployed on Azure Kubernetes Service with AWS Fargate for DR/batch workloads; provisioned infrastructure with Terraform and Ansible, and automated CI/CD through GitHub Actions with security scanning and container image signing.'
Bullet 'Investigated API, container, messaging, and deployment incidents using Azure Monitor, CloudWatch, and centralized logs; executed recovery, completed RCA, and improved alerts and runbooks.'
Bullet 'Integrated an AWS Bedrock and LangChain document-processing pipeline; delivered React, Angular, and Vue.js applications in a shared TypeScript monorepo.'
[void]$script:body.Append('<w:p><w:r><w:br w:type="page"/></w:r></w:p>')
Para 'Professional Experience Continued' 'Heading1'
Job 'Senior Full Stack Engineer' 'Merik Solutions | Cloud Transformation and AI Analytics' 'Nov 2020 - Sep 2023 | Islamabad, Pakistan'
Bullet 'Led enterprise migrations to Azure using .NET 5/6 ASP.NET Core microservices on AKS, Node.js Express on Azure Functions for event-driven integrations, and Python FastAPI for ML inference.'
Bullet 'Implemented Azure DevOps CI/CD and Bicep infrastructure as code; standardized dev, QA, and production environments with containers and Helm charts to resolve environment-parity failures.'
Bullet 'Published REST and GraphQL APIs through Azure API Management with OpenAPI documentation; secured services with Azure Key Vault, OAuth 2.0/OIDC, and Azure AD, supporting an ISO 27001-aligned security posture for two enterprise deployments.'
Bullet 'Implemented Azure Monitor and Application Insights for distributed tracing and production observability across platform services.'
Bullet 'Built forecasting, churn prediction, and anomaly-detection pipelines with Python and Scikit-learn; trained and versioned models through Azure Machine Learning Pipelines and served them through FastAPI.'
Bullet 'Automated document extraction with Azure Cognitive Services and Python post-processing; delivered Angular, React, and Vue.js interfaces for enterprise workflows and analytics.'
Job 'Senior Software Engineer' 'Calrom Pvt Ltd | Airline Reservation and Operations Platform' 'Dec 2017 - Oct 2020 | Lahore, Pakistan'
Bullet 'Designed reservation and scheduling microservices with ASP.NET Core 3.1, DDD, CQRS, and Event Sourcing, providing a replay-capable audit trail of booking changes.'
Bullet 'Migrated CI/CD from Jenkins to Azure DevOps; containerized services with Docker and orchestrated Kubernetes releases with Helm, replacing multi-hour manual deployments with repeatable automated releases and rollback capability.'
Bullet 'Built a Node.js API gateway and backend-for-frontend layer; used gRPC for booking workflows and RabbitMQ for independently deployable notification and audit consumers.'
Bullet 'Delivered Angular real-time operations dashboards and a React scheduling application with a shared TypeScript component library.'
Job 'Software Engineer' 'UDHC | Enterprise Web Applications' 'Oct 2016 - Nov 2017 | Lahore, Pakistan'
Bullet 'Developed enterprise applications with ASP.NET MVC and Web API, Entity Framework, Microsoft SQL Server, T-SQL procedures, and reporting queries.'
Bullet 'Built responsive JavaScript interfaces, improved build automation with Node.js, Gulp, and npm scripts, and validated services with NUnit and Postman.'
Para 'Education' 'Heading1'
Para 'Master of Software Engineering' 'Job'
Para 'Superior University | Nov 2022 - Nov 2024 | Lahore, Pakistan'
Para 'Bachelor of Computer Science' 'Job'
Para 'University of Sargodha | Oct 2012 - Sep 2016 | Sargodha, Pakistan'
Para 'Certification' 'Heading1'
Para 'Microsoft Certified: Azure Solutions Architect Expert (AZ-305)'
$document = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>' + $script:body.ToString() + '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="720" w:right="850" w:bottom="720" w:left="850" w:header="360" w:footer="360"/></w:sectPr></w:body></w:document>'
$styles = @'
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:color w:val="000000"/><w:sz w:val="20"/></w:rPr></w:rPrDefault><w:pPrDefault><w:pPr><w:spacing w:after="65" w:line="235" w:lineRule="auto"/><w:widowControl/></w:pPr></w:pPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>
<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/><w:pPr><w:keepNext/><w:spacing w:after="45"/></w:pPr><w:rPr><w:b/><w:sz w:val="44"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Subtitle"><w:name w:val="Subtitle"/><w:basedOn w:val="Normal"/><w:pPr><w:keepNext/><w:spacing w:after="80"/></w:pPr><w:rPr><w:b/><w:sz w:val="24"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Contact"><w:name w:val="Contact"/><w:basedOn w:val="Normal"/><w:pPr><w:keepNext/><w:spacing w:after="30"/></w:pPr><w:rPr><w:sz w:val="19"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:pPr><w:keepNext/><w:keepLines/><w:spacing w:before="140" w:after="70"/><w:outlineLvl w:val="0"/></w:pPr><w:rPr><w:b/><w:sz w:val="24"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Job"><w:name w:val="Job"/><w:basedOn w:val="Normal"/><w:pPr><w:keepNext/><w:spacing w:before="90" w:after="30"/></w:pPr><w:rPr><w:b/><w:sz w:val="21"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Company"><w:name w:val="Company"/><w:basedOn w:val="Normal"/><w:pPr><w:keepNext/><w:spacing w:after="20"/></w:pPr><w:rPr><w:b/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Dates"><w:name w:val="Dates"/><w:basedOn w:val="Normal"/><w:pPr><w:keepNext/><w:spacing w:after="65"/></w:pPr><w:rPr><w:i/><w:sz w:val="19"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Bullet"><w:name w:val="Bullet"/><w:basedOn w:val="Normal"/><w:pPr><w:keepLines/><w:spacing w:after="55"/></w:pPr></w:style>
</w:styles>
'@
$numbering = '<w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:abstractNum w:abstractNumId="0"><w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="&#8226;"/><w:lvlJc w:val="left"/><w:pPr><w:tabs><w:tab w:val="num" w:pos="220"/></w:tabs><w:ind w:left="220" w:hanging="220"/></w:pPr></w:lvl></w:abstractNum><w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num></w:numbering>'
$parts = @{
    '[Content_Types].xml' = '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/><Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/></Types>'
    '_rels/.rels' = '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>'
    'word/_rels/document.xml.rels' = '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/></Relationships>'
    'word/document.xml' = $document
    'word/styles.xml' = $styles
    'word/numbering.xml' = $numbering
}
$stream = [IO.File]::Open($out,[IO.FileMode]::Create)
$zip = [IO.Compression.ZipArchive]::new($stream,[IO.Compression.ZipArchiveMode]::Create)
foreach ($name in $parts.Keys) {
    [xml]$check = $parts[$name]
    $entry = $zip.CreateEntry($name)
    $writer = [IO.StreamWriter]::new($entry.Open(),[Text.UTF8Encoding]::new($false))
    $writer.Write($parts[$name]); $writer.Dispose()
}
$zip.Dispose(); $stream.Dispose()
Write-Output $out
