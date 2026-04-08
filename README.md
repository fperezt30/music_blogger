Project Description:
Built an automated music blogging pipeline that converts YouTube videos into structured WordPress posts using a hybrid architecture combining LLM-based content generation with Spotify API metadata enrichment.


E2E Pipeline:

YouTube URL (UI - Flask)
Metadata Extraction (YouTube)
Step 1: Entity Normalization (LLM)
Step 2: Metadata Enrichment (Spotify API + LLM fallback)
Content Generation (LLM - structured blog)
Image Handling (YouTube thumbnail validation)
WordPress Publishing (REST API)
UI Feedback (status + preview link)

Next Features:
-Improve UX
-Detect black bars on videos that have lower resolution in thumbnail
-Define rule for video with less than 10k views -> Follow Spotify Metadata (eg. media puzzle)


Lessons learned:
-Connect to OpenAI API
-Prompt Engineering
-Multistep agent to specialize task
-Using Multi-Step reasoning vs. MCP
-Initialization  + Sequence of Actions in Javascript


Lessons to learn:
-Use MCP to let agent orchestrate everything (eg. Create 1 TikTok video from this song with different angles) 
-Use automation like n8n if the task implies glue between services (eg. Post to Buffer, Instagram, TikTok)
-Use Evals for a more complex scenario (eg. agent for SME companies that need to train their employees)


Advanced topics (related mostly with scale problems):
-No async/job queue
-No persistance (database/logging)
-No observability (metrics)
-Weak matching logic scenarios
-No retry strategy when API call fails
-No idempotency
-No media pipeline
-No scheduling / batching logic

Related roles:
-Mid Level Backend / Product Engineer
-Applied AI Engineer
-Automation / Growth Engineer