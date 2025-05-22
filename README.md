## System Architecture: Visual Search Platform

```
+-----------------+          +---------------------+          +---------------------+
|     Web UI      +--------->    FastAPI Backend   +--------->  Semantic Search     |
| (Next.js + CSS) |          | (/search, /image)   |          | (OpenCLIP + FAISS)  |
+--------+--------+          +---------+-----------+          +----------+----------+
         |                               |                                 |
         |                               v                                 v
         |                      +---------------------+          +---------------------+
         |                      | Captioning Engine   |<---------+   Embedding Store   |
         |                      | (BLIP model)        |          |   (FAISS + metadata)|
         |                      +---------------------+          +---------------------+
         |                               |                                 |
         v                               v                                 v
+-----------------+          +---------------------+          +---------------------+
|  Explanation    |<---------+  Image Storage      |          |  Local/Cloud Images |
|   Output        |          |  (retrieval source) |          |                     |
+-----------------+          +---------------------+          +---------------------+
```
