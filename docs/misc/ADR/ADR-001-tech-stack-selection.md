# ADR-001: Tech Stack Selection for CLI Documentation Tool

**Date:** 2025-11-24
**Status:** Proposed
**Decision Makers:** Technical Lead

---

## Context

Building CLI tool for AI coding agents to search/retrieve documentation with:

**Requirements:**
- Natural language queries → structured documentation responses
- Two modes: (1) Crawl/index docs from URLs, (2) Search via Context7
- <1s startup time (CLI constraint)
- Token-efficient output for AI agents
- Easy install: Python + uv only
- Local caching (offline capability)
- Cross-platform support
- LLM provider flexibility

**Constraints:**
- Must be Python-based
- No complex dependency chains
- Simple architecture (avoid over-engineering)

---

## Decision

### **Primary Stack**

**LangChain (langchain-core) + Crawl4AI + Context7 REST API**

```
CLI Interface (Click/Typer)
    ↓
Agent/Orchestration: LangChain/LangGraph
    - Query processing
    - Response generation
    - Tool orchestration
    ↓
Documentation Sources:
    ├─ Context7 REST API (primary, cached)
    │  - Up-to-date library docs
    │  - Version-specific retrieval
    │  - 50 queries/day free tier
    │
    └─ Crawl4AI (fallback/custom docs)
       - Web crawling for unlisted libraries
       - Local indexing
       - Offline access
    ↓
Vector Store (optional): FAISS/Chroma
    - Local embedding storage
    - Fast retrieval
    - Persistent cache
```

**Core Dependencies:**
```
# requirements.txt
langchain-core>=0.3.0        # ~180ms startup
langchain-anthropic>=0.2.0   # LLM integration
crawl4ai>=0.4.0              # Web scraping
anthropic>=0.25.0            # Direct SDK access
click>=8.1.0                 # CLI framework
requests>=2.31.0             # Context7 API
faiss-cpu>=1.8.0             # Vector search (optional)
```

---

## Rationale

### **Why LangChain?**

| Criterion | Score | Justification |
|-----------|-------|---------------|
| **Startup Time** | ✅ 180ms | Fastest framework option, well within <1s requirement |
| **Project History** | ✅ 2.5 years | Longest development, enterprise adoption (Uber, LinkedIn, Klarna) |
| **Ecosystem** | ✅ Extensive | 100+ document loaders, 50+ integrations |
| **Flexibility** | ✅ High | Easy provider switching, minimal lock-in |
| **Complexity** | ⚠️ Moderate | More features than needed, but core is lightweight |

**Maturity Comparison:**

| Framework | Project Age | Pre-v1.0 Production | v1.0 Release | Assessment |
|-----------|-------------|---------------------|--------------|------------|
| **Instructor** | 2+ years | Extensive (3M+/month) | ~2023 | Most mature |
| **LangChain** | 2.5 years | Extensive (Uber, LinkedIn) | Late Oct 2025 | Mature |
| **PydanticAI** | 1 year | Moderate (15M downloads) | Sept 4, 2025 | Mature |

**Key insight:** Version numbers don't define maturity. All three frameworks were production-ready before v1.0. LangChain has longest history; PydanticAI has cleaner API. Both are mature choices.

**vs Alternatives:**
- **PydanticAI**: Best MCP integration, v1.0 older than LangChain, but missing local caching
- **Instructor**: Simpler API, most stable v1.0, but lacks orchestration (no LangGraph equivalent)
- **LlamaIndex**: 770ms startup (4.3x slower), heavier dependencies (27+)

### **Why Crawl4AI?**

| Feature | Crawl4AI | Firecrawl | Spider |
|---------|----------|-----------|--------|
| **Cost** | Free | $83-333/mo | $49-249/mo |
| **Speed** | Fastest | Baseline | 2x faster |
| **Stars** | 38.7K | 19.4K | 15.3K |
| **LLM-optimized** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Local** | ✅ Self-hosted | ❌ Cloud only | ❌ Cloud only |

**Clear winner:** Free, fastest, most popular, self-hosted.

### **Why Context7 REST API (not MCP)?**

| Aspect | REST API | MCP Server |
|--------|----------|------------|
| **Dependencies** | Python only | Requires Node.js |
| **Startup** | Minimal | +100-200ms overhead |
| **Rate Limits** | 50/day free | Same (50/day free) |
| **Caching Control** | Full control | MCP server handles |
| **Best for** | CLI tools | IDE integration |

**Decision:** Use REST API directly. MCP adds Node.js dependency + protocol overhead without benefits for CLI.

### **Why NOT Hybrid (LangChain + LlamaIndex)?**

Production research shows:
- **70%** use single framework with integrated loaders
- **20%** use specialized crawler + single framework
- **10%** use hybrid (rare, often unjustified)

**Hybrid complexity not justified:**
- LlamaIndex 770ms vs LangChain 180ms (4.3x slower)
- LlamaIndex has 27+ dependencies vs LangChain's fewer
- No compelling feature gap (LangChain has 100+ loaders)

**Rule:** Only add LlamaIndex if need specific features (Agentic Document Workflows, 40% faster retrieval benchmarks)

---

## Architecture

### **Component Breakdown**

```python
# cli.py - Main entry point
@click.command()
@click.argument('query')
@click.option('--library', help='Library context (e.g., vercel/next.js)')
@click.option('--mode', type=click.Choice(['context7', 'local', 'hybrid']))
def search(query: str, library: str, mode: str):
    """Search documentation and answer query"""

    # 1. Fetch documentation
    docs = get_documentation(library, query, mode)

    # 2. Generate response using LangChain
    response = agent.run(query=query, context=docs)

    # 3. Output structured result
    click.echo(response)


# context7_client.py - Context7 REST API integration
class Context7Client:
    """Direct REST API client with local caching"""

    def __init__(self, api_key: str = None, cache_ttl_hours: int = 24):
        self.api_key = api_key
        self.cache = Cache('.context7_cache', ttl=cache_ttl_hours)

    def get_docs(self, org: str, project: str, topic: str = None):
        # Check cache first
        # Fetch from API on miss
        # Store in persistent cache
        pass


# crawler.py - Crawl4AI integration
class DocumentationCrawler:
    """Crawl and index custom documentation"""

    async def crawl(self, url: str) -> str:
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url=url)
            return result.markdown.fit_markdown

    def index(self, docs: list[str]) -> VectorStoreIndex:
        # Create embeddings
        # Store in FAISS
        pass


# agent.py - LangChain orchestration
class DocumentationAgent:
    """LangChain agent with tool access"""

    def __init__(self):
        self.llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")
        self.tools = [context7_tool, crawler_tool]
        self.agent = create_react_agent(self.llm, self.tools)

    def run(self, query: str, context: str = None):
        # Process query
        # Use tools if needed
        # Generate structured response
        pass
```

### **Caching Strategy**

```python
# Three-tier cache hierarchy
1. Memory Cache (LRU):     Hot queries, session lifetime
2. Disk Cache (Shelve):    Context7 responses, 24-48h TTL
3. Vector Store (FAISS):   Crawled docs, persistent
```

**Expected API usage with caching:**
- Initial run: 10-20 Context7 API calls
- Subsequent runs: 1-2 API calls/day (cache hits)
- Well within 50/day free tier

---

## Consequences

### **Positive**

✅ **Fast startup**: 180ms (LangChain) + 50ms (imports) = <250ms total
✅ **Mature ecosystem**: 2.5 years production validation
✅ **Free tier sufficient**: 50/day Context7 + unlimited Crawl4AI
✅ **Simple architecture**: Single framework, no unjustified complexity
✅ **Flexible**: Easy to swap LLM providers (Anthropic, OpenAI, local)
✅ **Offline capable**: Local caching + Crawl4AI fallback
✅ **Python-only**: No Node.js or other language dependencies

### **Negative**

⚠️ **LangChain learning curve**: More complex than Instructor
⚠️ **Framework overhead**: 180ms startup vs 120ms (PydanticAI)
⚠️ **Context7 rate limit**: Need caching strategy for >50 queries/day
⚠️ **Crawl4AI dependency**: Requires Playwright (heavy install)

### **Risks & Mitigations**

| Risk | Impact | Mitigation |
|------|--------|------------|
| Context7 rate limit hit | Can't fetch fresh docs | Aggressive caching (24-48h TTL), Crawl4AI fallback |
| LangChain API changes | Breaking changes | Pin versions, monitor deprecations |
| Crawl4AI rendering issues | Can't scrape some sites | Fallback to simpler parsers (trafilatura, BeautifulSoup) |
| Large dependency size | Slow install | Use `uv` for fast installs, document system requirements |

---

## Alternatives Considered

### **Option A: PydanticAI + Crawl4AI**

**Strengths:**
- v1.0 since Sept 2025 (older than LangChain v1.0)
- Best MCP integration (3 transport mechanisms)
- Fastest startup (120ms)
- Clean Pydantic-native API
- 15M downloads, active development (now v1.22.0)

**Trade-offs:**
- Missing local caching (critical for CLI - must implement yourself)
- Smaller ecosystem than LangChain (fewer document loaders)
- Less enterprise adoption history

**When to use:** If MCP integration is critical or prefer cleaner API over larger ecosystem

### **Option B: Instructor + Crawl4AI**

**Strengths:**
- Simplest API (5 lines vs 15 lines)
- Most mature wrapper (2+ years)
- Lightest weight (210ms startup)

**Rejected because:**
- No orchestration layer (would need to build LangGraph equivalent)
- Limited tool/agent support
- Better for simple structured outputs, not complex workflows

**When to use:** If requirements simplify to basic query → response (no multi-step orchestration)

### **Option C: LangChain + LlamaIndex (Hybrid)**

**Rejected because:**
- LlamaIndex adds 770ms startup (4.3x slower than LangChain alone)
- 27+ dependencies vs LangChain's fewer
- 70% of production implementations use single framework
- No feature gap justifying complexity

**When to use:** Need LlamaIndex-specific features (Agentic Document Workflows, advanced retrieval)

### **Option D: Minimal Stack (Direct Anthropic SDK)**

**Strengths:**
- Lightest possible (270ms startup)
- Maximum control, zero framework overhead
- Simple mental model

**Rejected because:**
- Would need to implement:
  - Tool orchestration (LangGraph equivalent)
  - Document loader abstraction
  - Prompt management
  - Caching layer
- Reinventing the wheel (violates "Never Re-Invent the Wheel" rule)

**When to use:** Requirements become extremely simple (single LLM call, no tools)

---

## Implementation Plan

### **Phase 1: Core CLI (Week 1)**

1. Setup project structure with `uv`
2. Implement Context7 REST client with caching
3. Basic CLI interface (Click)
4. Simple LangChain agent (query → Context7 → response)
5. Unit tests for Context7 client

**Success Criteria:**
- `contextdocs search "next.js routing" --library vercel/next.js` works
- <1s total execution time
- Cache hit rate >90% after initial run

### **Phase 2: Crawling Support (Week 2)**

1. Integrate Crawl4AI for custom documentation
2. Implement FAISS vector store for indexed docs
3. Add `contextdocs index <url>` command
4. Fallback logic: Context7 → local index → crawl on-demand

**Success Criteria:**
- Can index arbitrary documentation URLs
- Offline search works from local index
- Crawling completes <30s for typical docs site

### **Phase 3: Advanced Features (Week 3)**

1. Multi-library context aggregation
2. Structured output formats (JSON, markdown, plain text)
3. Interactive mode (follow-up questions)
4. Configuration file support (`contextdocs.yaml`)

**Success Criteria:**
- Can query multiple libraries in single request
- Output format configurable
- Interactive session maintains context

### **Phase 4: Polish & Release (Week 4)**

1. Comprehensive error handling
2. Progress indicators for long operations
3. Documentation (README, examples)
4. PyPI package publishing
5. CI/CD pipeline (tests, linting)

**Success Criteria:**
- `pip install contextdocs` works
- Complete user documentation
- Test coverage >80%

---

## Validation Criteria

Before finalizing this decision, validate:

- [ ] LangChain startup time <250ms on target platforms (macOS, Linux, Windows)
- [ ] Context7 API returns quality results for top 10 libraries (Next.js, React, etc.)
- [ ] Crawl4AI successfully indexes 5 diverse documentation sites
- [ ] Cache strategy keeps API usage <50 queries/day for typical usage
- [ ] Total CLI response time <2s for cached queries, <5s for uncached
- [ ] Installation via `uv pip install` completes <60s on fresh environment

---

## References

- **Research Documents:**
  - `research.md` - Comprehensive framework and crawler analysis
  - `tradeoff-matrix.md` - Scoring matrix for 6 tech stack options
  - `CORRECTIONS.md` - Corrections to initial analysis (date, startup times, maturity)
  - `recommendation-v2-corrected.md` - Corrected recommendation with production patterns

- **Key Data Points:**
  - LangChain startup: 180ms (measured)
  - Context7 free tier: 50 queries/day
  - Crawl4AI: 38.7K stars, 4-6x faster than competitors, free
  - Production pattern: 70% single framework, 20% specialized crawler + framework

- **External Resources:**
  - Context7 API: https://context7.com/docs/api-guide
  - Crawl4AI: https://github.com/unclecode/crawl4ai
  - LangChain docs: https://python.langchain.com/docs/introduction/
  - LangGraph: https://langchain-ai.github.io/langgraph/

---

## Notes

- **Context7 MCP not used** because adds Node.js dependency + protocol overhead without benefit for CLI
- **Hybrid architecture avoided** based on production research showing 70% use single framework
- **LlamaIndex rejected** due to 770ms startup (4.3x slower) and 27+ dependencies
- **PydanticAI is equally mature** - both PydanticAI and LangChain were production-ready before v1.0
- **LangChain chosen for ecosystem** (100+ loaders, longer history), not maturity (both are mature)
- **PydanticAI trade-off:** Missing local caching requires custom implementation; smaller ecosystem but cleaner API

---

## Decision Review

**Next review:** 2026-02-24 (3 months)
**Trigger for earlier review:**
- Context7 pricing changes affecting free tier
- LangChain releases breaking changes
- PydanticAI ecosystem significantly matures
- Performance targets not met in validation

**Approval Required From:** Technical Lead
**Implementation Owner:** TBD
