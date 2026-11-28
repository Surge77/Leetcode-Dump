# 🔹 Computer Networks for SDE Interviews

Short answers you should be able to say aloud in under a minute each. The question that ties them together is *"what happens when you type a URL and press Enter?"*, so that walkthrough comes first.

## 🔹 What Happens When You Type a URL

1. **Parse** the URL: scheme (`https`), host (`example.com`), port (443 by default), path, query.
2. **DNS**: browser cache → OS cache → the resolver (your ISP or 1.1.1.1). On a miss the resolver asks a root server → the `.com` TLD server → the domain's authoritative server, and gets an `A` (IPv4) or `AAAA` (IPv6) record. The answer is cached for its **TTL**.
3. **TCP**: three-way handshake `SYN → SYN-ACK → ACK` to the server's IP on port 443. (HTTP/3 uses QUIC over UDP instead.)
4. **TLS 1.3**: client hello (supported ciphers, key share) → server hello + certificate. The client checks the certificate chain against its trusted roots and the hostname, both sides derive session keys, and encrypted traffic starts after one round trip.
5. **HTTP request**: `GET /path` with headers (`Host`, cookies, `Accept-Encoding`). A load balancer or reverse proxy may route it to one of many servers. The response comes back with a status code, headers (`Cache-Control`, `Set-Cookie`) and a body.
6. **Render**: parse HTML → DOM, CSS → CSSOM, run JS, fetch sub-resources (often from a CDN, reusing the connection), lay out, paint.

Follow-ups to expect: *where can caching happen?* (browser, CDN, reverse proxy, application, database), *why is the second visit faster?* (DNS, TLS session resumption, HTTP cache), *what if DNS fails?*

## 🔹 The Layers

| OSI layer | TCP/IP layer | Examples | Unit |
|---|---|---|---|
| 7 Application, 6 Presentation, 5 Session | Application | HTTP, DNS, TLS*, SMTP, SSH | message |
| 4 Transport | Transport | TCP, UDP, QUIC | segment / datagram |
| 3 Network | Internet | IP, ICMP, routing | packet |
| 2 Data link, 1 Physical | Link | Ethernet, Wi-Fi, ARP*, switches | frame / bits |

\*TLS sits between transport and application; ARP maps IP → MAC inside one local network.

## 🔹 TCP vs UDP

| | TCP | UDP |
|---|---|---|
| Connection | Handshake first | None |
| Delivery | Reliable, ordered: sequence numbers, ACKs, retransmission | Best effort, may drop or reorder |
| Control | Flow control (receiver window) and congestion control (slow start, AIMD) | None, the app decides |
| Header | 20+ bytes | 8 bytes |
| Use for | Web, APIs, file transfer, databases | DNS, video calls, games, QUIC |

* **Three-way handshake**: `SYN(seq=x)` → `SYN-ACK(seq=y, ack=x+1)` → `ACK(ack=y+1)`. Two messages are not enough because both sides must confirm they can send *and* receive.
* **Teardown**: `FIN → ACK`, `FIN → ACK` (four steps; each direction closes separately). The side that closes first waits in **TIME_WAIT** (2 × MSL) so late packets don't leak into a new connection.
* **Flow control** protects the *receiver* (sliding window). **Congestion control** protects the *network* (congestion window: slow start doubles it, a loss halves it).
* **Head-of-line blocking**: one lost TCP segment stalls everything behind it. This is why HTTP/3 moved to QUIC, whose streams are independent.

## 🔹 HTTP

* **Methods**: `GET` (read, safe, idempotent), `POST` (create or act, not idempotent), `PUT` (replace, idempotent), `PATCH` (partial update), `DELETE` (idempotent). *Idempotent* = repeating it has the same effect as doing it once, so it is safe to retry.
* **Status codes**: `200` OK, `201` Created, `204` No Content, `301`/`308` permanent redirect, `302`/`307` temporary, `304` Not Modified, `400` Bad Request, `401` unauthenticated, `403` forbidden (authenticated but not allowed), `404`, `409` Conflict, `429` Too Many Requests, `500`, `502` Bad Gateway (the proxy got a bad answer from upstream), `503` Unavailable, `504` Gateway Timeout.
* **Versions**: HTTP/1.1 = one request at a time per connection (keep-alive reuses the connection). HTTP/2 = many streams multiplexed over one TCP connection, binary framing, header compression. HTTP/3 = HTTP/2's ideas over QUIC (UDP), no TCP head-of-line blocking, faster handshakes.
* **Caching**: `Cache-Control: max-age=3600`, `no-cache` (revalidate first), `no-store` (never cache). Validators: `ETag` + `If-None-Match`, or `Last-Modified` + `If-Modified-Since`, give `304` with no body.
* **Cookies** carry session state over a stateless protocol: `HttpOnly` (no JS access, limits XSS damage), `Secure` (HTTPS only), `SameSite=Lax/Strict` (limits CSRF).
* **CORS**: the browser blocks cross-origin reads unless the server answers with `Access-Control-Allow-Origin`. Non-simple requests send an `OPTIONS` preflight first. CORS is enforced by browsers, not servers, so it is not an auth mechanism.
* **REST vs WebSocket vs SSE vs long polling**: request/response vs a full-duplex persistent connection (chat, collaboration) vs a server → client stream over HTTP (live feeds) vs a held-open request (fallback).

## 🔹 HTTPS and TLS

* **Goals**: confidentiality (encryption), integrity (MACs), authentication (certificates).
* **Asymmetric crypto** (key exchange, ECDHE) agrees on a **symmetric** session key (AES-GCM, ChaCha20); symmetric is used for the data because it is fast.
* **Certificates**: a CA signs "this public key belongs to example.com". The browser trusts a chain ending at a root CA it ships with. Forward secrecy (ephemeral keys) means a stolen server key can't decrypt past traffic.

## 🔹 DNS

* Record types: `A`/`AAAA` (IP), `CNAME` (alias to another name), `MX` (mail), `TXT` (verification, SPF), `NS` (authoritative servers).
* Mostly UDP port 53; TCP for large answers and zone transfers.
* DNS-based load balancing returns different IPs per query; GeoDNS answers by the client's location. TTL trades freshness for fewer lookups.

## 🔹 IP Addressing and Routing

* IPv4 = 32 bits; **CIDR** `10.0.0.0/24` = 256 addresses (24 network bits). Private ranges: `10/8`, `172.16/12`, `192.168/16`.
* **NAT** lets many private hosts share one public IP by rewriting ports; it is why inbound connections to a home machine need port forwarding.
* **DHCP** hands out IPs; **ARP** finds the MAC for an IP on the local network; routers forward packets by longest-prefix match.
* IPv6 = 128 bits, no NAT needed, written `2001:db8::1`.
* `ping` uses ICMP echo; `traceroute` uses increasing TTLs so each router reports back.

## 🔹 Proxies, Load Balancers, CDNs

* **Forward proxy** acts for clients (corporate filtering). **Reverse proxy** acts for servers (TLS termination, caching, routing): nginx, Envoy.
* **L4 load balancer** routes by IP/port (fast, protocol-agnostic). **L7** routes by HTTP content (path, header, cookie), so it can do sticky sessions and canary releases.
* Algorithms: round robin, least connections, consistent hashing (keeps a key on the same server as servers come and go).
* **CDN**: edge servers cache static content close to users; the origin is hit only on a miss.

## 🔹 Security Questions That Come Up

* **XSS**: injected script runs in other users' browsers → escape output, Content-Security-Policy, `HttpOnly` cookies.
* **CSRF**: a forged request rides the victim's cookies → `SameSite` cookies, anti-CSRF tokens.
* **SQL injection** → parameterised queries, never string concatenation.
* **DDoS** → rate limiting, CDN/WAF absorption, autoscaling.
* **Sessions vs JWT**: server-side session store (easy revocation) vs a signed self-contained token (stateless, hard to revoke before it expires; keep expiry short and refresh).

## 🔹 Rapid-Fire

| Question | Answer |
|---|---|
| Port numbers | HTTP 80, HTTPS 443, SSH 22, DNS 53, SMTP 25, PostgreSQL 5432, MySQL 3306, Redis 6379 |
| Hub vs switch vs router | broadcast everything / forward by MAC inside a LAN / forward by IP between networks |
| Why is DNS on UDP? | One small request and answer; a handshake would double the latency |
| What is MTU? | Max frame payload (1500 bytes on Ethernet); larger packets get fragmented or dropped |
| Latency vs bandwidth vs throughput | delay per message / capacity of the pipe / what you actually achieve |
| Socket | the (IP, port, protocol) endpoint a program reads and writes |
